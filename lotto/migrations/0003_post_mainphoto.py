# Generated by Django 4.1.1 on 2022-09-27 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0002_post_contents2'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='mainphoto',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
