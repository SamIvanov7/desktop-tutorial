from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from schema_graph.views import Schema
from django.views.static import serve
from django.urls import re_path
from django.views import defaults as default_views
from invoices.views import handler404, handler403, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from invoices.views import handler403, handler404, handler500
from django.urls import path, include
from django.urls import path
from authentication.views import (
    update_vertrieblers,
    update_elektrikers,
    protected_schema_view,
)

urlpatterns = (
    [
        path(
            "admin/update_vertrieblers/",
            update_vertrieblers,
            name="update_vertrieblers",
        ),
        path(
            "admin/update_elektrikers/", update_elektrikers, name="update_elektrikers"
        ),
        path("admin/schema/", protected_schema_view, name="schema_view"),
        path("admin/", admin.site.urls),
        path("/", include("djoser.urls")),
        path("", include("djoser.urls.jwt")),
        path("", include("authentication.urls", namespace="authentication")),
        path("", include("vertrieb_interface.urls", namespace="vertrieb_interface")),
        path("elektriker_interface/", include("invoices.urls", namespace="invoices")),
        path(
            "elektriker_kalender",
            include("elektriker_kalender.urls", namespace="elektriker_kalender"),
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

# Error handlers
if settings.DEBUG:
    urlpatterns += [
        re_path(r"^403/$", handler403),
        re_path(r"^404/$", handler404),
        re_path(r"^500/$", handler500),
    ]
