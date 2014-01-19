# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Route.asdfbool'
        db.delete_column(u'cta_route', 'asdfbool')


    def backwards(self, orm):
        # Adding field 'Route.asdfbool'
        db.add_column(u'cta_route', 'asdfbool',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    models = {
        u'cta.direction': {
            'Meta': {'object_name': 'Direction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cta.directiontoroute': {
            'Meta': {'object_name': 'DirectionToRoute'},
            'direction': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cta.Direction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cta.Route']"})
        },
        u'cta.route': {
            'Meta': {'object_name': 'Route'},
            'directions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cta.Direction']", 'null': 'True', 'through': u"orm['cta.DirectionToRoute']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'route_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cta.stop': {
            'Meta': {'object_name': 'Stop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'stop_id': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'stop_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cta.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['cta']