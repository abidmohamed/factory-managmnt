# Generated by Django 3.1.7 on 2021-04-06 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delivery', '0001_initial'),
        ('billingorder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbilling',
            name='delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.delivery'),
        ),
    ]
