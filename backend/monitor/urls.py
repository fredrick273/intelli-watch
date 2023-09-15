from django.urls import path
from . import views




urlpatterns = [
    path('report/<int:id>/',views.report),
    path('viewreport/<int:id>/',views.viewreport),
]