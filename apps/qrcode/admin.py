# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Visitors,QRcodes,AccessRecords
# Register your models here.
admin.site.register(Visitors)
admin.site.register(QRcodes)
admin.site.register(AccessRecords)