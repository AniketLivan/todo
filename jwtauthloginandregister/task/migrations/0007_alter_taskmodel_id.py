# Generated by Django 4.1.6 on 2023-02-06 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_commentmodel_votemodel_userpermissionmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]