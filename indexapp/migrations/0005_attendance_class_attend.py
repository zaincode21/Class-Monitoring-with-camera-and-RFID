# Generated by Django 4.0.6 on 2022-10-31 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0004_remove_attendance_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='class_attend',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='indexapp.ourclass'),
            preserve_default=False,
        ),
    ]
