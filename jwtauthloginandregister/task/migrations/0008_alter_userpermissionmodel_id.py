# Generated by Django 4.1.6 on 2023-02-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0007_alter_taskmodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpermissionmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
