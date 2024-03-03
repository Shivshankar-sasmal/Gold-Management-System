# Generated by Django 3.0.5 on 2020-09-10 12:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jewellery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jewellery_name', models.CharField(help_text='Ornament Name', max_length=100)),
                ('jewellery_owner_name', models.CharField(max_length=150)),
                ('total_gold', models.DecimalField(decimal_places=6, max_digits=15)),
                ('gold_purity', models.DecimalField(decimal_places=6, max_digits=15)),
                ('KDM', models.DecimalField(decimal_places=6, default=0, max_digits=15)),
                ('jewellery_net_weight', models.DecimalField(decimal_places=6, max_digits=15)),
                ('gold', models.DecimalField(decimal_places=6, max_digits=15)),
                ('silver', models.DecimalField(decimal_places=6, max_digits=15)),
                ('bronze', models.DecimalField(decimal_places=6, max_digits=15)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('extra_gold', models.DecimalField(decimal_places=6, default=0, max_digits=15)),
                ('gold_to_be_given', models.DecimalField(decimal_places=6, max_digits=15)),
                ('gold_given', models.DecimalField(decimal_places=6, default=0, max_digits=15)),
                ('loss', models.DecimalField(decimal_places=6, default=0, max_digits=15)),
                ('paid', models.DecimalField(decimal_places=6, default=0, max_digits=15)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
                ('worker_name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workers.Worker')),
            ],
        ),
    ]
