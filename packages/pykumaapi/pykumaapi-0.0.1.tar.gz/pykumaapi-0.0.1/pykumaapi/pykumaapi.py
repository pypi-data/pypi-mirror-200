import requests


def getevent(url:str, api_key_user:str, clusterID:str, sql:str, period_from:str, period_to:str):
    """
    pyipakuma have one function 'get_event()'
    You need get parameters:

    :param url:
    :param api_key_user:
    :param clusterID:
    :param sql:
    :param period_from:
    :param period_to: :
    """

    url_full = f'https://{url}:7223/api/v1'
    headers = {"Authorization": f"Bearer {api_key_user}"}
    json_ = {"clusterID": f"{clusterID}",
             "sql": f"{sql}",
             "period": {"from": f"{period_from}", "to": f"{period_to}"}
             }
    response = requests.post(f"{url_full}/events", json=json_, headers=headers, verify=False)
    json_response = response.json()

    return json_response
