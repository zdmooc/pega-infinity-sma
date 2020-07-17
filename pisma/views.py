from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages

from .views_services import *


def basic_view(template: str):
    """
    Decorator for basic view
    """

    def decorator(actual_view):
        def wrapper(request: HttpRequest, node_id: str, **kwargs):
            try:
                context = actual_view(request, node_id, **kwargs)
            except Exception as e:
                context = get_default_context(node_id)
                messages.error(request, e)

            return render(request, template, context)

        return wrapper

    return decorator


@login_required
def index(request: HttpRequest):
    """
    Home page
    """
    return render(request, 'pisma/base_index.html', get_default_context())


@login_required
@basic_view(template='pisma/base_node.html')
def node(request: HttpRequest, node_id: str):
    """
    Single node view
    """
    return get_context_for_node(node_id)


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
@basic_view(template='pisma/base_agent.html')
def agent(request: HttpRequest, node_id: str, real_node_id: str, agent_id: str):
    """
    Single agent view
    """
    return get_context_for_agent(node_id, real_node_id, agent_id)


@login_required
@basic_view(template='pisma/base_agents.html')
def agents(request: HttpRequest, node_id: str):
    """
    Agents list view
    """
    return get_context_for_agents(node_id)


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


@login_required
def agent_action(request: HttpRequest, node_id: str, real_node_id: str, agent_id: str ):
    """
    Taking action on agent: start, restart or stop
    """
    if 'start' in request.POST:
        action = 'start'
    elif 'restart' in request.POST:
        action = 'restart'
    elif 'stop' in request.POST:
        action = 'stop'
    else:
        messages.error(request, 'Invalid action')
        return HttpResponseRedirect(reverse('pisma:agent', args=(node_id, 'all', agent_id,)))

    try:
        status = take_action_on_agent(node_id, real_node_id, agent_id, action)
        messages.success(request, status)
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('pisma:agent', args=(node_id, 'all', agent_id,)))

    return HttpResponseRedirect(reverse('pisma:agent', args=(node_id, 'all', agent_id,)))


def login_view(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # TODO: redirect to 'next' query parameter
            return HttpResponseRedirect(reverse('pisma:index'))
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'pisma/login.html')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('pisma:index'))
        else:
            return render(request, 'pisma/login.html')


def logout_view(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse('pisma:index'))
