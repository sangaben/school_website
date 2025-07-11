# Generated by Django 5.2 on 2025-05-01 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('subtitle', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(upload_to='carousel/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
