# Generated by Django 4.2.4 on 2023-08-26 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='plan',
        ),
        migrations.AddField(
            model_name='plan',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plantype',
            name='month',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='plantype',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='plan',
            name='type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_account.plantype'),
        ),
    ]
