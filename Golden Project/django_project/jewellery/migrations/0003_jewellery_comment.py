# Generated by Django 3.0.5 on 2020-09-11 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jewellery', '0002_jewellery_extra_kdm'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewellery',
            name='comment',
            field=models.TextField(blank=True, help_text='Intructions Or Warning To Related Work', null=True),
        ),
    ]
