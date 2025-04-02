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

class StolenItem(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stolen_items")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # User input instead of choices
    description = models.TextField()
    stolen_datetime = models.DateTimeField()  # Changed from DateField to DateTimeField
    location = models.CharField(max_length=255)
    location_description = models.TextField()  # Extra column for detailed location description
    keywords = models.TextField(blank=True)  # Stores extracted keywords
    created_at = models.DateTimeField(auto_now_add=True)

    def extract_keywords(self):
       
        doc = nlp(self.description)
        extracted_keywords = set(token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"])
        self.keywords = ", ".join(extracted_keywords)  # Store keywords as a comma-separated string
        self.save()

@receiver(post_save, sender=StolenItem)
def extract_keywords_on_save(sender, instance, **kwargs):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(instance.description.lower())  # Tokenize words
    keywords = [word for word in words if word.isalnum() and word not in stop_words]
    instance.extracted_keywords = ", ".join(keywords)
    instance.save(update_fields=["extracted_keywords"])  # Avoid infinite loop

class StolenItemImage(models.Model):
    stolen_item = models.ForeignKey(StolenItem, on_delete=models.CASCADE, related_name="item_images")
    image = models.ImageField(upload_to="stolen_items/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.stolen_item.name}"


    @staticmethod
    def find_matching_items(query):
        """ Finds stolen items that match a given query based on keywords """
        query_doc = nlp(query)
        query_keywords = set(token.text.lower() for token in query_doc if token.pos_ in ["NOUN", "PROPN"])
        
        all_items = StolenItem.objects.all()
        matched_items = []

        for item in all_items:
            item_keywords = set(item.keywords.split(", ")) if item.keywords else set()
            match_score = len(query_keywords & item_keywords) / len(query_keywords | item_keywords) if item_keywords else 0

            if match_score > 0.3:  # Threshold for similarity
                matched_items.append((item, match_score))

        return sorted(matched_items, key=lambda x: x[1], reverse=True)  # Sort by highest match score

    def __str__(self):
        return f"{self.name} - {self.category} ({self.user.username})"



