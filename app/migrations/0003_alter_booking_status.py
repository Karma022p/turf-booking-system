# Generated by Django 5.1 on 2025-04-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_booking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Booked', 'Booked'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
