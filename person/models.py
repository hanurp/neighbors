from django.db import models
import geohash


class Person(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'User name')
    lon = models.FloatField()
    lat = models.FloatField()
    geo_hash = models.CharField(max_length=100, db_index=True, editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.geo_hash = geohash.encode(longitude=self.lon, latitude=self.lat)
        if update_fields:
            update_fields = update_fields + ['geo_hash']

        super(Person, self).save(force_insert=force_insert, force_update=force_update, using=using,
             update_fields=update_fields)
