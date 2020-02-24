from django.db import models


class Protein(models.Model):
    """Reference protein sequence"""
    ref_id = models.CharField('Reference ID', max_length=20, unique=True)
    description = models.CharField('Description', max_length=255)
    gene = models.CharField('Gene symbol', max_length=30)
    ec_number = models.CharField('EC number', max_length=20, blank=True)
    flag = models.CharField('flag', max_length=20, blank=True)
    organism = models.CharField('organism', max_length=255)
    source_db = models.CharField('source_db', max_length=20)
    sequence = models.TextField('Sequence')

    def __str__(self):
        return f"<Protein {self.ref_id} {self.description}>"
