# Generated by Django 3.2.7 on 2021-09-26 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csfd_id', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csfd_id', models.TextField()),
                ('name', models.TextField()),
                ('actors', models.ManyToManyField(to='csfd_search.Actor')),
            ],
        ),
        migrations.AddConstraint(
            model_name='actor',
            constraint=models.UniqueConstraint(fields=('csfd_id',), name='actor_unique_csfd_id'),
        ),
        migrations.AddConstraint(
            model_name='movie',
            constraint=models.UniqueConstraint(fields=('csfd_id',), name='movie_unique_csfd_id'),
        ),
    ]
