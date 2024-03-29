from django.shortcuts import render
from django.urls import reverse
import logging
import json, os
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from config import settings
from django.views.defaults import page_not_found
from django.shortcuts import render, redirect, get_object_or_404
from invoices.forms import (
    ElectricInvoiceForm,
    KundenDataForm,
    PositionForm,
    SlsForm,
    BmaterialForm,
    UssForm,
    LeitungschutzschalterForm,
    HauptabzweigklemmeForm,
    MantelleitungForm,
    KabelKanalForm,
    ZahlerKabelForm,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
from invoices.models import ElectricInvoice, KundenData, Position
from authentication.models import User
from django.core.exceptions import PermissionDenied
from invoices import excel_generator, pdf_creator2
from shared.chat_bot import handle_message
import anvil.server
from django.contrib import messages
from django.db.models.functions import Cast
from django.db.models import IntegerField, Q, CharField
from django.views.decorators.csrf import requires_csrf_token

logger = logging.getLogger(__name__)
from django.views.defaults import permission_denied
from django.views.defaults import server_error


# User's profession check decorators
def elektriker_check(user):
    return User.objects.filter(id=user.id, beruf="Elektriker").exists()


def verkaufer_check(user):
    return User.objects.filter(id=user.id, beruf="Vertrieb").exists()


class ElektrikerCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return elektriker_check(self.request.user)  # type: ignore


# Login , Logout
class CustomLoginView(LoginView):
    template_name = "login.html"


class CustomLogoutView(LogoutView):
    template_name = "logout.html"


@anvil.server.callable
@requires_csrf_token
def login_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_staff == True:  # type: ignore
            login(request, user)
            return redirect("/admin")
        if user is not None and user.beruf == "Elektriker":  # type: ignore
            login(request, user)
            return redirect("invoices:home")
        elif user is not None and user.beruf == "Vertrieb":  # type: ignore
            login(request, user)
            return redirect("vertrieb_interface:home")
        else:
            return page_not_found(request, Exception())

    return render(request, "login.html", context)


def handler500(request):
    return render(request, "500.html", status=500)


def handler403(request, exception):
    return render(request, "403.html", status=403)


def handler404(request, exception):
    return render(request, "404.html", status=404)


# Pages
@anvil.server.callable
@user_passes_test(elektriker_check)
def home(request):
    return render(request, "home.html")


@anvil.server.callable
@user_passes_test(elektriker_check)
def profile(request):
    user = request.user
    context = {"user": user}
    return render(request, "profile.html", context)


@anvil.server.callable
@user_passes_test(elektriker_check)
def elektriker_kalender(request):
    return render(request, "elektriker_kalender.html")


@anvil.server.callable
@user_passes_test(elektriker_check)
def help(request):
    return render(request, "help.html")


# Chat_bot view
@anvil.server.callable
@user_passes_test(elektriker_check)
@csrf_exempt
def chat_bot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get("question", "")
        response = handle_message(question)
        return JsonResponse({"response": response})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@anvil.server.callable
@csrf_exempt
def sync_data(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # Create forms and save data
        electric_invoice_form = ElectricInvoiceForm(data=data["electric_invoice"])
        kunden_data_form = KundenDataForm(data=data["kunden_data"])
        position_form = PositionForm(data=data["position"])
        if (
            electric_invoice_form.is_valid()
            and kunden_data_form.is_valid()
            and position_form.is_valid()
        ):
            # save ElectricInvoice form
            electric_invoice = electric_invoice_form.save(commit=False)
            electric_invoice.user = request.user
            electric_invoice.save()

            # save KundenData form
            kunden_data = kunden_data_form.save(commit=False)
            kunden_data.invoice = electric_invoice
            kunden_data.save()

            # save Position form
            position = position_form.save(commit=False)
            position.invoice = electric_invoice
            position.save()

            return redirect("inbvoices:view_orders")

        else:
            # Return the errors if the form is not valid
            return page_not_found(request, Exception())
            # return JsonResponse(
            #     {
            #         "status": "error",
            #         "electric_invoice_errors": electric_invoice_form.errors,
            #         "kunden_data_errors": kunden_data_form.errors,
            #         "position_errors": position_form.errors,
            #     }
            # )

    return page_not_found(request, Exception())


@anvil.server.callable
@user_passes_test(elektriker_check)
def create_invoice(request):
    if request.method == "POST":
        if "create_blank_invoice" in request.POST:
            blank_invoice = ElectricInvoice(user=request.user)
            blank_invoice.save()

            kunden_data = KundenData(invoice=blank_invoice)
            kunden_data.save()
            return HttpResponseRedirect(
                reverse("invoices:edit_invoice", args=[blank_invoice.invoice_id])
            )

        form_invoice = ElectricInvoiceForm(request.POST)
        form_kunden_data = KundenDataForm(request.POST)
        form_position = PositionForm(request.POST)

        if (
            form_invoice.is_valid()
            and form_kunden_data.is_valid()
            and form_position.is_valid()
        ):
            invoice = form_invoice.save(commit=False)
            invoice.user = request.user
            invoice.save()

            kunden_data = form_kunden_data.save(commit=False)
            kunden_data.invoice = invoice
            kunden_data.save()

            position = form_position.save(commit=False)
            position.invoice = invoice
            position.save()

            return redirect("your_success_url")
    else:
        form_invoice = ElectricInvoiceForm()
        form_kunden_data = KundenDataForm()
        form_position = PositionForm()

    context = {
        "form_invoice": form_invoice,
        "form_kunden_data": form_kunden_data,
        "form_position": form_position,
    }
    return render(request, "create_invoice.html", context)


class EditInvoiceView(LoginRequiredMixin, FormMixin, DetailView):
    model = ElectricInvoice
    form_class = KundenDataForm
    template_name = "edit_invoice.html"
    context_object_name = "invoice"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()  # This will use your custom 403.html template
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        invoice_id = self.kwargs.get("invoice_id")
        return get_object_or_404(ElectricInvoice, invoice_id=invoice_id)

    def get_queryset(self):
        user = self.request.user
        return ElectricInvoice.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["kunden_data_form"] = KundenDataForm()
        context["sls_form"] = SlsForm(instance=self.object.positions.first())  # type: ignore
        context["uss_form"] = UssForm(instance=self.object.positions.first())  # type: ignore
        context["b_material_form"] = BmaterialForm(instance=self.object.positions.first())  # type: ignore
        context["leitungschutzschalter_form"] = LeitungschutzschalterForm(instance=self.object.positions.first())  # type: ignore
        context["hauptabzweigklemme_form"] = HauptabzweigklemmeForm(instance=self.object.positions.first())  # type: ignore
        context["mantelleitung_form"] = MantelleitungForm(instance=self.object.positions.first())  # type: ignore
        context["kabelkanal_form"] = KabelKanalForm(instance=self.object.positions.first())  # type: ignore
        context["zahler_kabel_form"] = ZahlerKabelForm(instance=self.object.positions.first())  # type: ignore
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "delete_position" in request.POST:
            return self.delete_position(request)
        elif "uss" in request.POST:
            return self.add_uss(request)
        elif "sls" in request.POST:
            return self.add_sls(request)
        elif "b_material" in request.POST:
            return self.add_b_material(request)
        elif "leitungschutzschalter" in request.POST:
            return self.add_leitungschutzschalter(request)
        elif "hauptabzweigklemme" in request.POST:
            return self.add_hauptabzweigklemme(request)
        elif "mantelleitung" in request.POST:
            return self.add_mantelleitung(request)
        elif "kabelkanal" in request.POST:
            return self.add_kabelkanal(request)
        elif "zahler_kabel" in request.POST:
            return self.add_zahler_kabel(request)
        elif "kunden_data" in request.POST:
            return self.update_kunden_data(request)
        else:
            return self.form_invalid(self.get_form())

    def update_kunden_data(self, request):
        invoice = self.get_object()
        kunden_data = getattr(invoice, "kunden_data", None)

        if kunden_data is not None:
            form = KundenDataForm(request.POST, instance=kunden_data)
        else:
            form = KundenDataForm(request.POST)

        if form.is_valid():
            try:
                kunden_data = form.save(commit=False)
                if kunden_data.invoice_id is None:
                    kunden_data.invoice = invoice
                kunden_data.save()
                invoice.is_locked = True
                invoice.save()
                return redirect("invoices:edit_invoice", invoice_id=invoice.invoice_id)
            except IntegrityError as e:
                logger.error("Error occurred while saving form: %s", str(e))
                form.add_error(None, "Database error: " + str(e))
                return self.form_invalid(form)
            except Exception as e:
                logger.error("Unexpected error: %s", str(e))
                form.add_error(None, "Unexpected error: " + str(e))
                return self.form_invalid(form)
        else:
            logger.error("Form validation failed: %s", str(form.errors))
            return self.form_invalid(form)

    def add_sls(self, request):
        form = SlsForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["sls"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_uss(self, request):
        form = UssForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["uss"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_hauptabzweigklemme(self, request):
        form = HauptabzweigklemmeForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["hauptabzweigklemme"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_leitungschutzschalter(self, request):
        form = LeitungschutzschalterForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["leitungschutzschalter"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_mantelleitung(self, request):
        form = MantelleitungForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["mantelleitung"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_kabelkanal(self, request):
        form = KabelKanalForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["kabelkanal"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_zahler_kabel(self, request):
        form = ZahlerKabelForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["zahler_kabel"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def add_b_material(self, request):
        form = BmaterialForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.position = form.cleaned_data["b_material"]
            position.invoice = self.get_object()
            position.save()
            return redirect(
                "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
            )
        else:
            return self.form_invalid(form)

    def delete_position(self, request):
        position_id = request.POST.get("delete_position")
        position = get_object_or_404(Position, pk=position_id)
        position.delete()
        return redirect(
            "invoices:edit_invoice", invoice_id=self.get_object().invoice_id
        )

    def form_invalid(self, form, **forms):
        context = self.get_context_data()
        context.update({"form": form})
        context.update(forms)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse("invoices:success_page", args=[str(self.object.pk)])


# ANVIL MAIN UPDATE INVOICE VIEW


@anvil.server.callable
def update_kunden_data(request_data, invoice_id):
    invoice = get_object_or_404(ElectricInvoice, invoice_id=invoice_id)
    kunden_data = getattr(invoice, "kunden_data", None)

    if kunden_data is not None:
        form = KundenDataForm(request_data, instance=kunden_data)
    else:
        form = KundenDataForm(request_data)

    if form.is_valid():
        kunden_data = form.save(commit=False)
        if kunden_data.invoice_id is None:
            kunden_data.invoice = invoice
        kunden_data.save()
        invoice.is_locked = True
        invoice.save()
        return True
    else:
        return form.errors


# Angebots List view
class ViewOrders(ElektrikerCheckMixin, ListView):
    model = ElectricInvoice
    template_name = "view_orders.html"
    context_object_name = "invoices"
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(
            user=self.request.user, invoice_id__regex=r"^.*$"
        )

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(invoice_id__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_invoices = self.get_queryset()
        paginator = Paginator(list_invoices, self.paginate_by)

        page = self.request.GET.get("page")

        try:
            invoices = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            invoices = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            invoices = paginator.page(paginator.num_pages)

        context["invoices"] = invoices
        return context


@anvil.server.callable
def get_orders():
    # Note: this function does not have request parameter
    return list(ElectricInvoice.objects.values())


# PDF and EXCEL generators views


@anvil.server.callable
def create_pdf(request, invoice_id):
    invoice = get_object_or_404(ElectricInvoice, invoice_id=invoice_id)
    user = invoice.user
    if request.user != invoice.user and not request.user.is_staff:
        raise Http404("Permission denied.")
    mats = Position.objects.filter(invoice=invoice)
    k_data = KundenData.objects.filter(invoice=invoice)
    eintrag = 0
    pdf_creator2.createOfferPdf(
        invoice,
        eintrag,
        user,
        mats,
        k_data,
    )
    # Create the link to the PDF file
    pdf_link = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/Angebot_{invoice.invoice_id}.pdf")  # type: ignore

    # Redirect to the PDF file link
    return HttpResponseRedirect(pdf_link)


@anvil.server.callable
def PDFInvoicesListView(request, invoice_id):
    invoice = get_object_or_404(ElectricInvoice, invoice_id=invoice_id)
    user = invoice.user
    if request.user != invoice.user and not request.user.is_staff:
        raise Http404("Permission denied.")

    # Get the search query (returns None if no query has been specified)
    query = request.GET.get("q")

    # Filter the invoices based on the search query
    if query:
        user_invoices = ElectricInvoice.objects.filter(
            Q(user=user)
            & (Q(invoice_id__icontains=query) | Q(current_date__icontains=query))
        )
    else:
        user_invoices = ElectricInvoice.objects.filter(user=user)

    # Create a list of invoice file paths
    angebot_path = os.path.join(settings.MEDIA_URL, f"pdf/usersangebots/{user.username}/")  # type: ignore

    invoice_files = [
        os.path.join(angebot_path, f"Angebot_{invoice.invoice_id}.pdf")
        for invoice in user_invoices
    ]

    # Zip the two lists together
    zipped_invoices = list(zip(user_invoices, invoice_files))

    # Set up the paginator (with, e.g., 10 items per page)
    paginator = Paginator(zipped_invoices, 10)

    # Get the page number specified in the GET request (if any)
    page = request.GET.get("page")

    # Fetch the appropriate page of results
    zipped_invoices = paginator.get_page(page)

    return render(
        request,
        "pdf_created.html",
        {
            "user": user,
            "zipped_invoices": zipped_invoices,
        },
    )


@anvil.server.callable
def create_excel(request, invoice_id):
    invoice = get_object_or_404(ElectricInvoice, invoice_id=invoice_id)
    user = invoice.user
    if request.user != invoice.user and not request.user.is_staff:
        raise Http404("Permission denied.")
    mats = Position.objects.filter(invoice=invoice)
    k_data = KundenData.objects.filter(invoice=invoice)
    excel_generator.generate_xlsx(
        user,
        invoice,
        mats,
        k_data,
    )

    excel_link = os.path.join(settings.MEDIA_URL, f"excel/usersangebots/{user.username}/Angebot_{invoice.invoice_id}.xlsx")  # type: ignore

    # Redirect to the PDF file link
    return HttpResponseRedirect(excel_link)


@anvil.server.callable
def EXCELInvoicesListView(request, invoice_id):
    invoice = get_object_or_404(ElectricInvoice, invoice_id=invoice_id)
    user = invoice.user
    if request.user != invoice.user and not request.user.is_staff:
        raise Http404("Permission denied.")
    user_invoices = ElectricInvoice.objects.filter(user=user)

    # Create a list of invoice file paths
    angebot_path = os.path.join(settings.MEDIA_URL, f"excel/usersangebots/{user.username}/")  # type: ignore

    invoice_files = [
        os.path.join(angebot_path, f"Angebot_{invoice.invoice_id}.xlsx")
        for invoice in user_invoices
    ]

    # Zip the two lists together
    zipped_invoices = zip(user_invoices, invoice_files)

    return render(
        request,
        "xlsx_created.html",
        {
            "user": user,
            "zipped_invoices": zipped_invoices,
        },
    )
