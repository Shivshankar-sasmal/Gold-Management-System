# Generated by Django 3.0.5 on 2020-09-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewellery', '0003_jewellery_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewellery',
            name='urgent_work_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]