from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('cases/', views.case_list, name='case_list'),
    path('cases/create/', views.case_create, name='case_create'),
    path('cases/pending/', views.pending_cases, name='pending_cases'),
    path('cases/search/', views.search_cases, name='search_cases'),  # Place search above the CIN route
    path('cases/<str:CIN>/', views.case_detail, name='case_detail'),
    path('cases/<str:CIN>/edit/', views.case_edit, name='case_edit'),
    path('cases/<str:CIN>/delete/', views.case_delete, name='case_delete'),
]
