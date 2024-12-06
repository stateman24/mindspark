import datetime
from typing import Literal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class  Profile(models.Model):
    user = models.OneToOneField(User, related_name="userProfile", on_delete=models.CASCADE)
    date_of_birth  = models.DateField(null=True, validators=[MinValueValidator(limit_value=datetime.date.today() - datetime.timedelta(days=365*100))])
    city = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=500)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, default="profile_pic/no-profile.jpg")

    class Meta:
        ordering: tuple[Literal['user']] = ("user",)

    def __str__(self) -> str:
        return self.user.email + " Profile"
    

    



