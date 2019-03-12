from django.conf.urls import url
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

#
urlpatterns = [
    url(r'^$', views.index, name="index"),

    #浏览信息
    url(r'^check(?P<pIndex>[0-9]+)$', views.check, name="check"),

    #图片上传
    #加载添加表单
    url(r'^ul$', views.ul, name="ul"),
    #执行添加
    url(r'^upload$', views.upload, name="upload"),

    #删除信息
    url(r'^delete/(?P<pid>[0-9]+)$', views.delete, name="delete"),

    #编辑信息
    #加载编辑表单
    url(r'^edit/(?P<pid>[0-9]+)$', views.edit, name="edit"),
    #执行修改
    url(r'^update/$', views.update, name="update"),
]

urlpatterns += staticfiles_urlpatterns()
