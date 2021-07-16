# Generated by Django 3.2.3 on 2021-06-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domains',
            fields=[
                ('id_domain', models.AutoField(primary_key=True, serialize=False)),
                ('domain_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ip', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'domains',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='DomainDetails',
        ),
    ]
