# Generated by Django 3.0 on 2020-03-12 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('footcount', '0004_employees'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('vis_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('vis_type', models.CharField(max_length=50)),
                ('vis_feature_vector', models.CharField(max_length=200)),
                ('vis_photo_path', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'visitors',
            },
        ),
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('log_visit_id', models.AutoField(primary_key=True, serialize=False)),
                ('log_time_in', models.DateTimeField(null=True)),
                ('log_time_out', models.DateTimeField(null=True)),
                ('log_visitor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footcount.Visitors')),
            ],
            options={
                'db_table': 'visitlog',
            },
        ),
        migrations.CreateModel(
            name='EmployeeVisit',
            fields=[
                ('emp_visit_id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_visit_emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footcount.Employees')),
            ],
            options={
                'db_table': 'employee_visit',
            },
        ),
    ]
