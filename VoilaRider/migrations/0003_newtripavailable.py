# Generated by Django 3.2.7 on 2021-10-02 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VoilaRider', '0002_ridertriplocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewTripAvailable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rider_id', models.IntegerField()),
                ('driver_id', models.IntegerField(max_length=120)),
                ('rider_pickup_lat', models.CharField(blank=True, max_length=1220, null=True)),
                ('rider_pickup_lng', models.CharField(blank=True, max_length=1220, null=True)),
                ('rider_pickup_address', models.CharField(blank=True, max_length=1210, null=True)),
                ('trip_id', models.CharField(blank=True, max_length=310, null=True)),
                ('trip_min_rate', models.CharField(blank=True, max_length=310, null=True)),
                ('trip_max_rate', models.CharField(blank=True, max_length=310, null=True)),
                ('trip_status', models.CharField(blank=True, max_length=310, null=True)),
            ],
        ),
    ]