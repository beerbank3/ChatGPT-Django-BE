# Generated by Django 4.2.3 on 2023-07-26 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='guest_44437450', max_length=50, unique=True),
        ),
    ]
