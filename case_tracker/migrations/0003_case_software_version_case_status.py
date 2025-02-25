# Generated by Django 5.1.6 on 2025-02-25 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case_tracker', '0002_case_business_case_number_case_circuit_diagram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='software_version',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='case',
            name='status',
            field=models.CharField(choices=[('pending', '待處理'), ('in_progress', '進行中'), ('completed', '已完成'), ('on_hold', '暫停'), ('canceled', '已取消')], default='pending', max_length=20),
        ),
    ]
