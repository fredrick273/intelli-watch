from django.urls import path
from . import views




urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path('report/<int:id>/',views.report,name="report"),
    path('viewreport/<int:id>/',views.viewreport,name='system_report'),
    path('newsystem/',views.newsystem,name='newsys'),
    path('showhistory/',views.multisystem,name='multisystem'),
    path('showhistory/<int:id>/',views.showhistory,name='history'),
    path('sysdatainstance/<int:id>/',views.showhistorydata,name='historydata'),
    
]