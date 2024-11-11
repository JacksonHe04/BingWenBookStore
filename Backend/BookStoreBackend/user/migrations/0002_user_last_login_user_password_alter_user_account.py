# Generated by Django 5.0.3 on 2024-11-11 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="password",
            field=models.CharField(default="default_password", max_length=128),
        ),
        migrations.AlterField(
            model_name="user",
            name="account",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
