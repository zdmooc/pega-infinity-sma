import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages

from pisma.logger import PismaLogger

from .base_views import basic_view, action_view
from .services import (
    get_context_for_requestor,
    get_context_for_requestors,
    take_action_on_requestor,
)

logger = PismaLogger(__name__)


@login_required
@basic_view(template="pisma/base_requestor.html")
def requestor(request: HttpRequest, node_id: str, real_node_id: str, requestor_id: str):
    """
    Single requestor view
    """
    return get_context_for_requestor(node_id, real_node_id, requestor_id)


@login_required
@basic_view(template="pisma/base_requestors.html")
def requestors(request: HttpRequest, node_id: str, real_node_id: str = None):
    """
    Requestors list view
    """
    return get_context_for_requestors(node_id, real_node_id)


@login_required
@action_view
def requestor_action(
    request: HttpRequest, node_id: str, real_node_id: str, requestor_id: str
):
    """
    Taking action on requestor: stop or interrupt
    """
    if "interrupt" in request.POST:
        action = "interrupt"
    else:
        action = "stop"

    try:
        status = take_action_on_requestor(node_id, real_node_id, requestor_id, action)
        logger.info(
            "[requestor_action] requestor {} was {}ed".format(requestor_id, action),
            request=request,
        )
        messages.success(request, status)
    except Exception as e:
        logger.warning(
            '[requestor_action] view execution exception: "{}"'.format(e),
            request=request,
        )
        messages.error(request, e)
        return HttpResponseRedirect(
            reverse(
                "pisma:requestor",
                args=(
                    node_id,
                    real_node_id,
                    requestor_id,
                ),
            )
        )

    if action == "interrupt":
        return HttpResponseRedirect(
            reverse(
                "pisma:requestor",
                args=(
                    node_id,
                    real_node_id,
                    requestor_id,
                ),
            )
        )
    return HttpResponseRedirect(
        reverse(
            "pisma:requestors_real",
            args=(
                node_id,
                real_node_id,
            ),
        )
    )
