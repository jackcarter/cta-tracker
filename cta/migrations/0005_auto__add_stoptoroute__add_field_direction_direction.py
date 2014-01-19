# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StopToRoute'
        db.create_table(u'cta_stoptoroute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Route'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Stop'])),
        ))
        db.send_create_signal(u'cta', ['StopToRoute'])

        # Adding field 'Direction.direction'
        db.add_column(u'cta_direction', 'direction',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'StopToRoute'
        db.delete_table(u'cta_stoptoroute')

        # Deleting field 'Direction.direction'
        db.delete_column(u'cta_direction', 'direction')


    models = {
        u'cta.direction': {
            'Meta': {'object_name': 'Direction'},
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
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
            'route_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cta.Stop']", 'null': 'True', 'through': u"orm['cta.StopToRoute']", 'blank': 'True'})
        },
        u'cta.stop': {
            'Meta': {'object_name': 'Stop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'stop_id': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'stop_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cta.stoptoroute': {
            'Meta': {'object_name': 'StopToRoute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cta.Route']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cta.Stop']"})
        },
        u'cta.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['cta']