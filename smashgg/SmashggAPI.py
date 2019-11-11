import requests

def execute_api ( query, variables, api_token ) :
    """
    """

    url = 'https://api.smash.gg/gql/alpha'
    json = { 'query' : '%s' % query, 'variables' : '%s' % variables }
    headers = {'Authorization': 'Bearer %s' % api_token}

    res = requests.post(url=url, json=json, headers=headers).json()

    return res
