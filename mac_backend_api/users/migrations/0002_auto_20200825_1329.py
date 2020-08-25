# Generated by Django 3.0.6 on 2020-08-25 18:29

from django.db import migrations, models
import mac_backend_api.utils.random_id.random_id


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=mac_backend_api.utils.random_id.random_id.random_id, editable=False, max_length=14, primary_key=True, serialize=False),
        ),
    ]
