# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.qrcode import views

urlpatterns = [

    # The home page
    path('qrcode_detail/<int:id>/', views.qrcode_detail,name='qrcode_detail'),
    path('add_qrcode/<int:visitor_id>/', views.add_qrcode,name='add_qrcode'),
    path('', views.index, name='index'),    
    re_path(r'^.*\.*', views.index, name='index')

]
