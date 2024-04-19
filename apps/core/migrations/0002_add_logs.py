# Generated by Django 3.2.23 on 2023-12-09 17:04

import apps.core.models.api_key
from django.db import migrations, models
import django.db.models.deletion
import django_enum_choices.choice_builders
import django_enum_choices.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='type',
            field=django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('web', 'web'), ('proxy_client', 'proxy_client'), ('user_client', 'user_client'), ('git', 'git'), ('debug', 'debug')], default=apps.core.models.api_key.ApiKey.ApiKeyType['DEBUG'], enum_class=apps.core.models.api_key.ApiKey.ApiKeyType, max_length=12),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('base_log', models.JSONField(default=dict, verbose_name='log_log_base')),
                ('cleaned_log', models.JSONField(default=dict, verbose_name='log_log_cleaned')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='core.device', verbose_name='log_device')),
                ('remote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='core.remote', verbose_name='log_remote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='core.user', verbose_name='log_user')),
            ],
            options={
                'verbose_name': 'logs',
                'verbose_name_plural': 'logs',
                'db_table': 'logs',
                'default_permissions': (),
            },
        ),
    ]
