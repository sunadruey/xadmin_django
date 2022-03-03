# Generated by Django 2.2 on 2022-01-28 15:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='teacher/%Y/%m', verbose_name='封面图'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='org/%Y/%m', verbose_name='封面图'),
        ),
    ]