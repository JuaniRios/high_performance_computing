# Generated by Django 4.0.3 on 2022-04-13 15:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(choices=[(1, 'Submitted'), (2, 'Processing'), (3, 'Done')])),
                ('date_range', models.DateField()),
                ('assets', models.CharField(max_length=100, validators=[django.core.validators.int_list_validator])),
            ],
            options={
                'verbose_name': 'job',
                'verbose_name_plural': 'jobs',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('assets', models.CharField(max_length=100, validators=[django.core.validators.int_list_validator])),
                ('weights', models.CharField(max_length=100, validators=[django.core.validators.int_list_validator])),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='Master_Data.job')),
            ],
            options={
                'verbose_name': 'result',
                'verbose_name_plural': 'results',
            },
        ),
    ]