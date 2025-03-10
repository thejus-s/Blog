from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path("<slug:slug>",views.blog_details,name='blogdetails'),
    path("category/<slug:slug>",views.cat,name="category"),
    path("<slug:slug>/addcomment/",views.addcomment,name="addcomment"),
    path('signup/',views.userRegister,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('addblog/',views.addBlog,name="addblog"),
    path('yourpost/',views.userpost,name='userpost'),
    path('manage/<slug:slug>',views.userManagePost,name="umanagepost"),
    path("deletecomment/<int:cid>",views.deleteComment,name='deletecomment'),
    path("deletepost/<int:pid>",views.deletePost,name='deletepost'),
    path('editpost/<slug:slug>',views.editPost,name='editpost')
]