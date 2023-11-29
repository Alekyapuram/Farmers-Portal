from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from .forms import BuyerUserRegistrationForm
from .models import BuyerUserRegistrationModel, BuyerCropCartModels,BuyerTransactionModels,BlockChainTransactionModel
from sellers.models import FarmersCropsModels
from .utility.BlockChainImpl import Blockchain
from django.db.models import Sum
import random

blockchain = Blockchain()
# Create your views here.
def BuyerUserRegisterActions(request):
    if request.method == 'POST':
        form = BuyerUserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = BuyerUserRegistrationForm()
            return render(request, 'BuyerUserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = BuyerUserRegistrationForm()
    return render(request, 'BuyerUserRegistrations.html', {'form': form})
def BuyerUserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = BuyerUserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                cartin = checkCartCount(loginid)
                return render(request, 'buyers/BuyerUserHome.html', {'count':cartin})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'BuyerLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'BuyerLogin.html', {})
def BuyerUserHome(request):
    loginid = request.session['loginid']
    cartin = checkCartCount(loginid)
    return render(request, 'buyers/BuyerUserHome.html', {'count':cartin})

def BuyerSearchProductsForm(request):
    loginid = request.session['loginid']
    cartin = checkCartCount(loginid)
    return render(request,"buyers/BuyerSearchProducts.html",{'count':cartin})

def BuyerSearchCropsAction(request):
    if request.method=='POST':
        crpname = request.POST.get('cropname')
        search_data = FarmersCropsModels.objects.filter(cropname__icontains=crpname)
        loginid = request.session['loginid']
        cartin = checkCartCount(loginid)
        return render(request, 'buyers/BuyerSearchResults.html',{'data':search_data,'count':cartin})



def BuyerAddCropsToCart(request):
    crop_id = request.GET.get('cropid')
    crop = FarmersCropsModels.objects.get(id=crop_id)
    sellername = crop.sellername
    cropname = crop.cropname
    price = crop.price
    description = crop.description
    file = crop.file
    buyerUser = request.session['loginid']
    buyeremail = request.session['email']
    cartStatus = 'waiting'
    BuyerCropCartModels.objects.create(buyerusername=buyerUser,buyeruseremail=buyeremail,sellername=sellername,cropname=cropname, description=description, price=price, file=file,status=cartStatus)
    print("Seller name ",sellername)
    search_data = FarmersCropsModels.objects.filter(cropname__icontains=cropname)
    cartin = checkCartCount(buyerUser)
    print("Cart Count = ",cartin)
    loginid = request.session['loginid']
    cartin = checkCartCount(loginid)
    return render(request, 'buyers/BuyerSearchResults.html', {'data': search_data,'count':cartin})


def checkCartCount(buyername):
    cartin = BuyerCropCartModels.objects.filter(buyerusername=buyername,status='waiting').count()
    return cartin


def BuyyerCheckCartData(request):
    buyerName =request.GET.get('buyerUser')
    data = BuyerCropCartModels.objects.filter(buyerusername=buyerName, status='waiting')
    return render(request,"buyers/BuyerCheckInCart.html",{'data':data})

def BuyerDeleteanItemfromCart(request):
    cropid = request.GET.get('cropid')
    BuyerCropCartModels.objects.filter(id=cropid).delete()
    buyerName = request.session['loginid']
    cartin = checkCartCount(buyerName)
    data = BuyerCropCartModels.objects.filter(buyerusername=buyerName, status='waiting')
    return render(request, "buyers/BuyerCheckInCart.html", {'data': data,'count':cartin})

def startBlockChainProcess(request):
    blockchain = Blockchain()
    t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
    blockchain.new_block(12346)
    t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
    t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
    blockchain.new_block(12345)
    print("Genesis block: ", blockchain.chain)
    return HttpResponse("Block Chain Started")

def BuyerTotalAmountCheckOut(request):
    buyerName = request.GET.get('buyername')
    cartstatuc = 'waiting'
    total_price = BuyerCropCartModels.objects.filter(buyerusername=buyerName, status='waiting').aggregate(Sum('price'))
    total_price = total_price['price__sum']
    print('Total Price ',total_price)
    bank = ('SBI Bank','Union Bank','ICICI Bank','Axis Bank','Canara Bank','HDFC Bank','FDI Bank','Chase Bank')
    recipient = random.choice(bank)
    return render(request, 'buyers/BuyerInitiateTransactionForm.html',{'buyername':buyerName,'totaPrice':total_price,'bank':recipient})

def StartBlockChainTransaction(request):
    if request.method=='POST':
        ## Block Chain Data
        buyername = request.POST.get('buyername')
        totalamount = request.POST.get('totalamount')
        recipientnmae = request.POST.get('recipientnmae')

        #Transaction Data
        cardnumber = request.POST.get('cardnumber')
        nameoncard = request.POST.get('nameoncard')
        cvv = request.POST.get('cvv')
        cardexpiry = request.POST.get('cardexpiry')

        t1 = blockchain.new_transaction(buyername, recipientnmae, totalamount)
        proofId = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        blockchain.new_block(int(proofId))
        print("Genesis block: ", blockchain.chain)
        print("T1 is ",t1)
        currentTrnx = blockchain.chain[-1]
        previousTranx = blockchain.chain[-2]
        ### Current Tranasction Details
        c_transactions = currentTrnx.get('transactions')
        c_tnx_Dict = c_transactions[0]

        c_index = currentTrnx.get('index')
        c_timestamp = currentTrnx.get('timestamp')
        c_sender = c_tnx_Dict.get('sender')
        c_recipient = c_tnx_Dict.get('recipient')
        c_amount = c_tnx_Dict.get('amount')
        c_proof = currentTrnx.get('proof')
        c_previous_hash = currentTrnx.get('previous_hash')

        c_dict_rslt = {'c_index':c_index,'c_timestamp':c_timestamp,'c_sender':c_sender,'c_recipient':c_recipient,'c_amount':c_amount,'c_proof':c_proof,'c_previous_hash':c_previous_hash}

        # previous Transaction
        p_dict_rslt = {}
        p_transactions = previousTranx.get('transactions')
        if(len(p_transactions)!=0):
            p_tnx_Dict = p_transactions[0]

            p_index = previousTranx.get('index')
            p_timestamp = previousTranx.get('timestamp')
            p_sender = p_tnx_Dict.get('sender')
            p_recipient = p_tnx_Dict.get('recipient')
            p_amount = p_tnx_Dict.get('amount')
            p_proof = previousTranx.get('proof')
            p_previous_hash = previousTranx.get('previous_hash')

            BuyerTransactionModels.objects.create(buyername=buyername, totalamount=totalamount,recipientname=recipientnmae,cradnumber=cardnumber,nameoncard=nameoncard,cvv=cvv, cardexpiry=cardexpiry)
            p_dict_rslt = {'p_index': p_index, 'p_timestamp': p_timestamp, 'p_sender': p_sender, 'p_recipient': p_recipient, 'p_amount': p_amount, 'p_proof': p_proof, 'p_previous_hash': p_previous_hash}
            BlockChainTransactionModel.objects.create(c_index=c_index,c_timestamp=c_timestamp,c_sender=c_sender,c_recipient=c_recipient, c_amount=c_amount,c_proof=c_proof,c_previous_hash=c_previous_hash,p_index=p_index, p_timestamp=p_timestamp,p_sender=p_sender,p_recipient=p_recipient,p_amount=p_amount,p_proof=p_proof,p_previous_hash=p_previous_hash)
            buyer_name = request.session['loginid']
            print('buyername =',buyer_name)
            qs = BuyerCropCartModels.objects.filter(buyerusername=buyer_name).update(status='purchased')
        else:
            BuyerTransactionModels.objects.create(buyername=buyername, totalamount=totalamount,
                                                  recipientname=recipientnmae, cradnumber=cardnumber,
                                                  nameoncard=nameoncard, cvv=cvv, cardexpiry=cardexpiry)

            BlockChainTransactionModel.objects.create(c_index=c_index, c_timestamp=c_timestamp, c_sender=c_sender,
                                                      c_recipient=c_recipient, c_amount=c_amount, c_proof=c_proof,
                                                      c_previous_hash=c_previous_hash, p_index='p_index',
                                                      p_timestamp='p_timestamp', p_sender='p_sender',
                                                      p_recipient="p_recipient", p_amount="p_amount", p_proof="p_proof",
                                                      p_previous_hash="p_previous_hash")
            buyer_name = request.session['loginid']
            print('buyername =', buyer_name)
            qs = BuyerCropCartModels.objects.filter(buyerusername=buyer_name).update(status='purchased')
        return render(request, 'buyers/TransactionResults.html',{'c_dict_rslt':c_dict_rslt,'p_dict_rslt':p_dict_rslt})

def BuyerViewPurchasedDetails(request):
    buyer_name = request.session['loginid']
    cartin = checkCartCount(buyer_name)
    data = BuyerCropCartModels.objects.filter(buyerusername=buyer_name,status='purchased')
    return render(request, 'buyers/BuyersViewPurchasedData.html',{'data':data,'count':cartin})

def BuyerViewTransactinDetails(request):
    bd_name = request.session['loginid']
    print('buyer_name',bd_name)
    data = BuyerTransactionModels.objects.filter(buyername = ' '+bd_name)
    cartin = checkCartCount(bd_name)
    return render(request, 'buyers/BuyersViewTransactionDetails.html',{'data':data,'count':cartin})
