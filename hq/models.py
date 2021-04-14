from django.db import models
#from django.contrib.auth.models import User
import os
from fractions import Fraction
# from camera_imagefield import CameraImageField


class Person(models.Model):

    #team_user = models.OneToOneField(User,on_delete=models.CASCADE)
    id_number = models.CharField(max_length=128,blank=False,unique=True)
    name = models.CharField(max_length=50, blank=False)
    #team_email_id = models.EmailField(max_length=254,blank=False)
    #paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



def get_upload_path(instance, filename):
    return os.path.join(
      "%s" % instance.person.id_number, filename)


class PersonImage(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    pictures = models.ImageField(upload_to=get_upload_path,blank=False)
    # pictures = CameraImageField(aspect_ratio=Fraction(16, 9))
    # picture = CameraField(upload_to=get_upload_path, blank=True)

    def __str__(self):
        return self.person.id_number

class PersonBuffer(models.Model):

    id_number = models.CharField(max_length=128,blank=False,unique=True)
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return "{} - {}".format(self.name,self.id_number)