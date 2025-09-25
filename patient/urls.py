from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('patient_home/',views.patient_home),
    path('patient_login/',views.patient_login),
    path('patient_signup/',views.patient_signup),
    path('patient_logout/',views.patient_logout),
    path('patient_eye_reg/',views.eye_details),
    path('patient_heart_reg/',views.heart_details),
    path('patient_liver_reg/',views.liver_details),
    path('patient_lungs_reg/',views.lungs_details),
    path('patient_kidney_reg/',views.kidney_details),
    path('pat_og_de/',views.pat_de),
    path('pat_agree/',views.pat_agreement),
    path('pa_agree/<int:id>/<str:table_>/',views.pa_agree),
    path('pa_ignore/<int:id>/<str:table_>/',views.pat_ignore),



    ]