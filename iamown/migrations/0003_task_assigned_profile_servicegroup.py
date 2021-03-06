# Generated by Django 4.0.4 on 2022-06-26 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_first_name_remove_profile_last_name_and_more'),
        ('iamown', '0002_alter_task_task_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_in_library_task', to='users.profile'),
        ),
        migrations.CreateModel(
            name='ServiceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_group', models.CharField(blank=True, default='', max_length=150, null=True, unique=True)),
                ('purpose', models.TextField(blank=True, default='', null=True)),
                ('qualified_intentions', models.TextField(blank=True, default='', null=True)),
                ('service_group_type', models.CharField(choices=[('---', '---'), ('1) Esoteric', '1) Esoteric'), ('2) Exoteric', '2) Exoteric')], default='---', max_length=20)),
                ('service_group_status', models.CharField(choices=[('1) Active', '1) Active'), ('2) Inactive', '2) Inactive')], default='1) Active', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to='users.profile')),
            ],
            options={
                'verbose_name': 'Service Group',
                'verbose_name_plural': 'Service Groups',
                'ordering': ['service_group_type', 'service_group'],
            },
        ),
    ]
