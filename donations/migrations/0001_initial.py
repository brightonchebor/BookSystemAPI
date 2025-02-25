# Generated by Django 5.1.3 on 2025-01-31 09:28

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=100)),
                ('condition', models.CharField(choices=[('new', 'New'), ('used', 'Used')], max_length=10)),
                ('subject_or_grade_level', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='book_images/')),
                ('availability_status', models.CharField(choices=[('available', 'Available'), ('donated', 'Donated')], default='available', max_length=10)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donated_books', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonetaryDonation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_gateway', models.CharField(choices=[('mpesa', 'M-pesa'), ('paypal', 'Paypal'), ('stripe', 'Stripe')], max_length=50)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monetary_donations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
