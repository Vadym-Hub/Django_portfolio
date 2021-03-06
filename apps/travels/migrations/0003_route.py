# Generated by Django 3.1.4 on 2020-12-21 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0002_train'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='название маршрута')),
                ('travel_times', models.PositiveSmallIntegerField(verbose_name='общее время в пути')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_from_city_set', to='travels.city', verbose_name='из какого города')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_to_city_set', to='travels.city', verbose_name='в какой город')),
                ('trains', models.ManyToManyField(to='travels.Train', verbose_name='список поездов')),
            ],
            options={
                'verbose_name': 'маршрут',
                'verbose_name_plural': 'маршруты',
                'ordering': ['travel_times'],
            },
        ),
    ]
