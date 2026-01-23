from django.urls import path
from . import views

urlpatterns = [
    path('truth_table/', views.PropositionalViews.create_truth_table_views, name='truth_table'),
    path('truth_table/compute/', views.PropositionalViews.create_truth_table_compute, name='truth_table_compute'),
    path('constant_true_constant_false/', views.PropositionalViews.constant_true_constant_false_views, name='constant_true_constant_false'),
    path('constant_true_constant_false/compute/', views.PropositionalViews.constant_true_constant_false_compute, name='constant_true_constant_false_compute'),
    path('check_variable/', views.PropositionalViews.check_variable_views, name='check_variable'),
    path('check_variable/compute/', views.PropositionalViews.check_variable_compute, name='check_variable_compute'),
    path('caculator_boolean_algebra/', views.Boolean_algebraViews.caculator_boolean_algebra_views, name='caculator_boolean_algebra'),
    path('caculator_boolean_algebra/compute/', views.Boolean_algebraViews.caculator_boolean_algebra_compute, name='caculator_boolean_algebra_compute'),
    path('check_boolean_algebra_properties/', views.Boolean_algebraViews.check_boolean_algebra_properties_views, name='check_boolean_algebra_properties'),
    path('check_boolean_algebra_properties/compute/', views.Boolean_algebraViews.check_boolean_algebra_properties_compute, name='check_boolean_algebra_properties_compute'),
    path('check_distributed_compensation/', views.Boolean_algebraViews.check_distributed_compensation_views, name='check_distributed_compensation'),
    path('check_distributed_compensation/compute/', views.Boolean_algebraViews.check_distributed_compensation_compute, name='check_distributed_compensation_compute'),
    path('atom/', views.Boolean_algebraViews.atom_views, name='atom'),
    path('atom/compute/', views.Boolean_algebraViews.atom_compute, name='atom_compute'),
    path('minterm/', views.Boolean_algebraViews.minterm_views, name="minterm"),
    path('minterm/compute/', views.Boolean_algebraViews.minterm_compute, name="minterm_compute"),
    path('maxterm/', views.Boolean_algebraViews.maxterm_views, name='maxterm'),
    path('maxterm/compute/', views.Boolean_algebraViews.maxterm_compute, name='maxterm_compute'),
    path('abbreviated_SOP/', views.Boolean_algebraViews.abbreviated_SOP_views, name='abbreviated_SOP'),
    path('abbreviated_SOP/compute', views.Boolean_algebraViews.abbreviated_SOP_compute, name='abbreviated_SOP_compute'),
    path('Karnaugh_chart/', views.Boolean_algebraViews.draw_Karnaugh_chart_views, name='draw_Karnaugh_chart'),
    path('Karnaugh_chart/compute/', views.Boolean_algebraViews.draw_Karnaugh_chart_compute, name='draw_Karnaugh_chart_compute'),
]