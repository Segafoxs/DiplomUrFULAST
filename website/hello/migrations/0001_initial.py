# Generated by Django 5.1.4 on 2024-12-30 10:47

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Worker_is_mymodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryPermit',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=255)),
                ('reason', models.CharField(max_length=255)),
                ('department_name', models.CharField(max_length=255)),
                ('master_of_work', models.CharField(max_length=255)),
                ('signature_master', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись мастера')),
                ('executor', models.CharField(max_length=255)),
                ('countWorker', models.CharField(max_length=255)),
                ('workers', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=10), size=8)),
                ('work_description', models.CharField(max_length=255)),
                ('start_of_work', models.DateTimeField(max_length=255)),
                ('end_of_work', models.DateTimeField(max_length=255)),
                ('signature_director', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись директора')),
                ('signature_dailymanager', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись DailyManager')),
                ('signature_stationengineer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись StationEngineer')),
                ('safety', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=10), size=8)),
                ('condition', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('daily_manager', models.CharField(max_length=255)),
                ('station_engineer', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work_is_mymodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('DIRECTOR', 'Начальник цеха'), ('MASTER', 'Мастер'), ('WORKER', 'Работник'), ('DAILYMANAGER', 'Начальник смены'), ('STATIONENGINEER', 'Инженер станции')], max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(blank=True, editable=False, max_length=32, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.department')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.post', verbose_name='Должность')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Director_is_mymodel',
            fields=[
                ('worker_is_mymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hello.worker_is_mymodel')),
            ],
            bases=('hello.worker_is_mymodel',),
        ),
        migrations.CreateModel(
            name='Executor_is_mymodel',
            fields=[
                ('worker_is_mymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hello.worker_is_mymodel')),
            ],
            bases=('hello.worker_is_mymodel',),
        ),
        migrations.CreateModel(
            name='Manager_is_mymodel',
            fields=[
                ('worker_is_mymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hello.worker_is_mymodel')),
            ],
            bases=('hello.worker_is_mymodel',),
        ),
        migrations.CreateModel(
            name='ShiftManager_is_mymodel',
            fields=[
                ('worker_is_mymodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hello.worker_is_mymodel')),
            ],
            bases=('hello.worker_is_mymodel',),
        ),
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('OPEN', 'ОТКРЫТИЕ'), ('CLOSE', 'ЗАКРЫТИЕ')], max_length=255)),
                ('status', models.CharField(choices=[('approval', 'На согласовании с руководителем работ'), ('work', 'В работе'), ('closure', 'Закрытие'), ('closed', 'Закрыт')], default='На согласовании с руководителем работ', max_length=255)),
                ('signature_master', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись мастера')),
                ('countWorker', models.CharField(max_length=255)),
                ('workers', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=10), size=8)),
                ('work_description', models.CharField(max_length=255)),
                ('start_of_work', models.DateTimeField(max_length=255)),
                ('end_of_work', models.DateTimeField(max_length=255)),
                ('date_delivery', models.DateTimeField(max_length=255)),
                ('safety', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=10), size=8)),
                ('condition', models.CharField(max_length=255)),
                ('signature_director', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись директора')),
                ('signature_dailymanager', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись DailyManager')),
                ('signature_stationengineer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Подпись StationEngineer')),
                ('daily_manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dailymanager', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hello.department', verbose_name='Департамент')),
                ('director', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executorofwork', to=settings.AUTH_USER_MODEL)),
                ('master_of_work', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='masterofwork', to=settings.AUTH_USER_MODEL)),
                ('station_engineer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='statengineer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
