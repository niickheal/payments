# Generated by Django 5.0.4 on 2024-08-14 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankPayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.TextField(blank=True)),
                ('status', models.TextField(blank=True)),
                ('message', models.TextField(blank=True)),
                ('payout_id', models.TextField(blank=True)),
                ('reference', models.TextField(blank=True)),
                ('code', models.TextField(blank=True)),
                ('type', models.TextField(blank=True)),
            ],
        ),
    ]
