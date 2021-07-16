from django.db import models

# Create your models here.


class Domains(models.Model):
    id_domain = models.AutoField(primary_key=True)
    domain_name = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domains'
