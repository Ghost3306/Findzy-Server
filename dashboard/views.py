from django.shortcuts import render,redirect
from dashboard.models import StolenItem,StolenItemImage
from django.contrib.auth.models import User
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import nltk
from dashboard.models import StolenItem,ReportItem,Message
from django.dispatch import receiver
nlp = spacy.load("en_core_web_sm")
nltk.download("punkt")
nltk.download("stopwords")


def dashboard(request):
    if request.method=="POST":
        if 'name' in request.POST:
            name = request.POST.get("name")
            category = request.POST.get("category")
            description = request.POST.get("description")
            stolen_datetime = request.POST.get("stolen_datetime")
            location = request.POST.get("location")
            location_description = request.POST.get("location_description")
            images = request.FILES.getlist("image")  
            print(name,category,description,stolen_datetime,location,location_description)
            #keywords find

            doc = nlp(f"{description.lower()} {location_description} {location}")
            extracted_keywords = set(token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"])


            # stop_words = set(stopwords.words("english"))
            # words = word_tokenize(f"{description.lower()} {location_description}") 
            # keywords = [word for word in words if word.isalnum() and word not in stop_words]
            
            word_str = ", ".join(extracted_keywords)
            st_obj = StolenItem(name=name, user =request.user,category=category,description=description,stolen_datetime=stolen_datetime,keywords=word_str,location=location,location_description=location_description)
            
            st_obj.save()
            for image in images:
                st_img = StolenItemImage(stolen_item=st_obj,image=image)
                st_img.save()

            stolen = StolenItem.objects.filter(user=request.user)
            report = ReportItem.objects.filter(user=request.user)
            messages = Message.objects.filter(receiver=request.user)
            data = {
            'items':stolen,
            'reports':report,
            'message':"msg1",
            'messages':messages,
            'msg':"success"
            }   
           
            return render(request,'dashboard.html',context=data)

        if 'reportname' in request.POST:
            name = request.POST.get("reportname")
            category = request.POST.get("category")
            description = request.POST.get("description")
            stolen_datetime = request.POST.get("stolen_datetime")
            location = request.POST.get("location")
      
            doc = nlp(f"{description.lower()} {location}")
            extracted_keywords = set(token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"])

            
            word_str = ", ".join(extracted_keywords)
            re_obj = ReportItem(name=name, user =request.user,category=category,description=description,stolen_datetime=stolen_datetime,keywords=word_str,location=location)
            
            re_obj.save()
            stolen = StolenItem.objects.filter(user=request.user)
            report = ReportItem.objects.filter(user=request.user)
            messages = Message.objects.filter(receiver=request.user)
            data = {
            'items':stolen,
            'reports':report,
            'message':"msg",
            'messages':messages,
            'msg':"success"
            }   
           
            return render(request,'dashboard.html',context=data)

        if "receiver_uid" in request.POST:
            rec_email = request.POST.get('receiver_uid')
            reply = request.POST.get('msg_reply')
            item = request.POST.get('item')
            st_item = StolenItem.objects.get(uid=item)
            receiver = User.objects.get(email=rec_email)
            print(reply,item)
            msg_obj = Message(receiver=receiver,sender=request.user,body=reply,item=st_item)
            msg_obj.save()
            stolen = StolenItem.objects.filter(user=request.user)
            report = ReportItem.objects.filter(user=request.user)
            messages = Message.objects.filter(receiver=request.user)
            data = {
            'items':stolen,
            'reports':report,
            'messages':messages,
            'msg':"su"
            }   
           
            return render(request,'dashboard.html',context=data)
            

        if "sname" in request.POST:
            search = request.POST.get("sname")
            return redirect(f"/dashboard/search/{search}")

        if "sdes" in request.POST:
            search = request.POST.get("sdes")
            return redirect(f"/dashboard/searchdes/{search}")

    stolen = StolenItem.objects.filter(user=request.user)
    report = ReportItem.objects.filter(user=request.user)
    messages = Message.objects.filter(receiver=request.user)
    data = {
        'items':stolen,
        'reports':report,
        'messages':messages,
        'msg':"success"
    }   
           
    return render(request,'dashboard.html',context=data)

def searchquery(request,query):
    stolen_item= StolenItem.objects.filter(name__icontains=query)
    
    return render(request,'searchquery.html',{'searches':stolen_item})

def searchdescr(request,query):
    obj = StolenItem.find_matching_items(query)
    print("in search",obj)
    for i in obj:
        print(i.name)
    return render(request,'searchquery.html',{'searches':obj})


def delete_stolen(request,id):
    obj = StolenItem.objects.get(uid=id)
    if request.method =="POST":
        
        obj.delete()
        return redirect("/dashboard/home")
    return render(request,'delete.html',{'data':obj})


def delete_report(request,id):
    obj = ReportItem.objects.get(uid=id)
    if request.method =="POST":
        obj.delete()
        return redirect("/dashboard/home")
    return render(request,'delete.html',{'data':obj})


def get_card(request,uid):
    if request.user.is_authenticated:
        obj = StolenItem.objects.get(uid=uid)
        context = {
            'item':obj
        }
        if "message" in request.POST:
            message = request.POST.get("message")
            stolen_item = StolenItem.objects.get(uid=uid)
            receiver = stolen_item.user
            sender = request.user
            msg = Message(sender=sender,receiver=receiver,item=stolen_item,body=message)
            msg.save()
            data = {
            'msg':"success",
            'item':obj
            }   
           
            return render(request,'card.html',context=data)

        return render(request,'card.html',context)

        
    else:
        return redirect('/users/login')
    
