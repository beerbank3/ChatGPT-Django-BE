# Generated by Django 4.2.3 on 2023-08-01 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='guest_29508010', max_length=50, unique=True),
        ),
    ]