from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages

from .services import *


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
