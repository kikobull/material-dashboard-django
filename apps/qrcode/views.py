import os
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from .models import Visitors,QRcodes

from io import BytesIO
import qrcode
import hashlib
import datetime

def index(request):
    data = Visitors.objects.all()
    return render(request,'qrcode/visitor-tables.html',{'rows':data})

def qrcode_detail(request,id):
    data = QRcodes.objects.filter(visitor_id=id)
    return render(request,'qrcode/qrcode-tables.html',{'rows':data,'visitor_id':id})

def add_qrcode(request,visitor_id):
    qrstr = str(visitor_id) + "-" + str(datetime.datetime.now())
    hash_object = hashlib.sha1(qrstr.encode())
    hex_dig = hash_object.hexdigest()
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(hex_dig)
    qr.make(fit=True)
    

    # Convert the image to a byte string
    img_bytes = BytesIO()
    #qr_img.save(img_bytes, format='PNG')
    img_byte_str = img_bytes.getvalue()

    img = qr.make_image(fill_color='black', back_color='white')
    img.save(os.path.join(settings.PDF_ROOT,'qrcode'+qrstr+'.png'))

    new_qrcode = QRcodes()
    new_qrcode.qrcode = img_byte_str
    new_qrcode.qrstr = hex_dig
    visitor = Visitors.objects.get(id=visitor_id)
    new_qrcode.visitor = visitor
   
    new_qrcode.save()
   
    return qrcode_detail(request,visitor_id)