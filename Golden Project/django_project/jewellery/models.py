from django.db import models
from django.utils import timezone
from django.urls import reverse

#models
from workers.models import Worker

# Create your models here.
class Jewellery(models.Model) :
    jewellery_name = models.CharField(max_length=100, help_text='Ornament Name')
    jewellery_owner_name = models.CharField(max_length=150)
    total_gold = models.DecimalField(decimal_places=6, max_digits=15)
    gold_purity = models.DecimalField(decimal_places=6, max_digits=15)
    KDM = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    extra_KDM = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    jewellery_net_weight = models.DecimalField(decimal_places=6, max_digits=15)
    gold = models.DecimalField(decimal_places=6, max_digits=15)
    silver = models.DecimalField(decimal_places=6, max_digits=15)
    bronze = models.DecimalField(decimal_places=6, max_digits=15)
    start_date = models.DateTimeField(default=timezone.now)
    worker_name = models.ForeignKey(Worker, on_delete=models.PROTECT)
    extra_gold = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    gold_to_be_given = models.DecimalField(decimal_places=6, max_digits=15)
    gold_given = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    loss = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    paid = models.DecimalField(decimal_places=6, max_digits=15, default=0)
    comment = models.TextField(null=True, blank=True, help_text='Intructions Or Warning To Related Work')
    urgent_work_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.jewellery_name} {self.jewellery_net_weight:.3}gm'

    def get_absolute_url(self):
        return reverse('jewellery-detail', kwargs={'pk' : self.pk})
