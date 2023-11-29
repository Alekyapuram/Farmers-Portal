from django.db import models

# Create your models here.
class SellerUserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'SellerRegistrations'

class FarmersCropDataModels(models.Model):
    sellername = models.CharField(max_length=100)
    selleremail = models.CharField(max_length=100)
    cropname = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=100000)
    file = models.FileField(upload_to='files/')
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = "Farmerscroptable"

class FarmersCropsModels(models.Model):
    sellername = models.CharField(max_length=100)
    selleremail = models.CharField(max_length=100)
    cropname = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=100000)
    file = models.FileField(upload_to='files/')
    cdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = "FarmersCrops"

