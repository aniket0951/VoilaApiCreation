# Generated by Django 3.2.7 on 2021-10-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VoilaDriver', '0004_driverratecard'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiddingRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rider_id', models.IntegerField(blank=True, null=True)),
                ('driver_id', models.IntegerField(blank=True, null=True)),
                ('trip_id', models.IntegerField(blank=True, null=True)),
                ('live_bidding_rate', models.IntegerField(blank=True, null=True)),
                ('driver_status', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]