from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv, find_dotenv, set_key
import requests
import json
import os
from random import randint
from config.settings import ENV_FILE

User = get_user_model()

load_dotenv(ENV_FILE)


class Command(BaseCommand):
    help = "Updates the User model with the list of users from Zoho"

    def fetch_vertriebler_list_IDs(self):
        access_token = os.getenv("ZOHO_ACCESS_TOKEN")
        if not access_token:
            access_token = self.refresh_access_token()

        url = "https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/Privatkunden1"

        headers = {
            "Authorization": f"Zoho-oauthtoken {access_token}",
        }

        # Define an empty set to store unique Vertriebler data
        vertriebler_set = set()

        # Specify the number of records to fetch per request
        limit = 100
        start_index = 0

        while True:
            params = {
                "from": start_index,
                "limit": limit,
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                access_token = self.refresh_access_token()
                headers["Authorization"] = f"Zoho-oauthtoken {access_token}"
                continue

            # Check the response status code
            elif response.status_code != 200:
                print(f"Failed to fetch data, status code: {response.status_code}")
                break
            print(f"access_token is alive, status code: {response.status_code}")
            data = json.loads(response.text)

            if not data["data"]:
                break

            for record in data["data"]:
                if (
                    "Vertriebler" in record
                    and "display_value" in record["Vertriebler"]
                    and "ID" in record["Vertriebler"]
                ):
                    vertriebler_set.add(
                        (
                            record["Vertriebler"]["display_value"],
                            record["Vertriebler"]["ID"],
                        )
                    )

            # Update the start index for the next batch of records
            start_index += limit

        # Convert the set to a list and print
        vertriebler_list = list(vertriebler_set)
        vertriebler_list = json.dumps(vertriebler_list, indent=4)
        return vertriebler_list

    def refresh_access_token(self):
        client_id = os.getenv("ZOHO_CLIENT_ID")
        client_secret = os.getenv("ZOHO_CLIENT_SECRET")
        refresh_token = os.getenv("ZOHO_REFRESH_TOKEN")

        url = f"https://accounts.zoho.eu/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token"

        response = requests.post(url)

        if response.status_code == 200:
            data = response.json()
            new_access_token = data.get("access_token")
            print("Access token refreshed.", new_access_token)

            env_file = find_dotenv()
            set_key(env_file, "ZOHO_ACCESS_TOKEN", new_access_token)

            return new_access_token
        else:
            print(f"Error refreshing token: {response.status_code}")

    def handle(self, *args, **kwargs):
        zoho_users_list = self.fetch_vertriebler_list_IDs()
        # Parse JSON string back to Python list
        zoho_users_list = json.loads(zoho_users_list)

        phone_counter = 4
        for user_info in zoho_users_list:
            # Ensure that user_info is a list with at least two elements
            if isinstance(user_info, list) and len(user_info) >= 2:
                names = user_info[0].split(" ")
                if len(names) < 2:
                    self.stdout.write(
                        f"Skipping user {user_info[0]} due to improper name format."
                    )
                    continue
                first_name = names[0]
                last_name = " ".join(names[1:]) if len(names) > 1 else ""
                zoho_id = int(user_info[1])
                username = (first_name + last_name).lower()
                email = first_name[0].lower() + last_name[0].lower() + "@juno-solar.com"
                kuerzel = first_name[0].upper() + last_name[0].upper()
                phone = "+49175" + str(randint(1000000, 9999999))

                # Check if a User with the provided zoho_id exists
                user_exists = User.objects.filter(zoho_id=zoho_id).exists()

                # If the User does not exist, create a new User
                if not user_exists:
                    new_user = User.objects.create(
                        zoho_id=zoho_id,
                        email=email,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        age=30,
                        phone=phone,
                        is_staff=False,
                        beruf="Vertrieb",
                        users_aufschlag=0,
                        typ="Vertrieb",
                        kuerzel=kuerzel,
                        is_active=True,
                        is_superuser=False,
                    )
                    new_user.set_password("tiara3903")
                    new_user.save()
                    phone_counter += 1
            else:
                self.stdout.write(
                    f"Skipping user {user_info} due to incorrect data format."
                )
