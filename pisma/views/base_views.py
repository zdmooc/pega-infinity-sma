import logging
from typing import Callable
from pisma.logger import PismaLogger

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib import messages

from .services import get_default_context, get_context_for_node

logger = PismaLogger(__name__)


def basic_view(template: str):
    """
    Decorator for basic view
    """

    def decorator(actual_view: Callable):
        def wrapper(request: HttpRequest, node_id: str = None, **kwargs):
            logger.debug(
                '[basic_view.decorator.wrapper] start. template: {}. actual_view: {}. request: {}. node_id: {}. kwargs: {}'.format(
                    template, actual_view, request, node_id, kwargs
                ),
                request=request
            )
            try:
                logger.info(
                    '[basic_view.decorator.wrapper] {} view accessed. request: {}'.format(actual_view.__name__, request),
                    request=request)
                if node_id:
                    context = actual_view(request, node_id, **kwargs)
                else:
                    context = actual_view(request, **kwargs)
            except Exception as e:
                logger.warning(
                    '[basic_view.decorator.wrapper] {} view execution exception: "{}"'.format(actual_view.__name__, e),
                    request=request)
                context = get_default_context(node_id)
                messages.error(request, e)

            logger.debug('[basic_view.decorator.wrapper] end', request=request)
            return render(request, template, context)

        return wrapper

    return decorator


def action_view(actual_action: Callable):
    """
    Decorator for action views
    """
    def wrapper(request: HttpRequest, *args, **kwargs):
        try:
            logger.info(
                '[action_view.wrapper] {} view accessed. request: {}, agrs: {}, kwargs: {}'.format(
                    actual_action.__name__, request, args, kwargs))
            result = actual_action(request, *args, **kwargs)
            return result
        except Exception as e:
            logger.warning('[action_view.wrapper] {} view execution exception: "{}"'.format(actual_action.__name__, e))

    return wrapper


@login_required
@basic_view(template='pisma/base_index.html')
def index(request: HttpRequest):
    """
    Home page
    """
    return get_default_context()


@login_required
@basic_view(template='pisma/base_node.html')
def node(request: HttpRequest, node_id: str):
    """
    Single node view
    """
    return get_context_for_node(node_id)


def login_view(request: HttpRequest):
    logger.info('[login_view] accessed. request: {}'.format(request))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('pisma:index'))
        messages.error(request, 'Invalid credentials')
        return render(request, 'pisma/login.html')

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('pisma:index'))

    return render(request, 'pisma/login.html')


def logout_view(request: HttpRequest):
    logger.info('[logout_view] accessed. request: {}'.format(request))
    logout(request)
    return HttpResponseRedirect(reverse('pisma:index'))
