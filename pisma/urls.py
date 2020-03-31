from django.urls import path

from . import views

app_name = 'pisma'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('node/<int:node_id>/', views.node, name='node'),
    path('node/<int:node_id>/requestors/', views.requestors, name='requestors'),
    path('node/<int:node_id>/requestors/<str:real_node_id>/', views.requestors, name='requestors_real'),
    path('node/<int:node_id>/requestors/<str:real_node_id>/<str:requestor_id>/', views.requestor, name='requestor'),

    path('node/<int:node_id>/agents/', views.agents, name='agents'),
    path('node/<int:node_id>/agents/<str:real_node_id>/<str:agent_id>', views.agent, name='agent'),
    # path('node/new', views.new_node, name='new_node'),
    # path('node/delete', views.delete_node, name='delete_node')
]
