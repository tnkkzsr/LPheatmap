# Generated by Django 4.1.2 on 2023-06-27 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lpanalysis', '0007_clickdata_scrolldata'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrolldata',
            name='max_scroll_count',
            field=models.IntegerField(default=0),
        ),
    ]
