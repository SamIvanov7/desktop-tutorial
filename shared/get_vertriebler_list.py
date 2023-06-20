import requests
import json
from dotenv import load_dotenv, find_dotenv, set_key
from django.conf import settings
import os

settings.configure(default_settings="test_run_proj.config.settings", DEBUG=True)
load_dotenv()


def fetch_vertriebler_list_IDs():
    access_token = os.getenv("ZOHO_ACCESS_TOKEN")
    if not access_token:
        access_token = refresh_access_token()

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
            access_token = refresh_access_token()
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


def refresh_access_token():
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
