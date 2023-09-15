from django.urls import path
from . import views




urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    # path('report/<int:id>/',views.report,name="report"),
    path('viewreport/<int:id>/',views.viewreport,name='system_report'),
    path('newsystem/',views.newsystem,name='newsys'),

    path('showhistory/',views.multisystem,name='multisystem'),
    path('showhistory/<int:id>/',views.showhistory,name='history'),
    path('showhistory/instance/<int:id>/',views.showhistorydata,name='historydata'),

    path('showall/process/<int:id>',views.showallprocesses,name='all_process'),
    path('showall/network/<int:id>',views.showallnetwork,name='all_network'),
    path('showall/installed/<int:id>',views.showallinstalled,name='all_installed')
    
]