# Generated by Django 4.1.6 on 2023-02-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_alter_commentmodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votemodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]