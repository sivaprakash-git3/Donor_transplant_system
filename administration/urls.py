from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('admin_home/',views.admin_home),
    path('admin_login/',views.admin_login),
    path('admin_logout/',views.admin_logout),
    path('patient_stats/',views.patient_stats),
    path('donor_stats/',views.donor_stats),
    path('d_match/',views.don_match),
    path('pa_per/',views.patient_per),
    path('don_per/',views.donor_per),
    path('organ_u/',views.organ_users),
    path('donar_m/<int:id>/<str:table_>/',views.donor_match_prediction),
    path('d_con/<int:id>/<str:table_>/',views.donor_consent),

    ]