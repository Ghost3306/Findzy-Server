from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from users.models import Profile

def homepage(request):
    return render(request,'homepage.html')

def register_user(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        fname = name.split(' ')[0]
        lname = name.split(' ')[1]
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
                print('user already exist')
                return render(request,'register.html',{'message':'User already exists!'})
        else:
            user_obj = User(first_name=fname,last_name=lname,email=email,username=email)
            user_obj.set_password(password)
            user_obj.save()
            return render(request,'register.html',{'message':'Verfication mail sent to you'})
    return render(request,'register.html')

def login_user(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password) 
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            return render(request,'login.html',{'message':'Account not found!'})
        
        if not user_obj[0].user.is_email_verified:
             return render(request,'login.html',{'message':'Verify your account!'})
        
        user_obj = authenticate(username=username,password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('/dashboard/home')
        return render(request,'login.html',{'message','Invalid credentials!'})

    return render(request,'login.html')


def verify_acc(request,email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        if user.is_email_verified:
            context = {
            'status':'500',
            'title':'Message',
            'message':'Your account has already been verified.'
            }
            return render(request,'verificationmsg.html',context)
        user.is_email_verified=True
        user.save()
        context = {
            'status':'200',
            'title':'Account Verified!',
            'message':'Your account has been successfully verified.'
        }
        return render(request,'verificationmsg.html',context)
    except Exception as e:
        print(e)
        context = {
            'status':'500',
            'title':'Error!',
            'message':'Invalid Token.'
        }
        return render(request,'verificationmsg.html',context)
    

def user_logout(request):
    logout(request)
    return redirect('/')

def forgotpass(request,email_token):
    try:
        user = Profile.objects.filter(email_token=email_token)
        if not user.exists():
            context = {
            'status':'500',
            'title':'Error',
            'message':'Invalid Token.'
            }
            print('user not found')
            return render(request,'verificationmsg.html',context)
        else:
            
            email = user[0].user.email
            print(email)
            if request.method=="POST":
                password = request.POST.get('cnpass')
                user = User.objects.get(username=email)
                user.set_password(password)
                user.save()
                context = {
                'status':'200',
                'title':'Password Changed',
                'message':'Your password changed successfully.'
                }
                
                return render(request,'verificationmsg.html',context)
            return render(request,'forgotpassword.html',context)
            
    except Exception as e:
        print(e)
        context = {
            'status':'500',
            'title':'Error',
            'message':'Invalid Token.'
            }
        return render(request,'forgotpassword.html',context)

def launchforgot(request):
    if request.method=='POST':
        email = request.POST.get('email')
        print(email)
        #send email here
        return render(request,'forgot.html',{'message':'Reset password link sent to you'})  

    return render(request,'forgot.html')                
       
