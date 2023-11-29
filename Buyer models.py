from django.db import models

# Create your models here.
class BuyerUserRegistrationModel(models.Model):
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
        db_table = 'BuyersRegistrations'



class BuyerCropCartModels(models.Model):
    buyerusername = models.CharField(max_length=100)
    buyeruseremail = models.CharField(max_length=100)
    sellername = models.CharField(max_length=100)
    cropname = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)
    price = models.FloatField()
    file = models.FileField(upload_to='files/')
    cdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.buyerusername

    class Meta:
        db_table = "BuyerCartTable"


class BuyerTransactionModels(models.Model):
    buyername = models.CharField(max_length=100)
    totalamount = models.FloatField()
    recipientname = models.CharField(max_length=100)
    cradnumber = models.IntegerField()
    nameoncard = models.CharField(max_length=100)
    cvv = models.IntegerField()
    cardexpiry = models.CharField(max_length=200)
    trnx_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #return self.id
        return self.buyername

    class Meta:
        db_table = "BuyerTransactionTable"

class BlockChainTransactionModel(models.Model):
    c_index = models.CharField(max_length=100)
    c_timestamp = models.CharField(max_length=100)
    c_sender = models.CharField(max_length=100)
    c_recipient = models.CharField(max_length=100)
    c_amount = models.CharField(max_length=100)
    c_proof = models.CharField(max_length=100)
    c_previous_hash = models.CharField(max_length=100)
    p_index = models.CharField(max_length=100)
    p_timestamp = models.CharField(max_length=100)
    p_sender = models.CharField(max_length=100)
    p_recipient = models.CharField(max_length=100)
    p_amount = models.CharField(max_length=100)
    p_proof = models.CharField(max_length=100)
    p_previous_hash = models.CharField(max_length=100)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "BlockChainTransactiontable"

