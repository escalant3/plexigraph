import simplejson

from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    topics = models.FileField(upload_to='files/')
    relations = models.FileField(upload_to='files/')
    configuration = models.TextField()


    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)


    def node_styles(self):
        configuration = simplejson.loads(self.configuration)
        return  configuration["node_styles"]
