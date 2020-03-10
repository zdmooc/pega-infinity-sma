from django.shortcuts import render, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

from .models import PegaNode
import pegaapi


def default_index_context(node_id=None):
    nodes = get_list_or_404(PegaNode)
    context = {'nodes': nodes}

    if node_id:
        for node in nodes:
            if node.id == node_id:
                context['node'] = node

    return context


@login_required()
def index(request):
    return render(
        request,
        'pisma/base_index.html',
        default_index_context()
    )


@login_required()
def node(request, node_id):
    context = default_index_context()
    for node in context['nodes']:
        if node.id == node_id:
            context['node'] = node
            try:
                nodes_data = pegaapi.nodes(node.url, node.login, node.password)
            except Exception as e:
                messages.error(request, e)
                return render(request, 'pisma/base_node.html', context)

            nodes_data_json = nodes_data.json()
            cluster_members = []
            for result in nodes_data_json['data']['result']:
                for member in result['cluster_members']:
                    cluster_members.append(member)
                context['cluster_members'] = cluster_members

    return render(request, 'pisma/base_node.html', context)


@login_required()
def new_node(request):
    if request.method == 'POST':
        context = default_index_context()

        node = PegaNode()
        node.name = request.POST['name']
        node.url = request.POST['url']
        node.production_level = request.POST['production_level']

        try:
            user = User.objects.create_user(
                username='{}-{}'.format(request.POST['name'], request.POST['login']),
                first_name=request.POST['login'],
                password=request.POST['password']
            )
            user.save()

            node.user = user
            node.save()
        except Exception as e:
            user.delete()
            context['error_message'] = 'Node was not added. Error {}'.format(e)
            return render(request, 'pisma/new_node.html', context)

        context['success_message'] = 'Node {} was added'.format(node.name)

        return render(request, 'pisma/new_node.html', context)
    else:
        return render(request, 'pisma/new_node.html', default_index_context())


@login_required()
def delete_node(request):
    pass


@login_required()
def requestor(request, node_id, real_node_id, requestor_id, action=None):
    context = default_index_context(node_id=node_id)
    node = context['node']

    try:
        data = pegaapi.requestor(node.url, node.login, node.password, real_node_id, requestor_id, action)
    except Exception as e:
        messages.error(request, e)
        return render(request, 'pisma/base_requestor.html', context)

    if action == 'interrupt':
        messages.success(request, data.json()['data']['result'][0]['status'])
        data = pegaapi.requestor(node.url, node.login, node.password, real_node_id, requestor_id)
        requestor_data = data.json()['data']['result'][0]['requestor_details']
        context['requestor'] = requestor_data
        context['real_node_id'] = real_node_id

        return render(request, 'pisma/base_requestor.html', context)
    elif action == 'stop':
        messages.success(request, 'Requestor {} stopped on node {}'.format(requestor_id, real_node_id))

        try:
            nodes_data = pegaapi.nodes(node.url, node.login, node.password)
        except Exception as e:
            messages.error(request, e)
            return render(request, 'pisma/base_requestors.html', context)

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
                messages.error(request, e)
                return render(request, 'pisma/base_requestors.html', context)

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

        return render(request, 'pisma/base_requestors.html', context)
    else:
        requestor_data = data.json()['data']['result'][0]['requestor_details']
        context['requestor'] = requestor_data
        context['real_node_id'] = real_node_id

        return render(request, 'pisma/base_requestor.html', context)


@login_required()
def requestors(request, node_id, real_node_id=None):
    context = default_index_context(node_id)
    node = context['node']

    try:
        nodes_data = pegaapi.nodes(node.url, node.login, node.password)
    except Exception as e:
        messages.error(request, e)
        return render(request, 'pisma/base_requestors.html', context)

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
            messages.error(request, e)
            return render(request, 'pisma/base_requestors.html', context)

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

    return render(request, 'pisma/base_requestors.html', context)


def login_view(request):
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('pisma:index'))
