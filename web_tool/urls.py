from django.contrib import admin
from django.urls import path
from . import views #匯入你的 web_tool/view.py

urlpatterns = [
    path('', views.web),
    path('read_table/', views.read_csv),
    path('get_png/', views.get_picture),
    path('<str:version>/<int:id>/', views.giv_web, name='giv_web'),
]