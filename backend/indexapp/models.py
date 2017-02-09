from __future__ import unicode_literals

from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Fs_database(models.Model):

    objct = models.CharField('Object', max_length = 25)
    location = models.CharField('Location', max_length = 25)

    def __str__(self):
        return '%s %s' % (self.objct, self.location)
