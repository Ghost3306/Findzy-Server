
from django.urls import path,include
from dashboard import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('home',views.dashboard),
    path('search/<query>',views.searchquery)    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)