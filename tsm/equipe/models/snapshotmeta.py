# -*- coding: ISO-8859-1 -*-
from django.db import models

# Model de Snpashots de metas
class SnapshotMeta(models.Model):
    data = models.DateField(verbose_name="Data", null=False, blank=False) 
    
    def __unicode__(self):
        return self.data

    class Meta:
        app_label = 'equipe'