# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.PositiveIntegerField()
    aadhar_card = models.PositiveIntegerField()
    total_work = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    loss = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    paid = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    image = models.ImageField(default='defaults/default.jpg', upload_to='owner_profile_pics')
    no_of_employees = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)
        img.thumbnail((250,250))
        img.save(self.image.path)
