from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('donor_home/',views.donor_home),
    path('donor_login/',views.donor_login),
    path('donor_signup/',views.donor_signup),
    path('donor_logout/',views.donor_logout),
    path('donor_reg/',views.donor_registration),
    path('donor_organ_d/',views.donor_organ_details),
    path('eye_reg/',views.eye_reg),
    path('heart_reg/',views.heart_reg),
    path('liver_reg/',views.liver_reg),
    path('lungs_reg/',views.lungs_reg),
    path('kidney_reg/',views.kidney_reg),
    path('donor_agree/',views.donor_agree),
    path('donor_og_details/',views.donor_og_details),
    path('agree/<int:id>/<str:table_name>/',views.agree),
    path('ignore/<int:id>/<str:table_name>/',views.ignore),
    ]