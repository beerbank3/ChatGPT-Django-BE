# Generated by Django 4.2.3 on 2023-07-26 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='guest_25474152', max_length=50, unique=True),
        ),
    ]
