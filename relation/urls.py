from django.urls import path
from . import views

urlpatterns = [
    path('plus_and_minus_modulo/', views.RelationshipViews.plus_and_minus_modulo_views, name='plus_and_minus_modulo'),
    path('plus_and_minus_modulo/compute/', views.RelationshipViews.plus_and_minus_modulo_compute, name='plus_and_minus_modulo_compute'),
    path('multiple_modulo/', views.RelationshipViews.multiple_modulo_views, name='multiple_modulo'),
    path('multiple_modulo/compute/', views.RelationshipViews.multiple_modulo_compute, name='multiple_modulo_compute'),
    path('exponential_modulo/', views.RelationshipViews.exponential_modulo_views, name='exponential_modulo'),
    path('exponential_modulo/compute/', views.RelationshipViews.exponential_modulo_compute, name='exponential_modulo_compute'),
    path('check_the_properties_of_the_relationship/', views.RelationshipViews.check_the_properties_of_the_relationship_views, name='check_the_properties_of_the_relationship'),
    path('check_the_properties_of_the_relationship/compute/', views.RelationshipViews.check_the_properties_of_the_relationship_compute, name='check_the_properties_of_the_relationship_compute'),
    path('create_hasse_diagram/', views.RelationshipViews.create_hasse_diagram_views, name='create_hasse_diagram'),
    path('create_hasse_diagram/compute', views.RelationshipViews.create_hasse_diagram_compute, name='create_hasse_diagram_compute'),
]