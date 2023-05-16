from django.urls import path

from .views import index, by_rubric, BbDetailView, BbEditView, BbAddView, BbDeleteView #, BbCreateView, add_and_save


app_name = 'bboard'

urlpatterns = [
    path('confirm_delete/<int:pk>/', BbDeleteView.as_view(), name='confirm_delete'),
    path('correct/<int:pk>/', BbEditView.as_view(), name='correct'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/', BbAddView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
]
