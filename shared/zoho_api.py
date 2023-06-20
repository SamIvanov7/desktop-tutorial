""" 
 Im Anhang sind die Code-Beispiele für das Auffrischen des access_token, die Anfrage aller Privatkunden und eines einzelnen Privatkunden anhand seiner ID. Speichere dir dringend die ID eines Privatkunden bzw. Elektriktermins in deiner Datenbank ab, damit es in Zukunft beim Update der Daten in Zoho einfach geht.

Wichtig ist immer die URL „https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/ und dann die Bezeichnung des Berichts im Privatanlagenportal, also z.B. „Privatkunden1“ oder "Elektrikkalender“.

client_id:  1000.ZUK8CKLOM7WOWEF8GHVEZSJWDN68AE
client_secret: 4a8d83ba191f54971358e31978d34a2b1fbb41d3c3
refresh_token:  1000.bdd6131b2a61f13e5f66199e53472b45.48ba19e2fbce6213f2984c050eae91d8
access_token 13:18: 1000.93955e396faca0ccbe9ed6029985f4b5.8fbe0f2504c7db21ef6e5ccab4290571

Viele Grüße
Fabian

"""

import re
import requests
import json


def connect_to_zoho_creator(client_id, client_secret, refresh_token, access_token):
    # Define the API endpoint
    api_endpoint = "https://creator.zoho.eu/api/json"

    # Prepare the payload with your credentials
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "access_token": access_token,
    }

    # Make a POST request to the Zoho Creator API
    response = requests.post(api_endpoint, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Convert the response content to JSON
        result = response.json()

        # Save the result to a JSON file
        with open("result.json", "w") as file:
            json.dump(result, file)

        print("Data saved to result.json file.")
    else:
        print("Failed to connect to Zoho Creator API.")


# Example usage:
client_id = "1000.ZUK8CKLOM7WOWEF8GHVEZSJWDN68AE"
client_secret = "4a8d83ba191f54971358e31978d34a2b1fbb41d3c3"
refresh_token = "1000.bdd6131b2a61f13e5f66199e53472b45.48ba19e2fbce6213f2984c050eae91d8"
access_token = "1000.b3134c1cec791290660698c77743e4b4.ea8f3d4a1a865b6c778ad119d746c6a3"

# def refresh_access_token(client_id, client_secret, refresh_token):
#     url = f"https://accounts.zoho.eu/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token"

#     response = requests.post(url)

#     if response.status_code == 200:  # success
#         data = response.json()
#         print(data)
#         new_access_token = data.get('access_token')
#         print("Access token refreshed.", new_access_token)
#         return new_access_token
#     else:
#         print(f"Error refreshing token: {response.status_code}")

# print(refresh_access_token(client_id, client_secret, refresh_token))
# https://<base_url>/api/v2/<account_owner_name>/<app_link_name>/report/<report_link_name>


def get_report_data_quick_view(access_token):
    url = f"https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/Elektrikkalender/26172000006435245"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:  # success
        data = response.json()
        print(data)

        # save data to result.json
        with open("result.json", "w") as f:
            json.dump(data, f)

        print("Data saved to result.json")
    # elif response.status_code == 401:  # Unauthorized, token expired
    #     print("Access token expired, refreshing...")
    #     new_access_token = refresh_access_token(client_id, client_secret, refresh_token)
    #     if new_access_token:
    #         get_report_data(client_id, client_secret, refresh_token, new_access_token, app_link_name, report_link_name)
    #     else:
    #         print("Failed to refresh access token.")
    else:
        print(f"Error: {response.status_code}")


# curl "https://creator.zoho.com/api/v2/jason18/zylker-store/report/All_Orders/3888833000000114027"


def get_report_data_detail_view(access_token):
    url = f"https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/Elektrikkalender/26172000006435245"

    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:  # success
        data = response.json()
        print(data)

        # save data to result.json
        with open("result.json", "w") as f:
            json.dump(data, f)

        print("Data saved to elektrik_detail_view.json")
    # elif response.status_code == 401:  # Unauthorized, token expired
    #     print("Access token expired, refreshing...")
    #     new_access_token = refresh_access_token(client_id, client_secret, refresh_token)
    #     if new_access_token:
    #         get_report_data(client_id, client_secret, refresh_token, new_access_token, app_link_name, report_link_name)
    #     else:
    #         print("Failed to refresh access token.")
    else:
        print(f"Error: {response.status_code}")


def get_report_data_quick_view_vertrieb(access_token):
    url = f"https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/Privatkunden1"
    params = {"Vertriebler": "26172000006250182"}
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:  # success
        data = response.json()
        print(data)

        # save data to result.json
        with open("result2.json", "w") as f:
            json.dump(data, f)

        print("Data saved to elektrik_detail_view.json")
    # elif response.status_code == 401:  # Unauthorized, token expired
    #     print("Access token expired, refreshing...")
    #     new_access_token = refresh_access_token(client_id, client_secret, refresh_token)
    #     if new_access_token:
    #         get_report_data(client_id, client_secret, refresh_token, new_access_token, app_link_name, report_link_name)
    #     else:
    #         print("Failed to refresh access token.")
    else:
        print(f"Error: {response.status_code}")


def fetch_filtered_data(access_token):
    # API endpoint
    url = "https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/Privatkunden1"

    # replace 'your_auth_token' with your actual auth token
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }

    # Criteria to filter by 'Vertriebler' field
    params = {
        # 'criteria': 'Vertriebler.ID == 26172000006250182',
    }

    # Sending GET request
    response = requests.get(url, headers=headers, params=params)

    # Checking the response status code
    if response.status_code == 200:
        # Convert the response to JSON
        data = response.json()
        with open("result2.json", "w") as f:
            json.dump(data, f)

    else:
        print(f"Failed to fetch data, status code: {response.status_code}")


print(access_token)


def fetch_vertriebler_list_IDs(access_token):
    # API endpoint
    url = "https://creator.zoho.eu/api/v2/thomasgroebckmann/juno-kleinanlagen-portal/report/Privatkunden1"

    # replace 'your_auth_token' with your actual auth token
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
    }

    # Define an empty set to store unique Vertriebler data
    vertriebler_set = set()

    # Specify the number of records to fetch per request
    limit = 200
    start_index = 0

    while True:
        # Get a batch of records
        params = {
            "from": start_index,
            "limit": limit,
        }
        response = requests.get(url, headers=headers, params=params)

        # Check the response status code
        if response.status_code != 200:
            print(f"Failed to fetch data, status code: {response.status_code}")
            break

        # Convert the response to JSON
        data = json.loads(response.text)

        # If no more data, exit the loop
        if not data["data"]:
            break

        # Extract Vertriebler data and add to the set
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
    print(json.dumps(vertriebler_list, indent=4))


def refresh_access_token(client_id, client_secret, refresh_token):
    url = f"https://accounts.zoho.eu/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token"

    response = requests.post(url)

    if response.status_code == 200:  # success
        data = response.json()
        print(data)
        new_access_token = data.get("access_token")
        print("Access token refreshed.", new_access_token)
        return new_access_token
    else:
        print(f"Error refreshing token: {response.status_code}")


fetch_vertriebler_list_IDs(access_token)
