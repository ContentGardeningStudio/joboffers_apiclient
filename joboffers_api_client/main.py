import requests


def get_offers(api_url: str, auth_key: str, department_code: str, paginate_max: int):
    headers = {"Authorization": f"Basic {auth_key}", "Connection": "close"}

    for i in range(1, paginate_max + 1):
        print(f"Get job offers from the results page #{i}")
        body = {
            "department_code": department_code,
            "page": i,
        }
        resp = requests.post(api_url, data=body, headers=headers)

        offers = resp.json()
        return offers
