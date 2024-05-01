from django.shortcuts import render,redirect
from .forms import checkForm
from .models import check
from nayamain import FUN
import datetime
# Create your views here.
front_ver={}
date=0
amount=0
ac=0
leaf_no=0
account=0
phone=0
bank=''
ifsc=''
payee_name=''
payee_amt=''
name=''
back_ver={}
cur_id=0

def index(request):
    return render(request,'index.html')

def main(request):
    if request.method == "POST":
        form = checkForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get("check_img")
            img2=form.cleaned_data.get("back_check_img")
            obj = check.objects.create(check_img = img,back_check_img=img2)
            obj.save()
            global cur_id
            cur_id=obj.id
            str1=obj.check_img.url
            str2=obj.back_check_img.url
            print(str1,str2)
            global front_ver,date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no,back_ver,account,phone,name
            front_ver,date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no,back_ver,account,phone,name=FUN(str1,str2)
            return redirect('upload')
    else:
        form = checkForm()
    return render(request, "main.html",{'form':form})

def upload(request):
    t=str(date)
    yyyy=t[4:]
    mm=t[2:4]
    dd=t[0:2]
    date1 = datetime.date(int(yyyy), int(mm), int(dd))
    print(date1)
    print(front_ver,date,amount,bank,ifsc,payee_name,payee_amt,ac,leaf_no,back_ver,account,phone,name)
    if request.method == 'GET':
        checks=check.objects.get(id=cur_id)
        if(front_ver['valid']==1 and back_ver['valid']==1):
            return render(request,'upload.html',{'checks':checks,'Valid':1,'amount':amount,'ac':ac,'leaf_no':leaf_no,'account':account,'phone':phone,'bank':bank,'ifsc':ifsc,'payee_name':payee_name,'payee_amt':payee_amt,'name':name,'date':date1})
        else:
            return render(request,'upload.html',{'checks':checks,'Valid':0,'amount':amount,'ac':ac,'leaf_no':leaf_no,'account':account,'phone':phone,'bank':bank,'ifsc':ifsc,'payee_name':payee_name,'payee_amt':payee_amt,'name':name,'date':date1})

