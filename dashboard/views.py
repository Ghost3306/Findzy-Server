from django.shortcuts import render
from dashboard.models import StolenItem,StolenItemImage
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import nltk
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
            
           
    return render(request,'dashboard.html')