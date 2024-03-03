from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models

# models
from .models import Worker

# os import
import os


# Event Image Delete
@receiver(post_delete,sender=Worker)
def auto_delete_file_on_delete(sender,instance,**kwargs) :
    if not instance.image == 'defaults/default.jpg' :
        instance.image.delete(False)


# Event Image Change Delete
@receiver(models.signals.pre_save, sender=Worker)
def auto_delete_file_on_change(sender,instance,**kwargs) :

   try :
       old_file = sender.objects.get(pk=instance.pk).image
   except sender.DoesNotExist :
       return False

   new_file = instance.image

   if not old_file == new_file :
       if os.path.isfile(old_file.path) :
           if not old_file == 'defaults/default.jpg' :
                os.remove(old_file.path)
