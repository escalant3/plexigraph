import simplejson

from django.db import models

from fields import PickledObjectField

class Dataset(models.Model):
    DATASET_TYPE_CHOICES = (
        ('plxgh', 'Plexigraph'),
        ('adjlist', 'Adjacency List'),
        ('edgelist', 'Edge List'),
        ('gml', 'GML'),
        ('gpickle', 'Pickle'),
        ('graphml', 'GraphML'),
        ('leda', 'LEDA'),
        ('yaml', 'YAML'),
        ('graph6', 'Graph6'),
        ('sparse6', 'Sparse6'),
        ('pajek', 'Pajek'),
    )
    DEFAULT_CONFIGURATION = """ {"topic_structure": {},
    "relation_node_info": {},
    "node_styles": {},
    "edge_styles": {}
    }
    """
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    data_type = models.CharField(max_length=10, choices=DATASET_TYPE_CHOICES)
    topics = models.FileField(upload_to='files/', blank=True,
                                help_text='Useful for plexigraph format only')
    relations = models.FileField(upload_to='files/', blank=True,
                                help_text='Useful for plexigraph format only')
    graph_file = models.FileField(upload_to='files/', blank=True,
                        help_text='Required for non-plexigraph formats only')
    configuration = models.TextField(default = DEFAULT_CONFIGURATION)
    layout = PickledObjectField(blank=True)


    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)


    def get_configuration(self):
        return simplejson.loads(self.configuration)


    def node_styles(self):
        configuration = simplejson.loads(self.configuration)
        return  configuration["node_styles"]
