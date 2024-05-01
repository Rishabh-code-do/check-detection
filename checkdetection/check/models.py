from django.db import models

# Create your models here.

class check(models.Model):
    check_img=models.ImageField(upload_to='check_pics')
    back_check_img=models.ImageField(upload_to='back_check_pics')
