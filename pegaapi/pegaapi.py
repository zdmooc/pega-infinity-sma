import requests

# timeout for requests in seconds
TIMEOUT = 5


def nodes(url, login, password):
    print(url, login, password)
    data = requests.get('{}/prweb/api/v1/nodes'.format(url), auth=(login, password), timeout=TIMEOUT)
    return data


def requestors(url, login, password, node_id):
    print(url, login, password)
    data = requests.get('{}/prweb/api/v1/nodes/{}/requestors'.format(url, node_id), auth=(login, password),
                        timeout=TIMEOUT)
    return data
