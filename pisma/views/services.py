from typing import Dict, List

from pisma.models import PegaNode

import pegaapi
from pegaapi import PegaAPIException


def get_default_context(node_id: str = None) -> Dict:
    """
    Getting default context for every view.
    Contains all nodes from database and a separate node if node_id is passed
    """
    nodes: List[PegaNode] = PegaNode.objects.all()
    context = {'nodes': nodes}

    if node_id:
        for node in nodes:
            if node.id == node_id:
                context['node'] = node

    return context


def get_context_for_node(node_id: str) -> Dict:
    """
    Context for the node view
    """
    context = get_default_context(node_id)
    for node in context['nodes']:
        if node.id == node_id:
            context['node'] = node
            try:
                nodes_data = pegaapi.nodes(node.url, node.login, node.password)
            except Exception as e:
                raise PegaAPIException(str(e), str(node), 'nodes')

            nodes_data_json = nodes_data.json()
            cluster_members = []
            for result in nodes_data_json['data']['result']:
                for member in result['cluster_members']:
                    cluster_members.append(member)
                context['cluster_members'] = cluster_members

    return context


def get_context_for_requestor(node_id: str, real_node_id: str, requestor_id: str) -> Dict:
    """
    Context for the single requestor view
    """
    context = get_default_context(node_id)
    node: PegaNode = context['node']

    try:
        data = pegaapi.requestor(node.url, node.login, node.password, real_node_id, requestor_id)
        requestor_data = data.json()['data']['result'][0]['requestor_details']
        context['requestor'] = requestor_data
        context['real_node_id'] = real_node_id
    except Exception as e:
        raise PegaAPIException(str(e), str(node), 'requestors')

    return context


def take_action_on_requestor(node_id: str, real_node_id: str, requestor_id: str, action: str) -> str:
    """
    Taking action on requestor: stop or interupt
    """
    node: PegaNode = get_default_context(node_id)['node']
    try:
        data = pegaapi.requestor(node.url, node.login, node.password, real_node_id, requestor_id, action)
        return data.json()['data']['result'][0]['status']
    except Exception as e:
        raise PegaAPIException(str(e), str(node), 'requestors')


def get_context_for_requestors(node_id: str, real_node_id: str = None):
    """
    Context for the list of requestors view
    """
    context = get_default_context(node_id)
    node: PegaNode = context['node']

    try:
        nodes_data = pegaapi.nodes(node.url, node.login, node.password)
    except Exception as e:
        raise PegaAPIException(str(e), str(node), 'nodes')

    nodes_data_json = nodes_data.json()
    cluster_members = []
    for result in nodes_data_json['data']['result']:
        for member in result['cluster_members']:
            cluster_members.append(member)
        context['cluster_members'] = cluster_members

    if real_node_id:
        try:
            requestors_data = pegaapi.requestors(node.url, node.login, node.password, real_node_id)
        except Exception as e:
            raise PegaAPIException(str(e), str(node), 'requestors')

        requestors_data_json = requestors_data.json()
        requestors = []
        node_ids = []
        for result in requestors_data_json['data']['result']:
            node_ids.append(result['nodeId'])
            for requestor in result['requestors']:
                requestor['nodeId'] = result['nodeId']
                requestors.append(requestor)
        context['requestors'] = requestors
        context['node_ids'] = node_ids

        context['real_node_id'] = real_node_id

    return context


def get_context_for_agent(node_id: str, real_node_id: str, agent_id: str) -> Dict:
    """
        Context for the single agent view
    """
    context = get_default_context(node_id)
    node: PegaNode = context['node']

    try:
        data = pegaapi.agent(node.url, node.login, node.password, 'all', agent_id)
        agent_data = data.json()['data']['result'][0]['agent_info']
        context['agent'] = agent_data
        context['real_node_id'] = real_node_id
    except Exception as e:
        raise PegaAPIException(str(e), str(node), 'agents')

    return context


def take_action_on_agent(node_id: str, real_node_id: str, agent_id: str, action: str) -> str:
    """
    Taking action on agent: stop, start or restart
    """
    node: PegaNode = get_default_context(node_id)['node']
    try:
        data = pegaapi.agent(node.url, node.login, node.password, real_node_id, agent_id, action)
        return data.json()['data']['result'][0]['message']
    except Exception as e:
        raise PegaAPIException(str(e), str(node), 'agents')


def get_context_for_agents(node_id: str) -> Dict:
    """
    Context for the list of agents view
    """
    context = get_default_context(node_id)
    node: PegaNode = context['node']

    try:
        agents_data = pegaapi.agents(node.url, node.login, node.password, 'all')
    except Exception as e:
        raise PegaAPIException(str(e), str(node), 'agents')

    agents_data_json = agents_data.json()
    agents = []
    for result in agents_data_json['data']['result']:
        agent = result['agent_info']
        agent['agent_name'] = agent['agent_id'].split('|')[0]
        agent['agent_ruleset'] = agent['agent_id'].split('|')[1]
        # TODO: Pega magic
        if agent['agent_id'] != 'Refactor Copy/Move/Merge|Pega-RuleRefactoring':
            agents.append(result['agent_info'])
    context['agents'] = agents

    return context
