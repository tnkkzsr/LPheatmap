# Generated by Django 4.1.2 on 2023-06-27 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lpanalysis', '0008_scrolldata_max_scroll_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attentiondata',
            name='stay_time',
            field=models.IntegerField(default=0),
        ),
    ]
