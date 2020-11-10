import os

from requests import Response

from config import AppConfig
import rwhe as requests

# timeout for requests in seconds
TIMEOUT = AppConfig.PISMA_PEGAAPI_TIMEOUT


def nodes(url: str, login: str, password: str) -> Response:
    data = requests.get(
        "{}/prweb/api/v1/nodes".format(url), auth=(login, password), timeout=TIMEOUT
    )
    return data


def requestors(url: str, login: str, password: str, node_id: str) -> Response:
    data = requests.get(
        "{}/prweb/api/v1/nodes/{}/requestors".format(url, node_id),
        auth=(login, password),
        timeout=TIMEOUT,
    )
    return data


def requestor(
    url: str,
    login: str,
    password: str,
    node_id: str,
    requestor_id: str,
    action: str = None,
) -> Response:
    if action == "interrupt":
        data = requests.put(
            "{}/prweb/api/v1/nodes/{}/requestors/{}/interrupt".format(
                url, node_id, requestor_id
            ),
            auth=(login, password),
            timeout=TIMEOUT,
        )
    elif action == "stop":
        data = requests.delete(
            "{}/prweb/api/v1/nodes/{}/requestors/{}".format(url, node_id, requestor_id),
            auth=(login, password),
            timeout=TIMEOUT,
        )
    else:
        data = requests.get(
            "{}/prweb/api/v1/nodes/{}/requestors/{}".format(url, node_id, requestor_id),
            auth=(login, password),
            timeout=TIMEOUT,
        )
    return data


def agents(url: str, login: str, password: str, node_id: str) -> Response:
    data = requests.get(
        "{}/prweb/api/v1/nodes/{}/agents".format(url, node_id),
        auth=(login, password),
        timeout=TIMEOUT,
    )
    return data


def agent(
    url: str, login: str, password: str, node_id: str, agent_id: str, action: str = None
) -> Response:
    if action == "start":
        data = requests.post(
            "{}/prweb/api/v1/nodes/{}/agents/{}".format(url, node_id, agent_id),
            auth=(login, password),
            timeout=TIMEOUT,
        )
    elif action == "restart":
        data = requests.put(
            "{}/prweb/api/v1/nodes/{}/agents/{}".format(url, node_id, agent_id),
            auth=(login, password),
            timeout=TIMEOUT,
        )
    elif action == "stop":
        data = requests.delete(
            "{}/prweb/api/v1/nodes/{}/agents/{}".format(url, node_id, agent_id),
            auth=(login, password),
            timeout=TIMEOUT,
        )
    else:
        data = requests.get(
            "{}/prweb/api/v1/nodes/{}/agents/{}".format(url, node_id, agent_id),
            auth=(login, password),
            timeout=TIMEOUT,
        )

    return data
