from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

# Create your models here.

# State Model
class State(models.Model) :
    state = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.state}'


# Worker Model
class Worker(models.Model) :
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.PositiveIntegerField(help_text='Mobile Number Without Country Code')
    email = models.EmailField()
    aadhar_card = models.PositiveIntegerField(help_text='Enter Aadhar Card UID Number')
    address = models.TextField(max_length=300)
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    skills = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(default=timezone.now)
    left_date = models.DateTimeField(null=True, blank=True)
    gold_toot = models.DecimalField(decimal_places=6, max_digits=15)
    gold_toot_income = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    total_work = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    loss = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    paid = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    image = models.ImageField(default='defaults/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.full_name} : +91{self.phone}'

    def get_absolute_url(self):
        return reverse('jewellery-home')

    def get_passbook_url(self):
        return reverse('worker-passbook', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)
        img.thumbnail((250,250))
        img.save(self.image.path)

