import os
from django.shortcuts import render,get_object_or_404,redirect
from django.conf import settings
from .models import Visitors,QRcodes,AccessRecords

from io import BytesIO
import qrcode
import hashlib
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import forms

def index(request):
    if request.method == 'POST':
        search = request.POST['search']
        data = Visitors.objects.filter(phone__icontains=search)
    else:
        data = Visitors.objects.order_by('-created_at')[:50]
    
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

@api_view(['POST'])
def scan_qrcode(request):
    sha1 = request.data
    qrcode = QRcodes.objects.filter(qrstr=sha1['qrcode'], enable=True)
    if len(qrcode) == 1:
        access_detail = AccessRecords()
        access_detail.qrcode = qrcode[0]
        access_detail.save()
    return Response("Done")

def access_detail(request):
    data = AccessRecords.objects.order_by('-created_at')[:50]
    return render(request,'qrcode/access_detail.html',{'rows':data})

def new_visitor(request):

    if request.method == 'POST':
        visitor_form = forms.NewVisitorForm(request.POST)
        message = ""
        if visitor_form.is_valid():
            firstname = visitor_form.cleaned_data.get('firstname')
            lastname = visitor_form.cleaned_data.get('lastname')
            phone = visitor_form.cleaned_data.get('phone')
            email = visitor_form.cleaned_data.get('email')
            gender = visitor_form.cleaned_data.get('gender')
            notes = visitor_form.cleaned_data.get('notes')

            
            same_name_user = Visitors.objects.filter(firstname=firstname,lastname=lastname)
            if same_name_user:
                message = 'Visitor existed'
                return render(request, 'qrcode/new-visitor.html', locals())
            if email:
                same_email_user = Visitors.objects.filter(email=email)
                if same_email_user:
                    message = 'Email existed'
                    return render(request, 'qrcode/new-visitor.html', locals())
            same_phone = Visitors.objects.filter(phone = phone)
            if same_phone:
                message = 'Phone existed'
                return render(request, 'qrcode/new-visitor.html', locals())

            new_visitor = Visitors()
            new_visitor.firstname = firstname
            new_visitor.lastname = lastname
            new_visitor.gender = gender
            new_visitor.phone = phone
            new_visitor.email = email
            new_visitor.notes = notes          
            new_visitor.save()

            return redirect('/qrcode/')
        else:
            return render(request, 'qrcode/new-visitor.html', locals())
    visitor_form = forms.NewVisitorForm()
    return render(request, 'qrcode/new-visitor.html', locals())