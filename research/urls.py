from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('re_home/',views.research_home),
    path('re_login/',views.research_login),
    path('re_signup/',views.research_signup),
    path('re_logout/',views.research_logout),
    path('re_pat_p/',views.research_patient_pre),
    path('do_pat_p/',views.research_donor_pre),
    path('get_input/<int:id>/<str:table_name>/',views.get_input),

    ]