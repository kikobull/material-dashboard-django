from django.db import models

class Visitors(models.Model):    
    GenderChoice = (
        ("M","Male"),
        ("F","Female"),
        )
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=50)
    gender = models.CharField(max_length=2, choices=GenderChoice)
    notes = models.CharField(max_length=400,null=True)
    phone = models.CharField(max_length=20)
    photo = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)

class QRcodes(models.Model):
    visitor = models.ForeignKey(Visitors, on_delete=models.CASCADE)
    qrcode = models.BinaryField()
    qrstr = models.CharField(max_length=400,null=True)
    expiry_dt = models.DateTimeField(null=True)
    enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AccessRecords(models.Model):
    qrcode = models.ForeignKey(QRcodes,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


