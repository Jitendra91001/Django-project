from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime
from django.db import connection
# Create your views here.
def home(req):

    cdata=category.objects.all().order_by('-id')[0:6]
    pdata=product.objects.all().order_by('-id')[0:6]
    print(pdata)

    return render(req,'user/index.html',{"data":cdata,"products":pdata})

def about(req):
    return render(req,'user/about.html')

def contactus(request):
    status=False
    if request.method=='POST':
        Name=request.POST.get("name","")
        Mobile=request.POST.get("mobile","")
        Email=request.POST.get("email","")
        Message=request.POST.get("msg","")
        res=contact(name=Name,contact=Mobile,email=Email,message=Message)
        res.save()
        status=True
        return HttpResponse("<script>alert('Thanks For Enquiry..');window.location.href='/user/contactus/'</script>")
    return render(request,'user/contactus.html',{'S':status})

def services(req):
    return render(req,'user/services.html')

def myorder(req):
    return render(req,'user/myorder.html')

def myprofile(request):
    mdata = profile.objects.all().order_by('-name')
    if request.session.get('userid'):

        #userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select * from user_profile")
        pro=cursor.fetchall()
    return render(request,'user/myprofile.html',{"jitendra":pro,"vivek":mdata})
def admin(req):
    return render(req,'/admin')

def prod(request):
    cdata=category.objects.all().order_by('-id')
    x=request.GET.get('abc')

    if x is not None:
        pdata=product.objects.filter(category=x)
    else:
        pdata = product.objects.all().order_by('-id')

    return render(request,'user/products.html',{"cat":cdata,"products":pdata})

def signup(request):
    status=False
    if request.method=='POST':
        name=request.POST.get("name","")
        DOB=request.POST.get("dob","")
        Mobile=request.POST.get("mobile","")
        Email=request.POST.get("email","")
        Password=request.POST.get("passwd","")
        ProfilePhoto=request.FILES['myfile']
        Address=request.POST.get("address","")
        d=profile.objects.filter(email=Email)

        if d.count()>0:
            return HttpResponse("<script>alert('You are already registered..');window.location.href='/user/signup/'</script>")
        else:
            res=profile(name=name,dob=DOB,mobile=Mobile,email=Email,passwd=Password,myfile=ProfilePhoto,address=Address)
            res.save()
            return HttpResponse("<script>alert('You are registered successfully..');window.location.href='/user/signup/'</script>")

        #return HttpResponse("<script>alert('Thanks For SignUp..');window.location.href='/user/signup/';</script>")
    return render(request,'user/signup.html')

def signin(request):
    if request.method=='POST':

        uname=request.POST.get("uname")
        passwd=request.POST.get("passwd")
        checkuser=profile.objects.filter(email=uname,passwd=passwd)
        if(checkuser):
            request.session['userid']=uname
            return HttpResponse("<script>alert('Logged In Successfully');window.location.href='/user/signin';</script>")

        else:
            return HttpResponse("<script>alert('UserID or Password is Incorrect');window.location.href='/user/signin';</script>")
    return render(request,'user/signin.html')

def viewdetails(request):
    a=request.GET.get('msg')
    data=product.objects.filter(id=a)

    return render(request,'user/viewdetails.html',{"d":data})

def process(request):
    userid=request.session.get('userid')
    pid=request.GET.get('pid')
    btn=request.GET.get('bn')
    if userid is not None:
        if btn == 'kart':
            addtocart(pid=pid,userid=userid,status=True,cdate=datetime.datetime.now()).save()
        elif btn == 'order':
            order(pid=pid,userid=userid,remarks="pending",status=True,odate=datetime.datetime.now()).save()
            return HttpResponse("<script>alert('your order is comfirm...');window.location.href='/user/myorder/'</script>")
        return render(request,'user/process.html',{"alreadylogin":True})
    else:
        return HttpResponse("<script>window.location.href='/user/signin/'</script>")

    

def logout(request):
    del request.session['userid']
    return HttpResponse("<script>window.location.href='/user/home/'</script>")


def cartd(request):
    
    if request.session.get('userid'):
        userid=request.session.get('userid')
        cursor=connection.cursor()
        cursor.execute("select c.*,p.* from user_addtocart c,user_product p")
        datac=cursor.fetchall()
        pid = request.GET.get('pid')
        if request.GET.get('pid'):
            res=addtocart.objects.filter(pid=pid,userid=userid)
            res.delete()
            return HttpResponse("<script>alert('Your product has been removed successfully...');window.location.href='/user/cart'</script>")
    return render(request, 'user/cart.html',{"cart":datac})

