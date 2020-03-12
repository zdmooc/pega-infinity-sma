import rwhe as requests

# TODO: DSS?
# timeout for requests in seconds
TIMEOUT = 5


def nodes(url, login, password):
    data = requests.get('{}/prweb/api/v1/nodes'.format(url), auth=(login, password), timeout=TIMEOUT)
    return data


def requestors(url, login, password, node_id):
    data = requests.get('{}/prweb/api/v1/nodes/{}/requestors'.format(url, node_id), auth=(login, password),
                        timeout=TIMEOUT)
    return data


def requestor(url, login, password, node_id, requestor_id, action=None):
    if action == 'interrupt':
        data = requests.put('{}/prweb/api/v1/nodes/{}/requestors/{}/interrupt'.format(url, node_id, requestor_id),
                            auth=(login, password),
                            timeout=TIMEOUT)
    elif action == 'stop':
        data = requests.delete('{}/prweb/api/v1/nodes/{}/requestors/{}'.format(url, node_id, requestor_id),
                               auth=(login, password),
                               timeout=TIMEOUT)
    else:
        data = requests.get('{}/prweb/api/v1/nodes/{}/requestors/{}'.format(url, node_id, requestor_id),
                            auth=(login, password),
                            timeout=TIMEOUT)
    return data
