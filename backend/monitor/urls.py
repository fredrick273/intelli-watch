from django.urls import path
from . import views




urlpatterns = [
    path("send/",views.receive),
    path('seedata/',views.seedata),
    path('report/<int:id>/',views.report),
    path('viewreport/<int:id>/',views.viewreport)
]