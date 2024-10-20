import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator



class  Profile(models.Model):
    user = models.OneToOneField(User, related_name="userProfile", on_delete=models.CASCADE)
    date_of_birth  = models.DateField(null=True, validators=[MinValueValidator(limit_value=datetime.date.today() - datetime.timedelta(days=365*100))])
    city = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=11, null=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True)

    class Meta:
        ordering = ("user",)

    def __str__(self):
        return self.user.email + " Profile"
    
    



