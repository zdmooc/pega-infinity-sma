import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages

from pisma.logger import PismaLogger

from .base_views import basic_view, action_view
from .services import (
    get_context_for_agent,
    get_context_for_agents,
    take_action_on_agent,
)

logger = PismaLogger(__name__)


@login_required
@basic_view(template="pisma/base_agent.html")
def agent(request: HttpRequest, node_id: str, real_node_id: str, agent_id: str):
    """
    Single agent view
    """
    return get_context_for_agent(node_id, real_node_id, agent_id)


@login_required
@basic_view(template="pisma/base_agents.html")
def agents(request: HttpRequest, node_id: str):
    """
    Agents list view
    """
    return get_context_for_agents(node_id)


@login_required
@action_view
def agent_action(request: HttpRequest, node_id: str, real_node_id: str, agent_id: str):
    """
    Taking action on agent: start, restart or stop
    """
    if "start" in request.POST:
        action = "start"
    elif "restart" in request.POST:
        action = "restart"
    elif "stop" in request.POST:
        action = "stop"
    else:
        messages.error(request, "Invalid action")
        return HttpResponseRedirect(
            reverse(
                "pisma:agent",
                args=(
                    node_id,
                    "all",
                    agent_id,
                ),
            )
        )

    try:
        status = take_action_on_agent(node_id, real_node_id, agent_id, action)
        logger.info(
            "[agent_action] agent {} was {}ed".format(agent_id, action), request=request
        )
        messages.success(request, status)
    except Exception as e:
        logger.warning(
            '[agent_action] view execution exception: "{}"'.format(e), request=request
        )
        messages.error(request, e)
        return HttpResponseRedirect(
            reverse(
                "pisma:agent",
                args=(
                    node_id,
                    "all",
                    agent_id,
                ),
            )
        )

    return HttpResponseRedirect(
        reverse(
            "pisma:agent",
            args=(
                node_id,
                "all",
                agent_id,
            ),
        )
    )
