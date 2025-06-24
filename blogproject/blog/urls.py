from django.contrib import admin
from django.urls import path
from . import views  # if you have views in the project root or adjust the import to the correct app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  # this will handle the root URL
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('tag/<int:tag_id>/', views.posts_by_tag, name='posts_by_tag'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('ajax/delete_post/', views.ajax_delete_post, name='ajax_delete_post'),
    path('ajax/edit_post/', views.ajax_edit_post, name='ajax_edit_post'),

]


