from django.urls import path
from . import views

urlpatterns = [
    path('check_injective/', views.CountingView.check_injective_views, name='check_injective'),
    path('check_injective/compute/', views.CountingView.check_injective_compute, name='check_injective_compute'),
    path('check_surjective/', views.CountingView.check_surjective_views, name='check_surjective'),
    path('check_surjective/compute/', views.CountingView.check_surjective_compute, name='check_surjective_compute'),
    path('check_bijective/', views.CountingView.check_bijective_views, name='check_bijective'),
    path('check_bijective/compute/', views.CountingView.check_bijective_compute, name='check_bijective_compute'),
    path('reverse_mapping/', views.CountingView.reverse_mapping_views, name='reverse_mapping'),
    path('reverse_mapping/compute/', views.CountingView.reverse_mapping_compute, name='reverse_mapping_compute'),
    path('pigeonhole/', views.PigeonholeView.pigeonhole_views, name='pigeonhole'),
    path('pigeonhole/compute/', views.PigeonholeView.pigeonhole_compute, name='pigeonhole_compute'),
]
