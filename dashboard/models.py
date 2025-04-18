import uuid
import spacy
import nltk
from django.db import models
from django.contrib.auth.models import User
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
nlp = spacy.load("en_core_web_sm")
nltk.download("punkt")
nltk.download("stopwords")
import uuid
from users.functions import send_match_result


class ReportItem(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stolen_items")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  
    description = models.TextField()
    stolen_datetime = models.DateTimeField()  
    location = models.CharField(max_length=255)
    keywords = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=ReportItem)
def check_matching(sender, instance, created, **kwargs):
    print('report receive')

    qu = instance.description+instance.location
    obj = StolenItem.find_matching_items(qu)
    ui = uuid.uuid4()
    msg = "We may have found items matching your lost report!\n\nPlease check the following links to see if any of them belong to you:\n\n"
    for o in obj:
        msg += f"🔗 http://127.0.0.1:8000/dashboard/view/{o.uid}\n"
    msg += "\nIf any of these items are yours, kindly follow the instructions on the page to claim them."
    send_match_result(instance.user.email, msg)


class StolenItem(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="report_item")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # User input instead of choices
    description = models.TextField()
    stolen_datetime = models.DateTimeField()  # Changed from DateField to DateTimeField
    location = models.CharField(max_length=255)
    location_description = models.TextField()  # Extra column for detailed location description
    keywords = models.TextField(blank=True)  # Stores extracted keywords
    created_at = models.DateTimeField(auto_now_add=True)




    @staticmethod
    def find_matching_items(query):
        query_doc = nlp(query)
        query_keywords = set(token.text.lower() for token in query_doc if token.pos_ in ["NOUN", "PROPN"])
        
        all_items = StolenItem.objects.all()
        matched_uids = []

        for item in all_items:
            item_keywords = set(item.keywords.split(", ")) if item.keywords else set()
            match_score = len(query_keywords & item_keywords) / len(query_keywords | item_keywords) if item_keywords else 0
            if match_score > 0.3:
                matched_uids.append(item.uid)

        return StolenItem.objects.filter(uid__in=matched_uids) # Sort by highest match score







    

class StolenItemImage(models.Model):
    stolen_item = models.ForeignKey(StolenItem, on_delete=models.CASCADE, related_name="item_images")
    image = models.ImageField(upload_to="stolen_items/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.stolen_item.name}"



class Message(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    item = models.ForeignKey(StolenItem,related_name='stolen_item',on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class Notification(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - {self.title}"



    
    



