from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages

from .base_views import basic_view
from .services import get_context_for_requestor, get_context_for_requestors, take_action_on_requestor


@login_required
@basic_view(template='pisma/base_requestor.html')
def requestor(request: HttpRequest, node_id: str, real_node_id: str, requestor_id: str):
    """
    Single requestor view
    """
    return get_context_for_requestor(node_id, real_node_id, requestor_id)


@login_required
@basic_view(template='pisma/base_requestors.html')
def requestors(request: HttpRequest, node_id: str, real_node_id: str=None):
    """
    Requestors list view
    """
    return get_context_for_requestors(node_id, real_node_id)


@login_required
def requestor_action(request: HttpRequest, node_id: str, real_node_id: str, requestor_id: str):
    """
    Taking action on requestor: stop or interrupt
    """
    if 'interrupt' in request.POST:
        action = 'interrupt'
    else:
        action = 'stop'

    try:
        status = take_action_on_requestor(node_id, real_node_id, requestor_id, action)
        messages.success(request, status)
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('pisma:requestor', args=(node_id, real_node_id, requestor_id,)))

    if action == 'interrupt':
        return HttpResponseRedirect(reverse('pisma:requestor', args=(node_id, real_node_id, requestor_id,)))
    else:
        return HttpResponseRedirect(reverse('pisma:requestors_real', args=(node_id, real_node_id,)))