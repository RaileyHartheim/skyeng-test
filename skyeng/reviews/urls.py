from django.urls import path

from . import views

app_name = 'reviews'


urlpatterns = [
    path('', views.index, name='index'),
    path('files_list', views.get_files_list, name='files_list'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('files/<int:file_id>/', views.get_file_detail, name='file_detail'),
    path('file/<int:file_id>/edit/', views.edit_file, name='edit_file'),
    path('file/<int:file_id>/delete/', views.delete_file, name='delete_file')
]
