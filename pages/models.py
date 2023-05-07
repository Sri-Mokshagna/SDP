from django.db import models

# Create your models here.

# class Access_Influencer(models.Model):
#     Influencer_name = models.CharField(max_length=50)
#     Fame = models.TextField()
#     thumbnail = models.ImageField()
#
#     def __str__(self):
#         return self.Influencer_name



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    user_type = models.CharField(max_length=255)



# class LoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)



