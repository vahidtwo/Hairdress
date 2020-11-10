# Generated by Django 3.1.3 on 2020-11-08 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('barber', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, editable=False, max_digits=15)),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shifts', to='barber.barber')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shifts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]