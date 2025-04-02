
from django.urls import path
from users import views
urlpatterns = [
    path('register',views.register_user),
    path('login',views.login_user),
    path('verify/<email_token>/',views.verify_acc),
    
    path('logout',views.user_logout),
    path('forgot',views.launchforgot),
    path('forgotpassword/<email_token>/',views.forgotpass)
]