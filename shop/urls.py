from django.urls import path,re_path
from . import views
from django.contrib.auth.views import  (login,logout,password_reset,password_reset_done,password_reset_confirm,)
from django.contrib.auth import views as auth_views
#from .feeds import LatestProductFeed

app_name = 'shop'
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,  name='login'),
    path('logout/',auth_views.logout,name='logout'),
    #path('feed/',LatestProductFeed(),name='product_feed'),
    re_path(r'^password-change/$', views.change_password, name='change_password'),

    re_path('profile/edit/', views.edit, name='edit'),
    path('', views.dashboard, name='dashboard'),

#products
    re_path(r'^product_list/$', views.product_list, name='product_list'),
    re_path(r'^(?P<category_slug>[-\w]+)/$',views.product_list,name='product_list_by_category'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.product_detail,name='product_detail'),
    path('all/products/',views.allproducts,name='allproducts'),

]
