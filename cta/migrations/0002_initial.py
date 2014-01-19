# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stop'
        db.create_table(u'cta_stop', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop_id', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('stop_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'cta', ['Stop'])

        # Adding model 'Direction'
        db.create_table(u'cta_direction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cta', ['Direction'])

        # Adding model 'Route'
        db.create_table(u'cta_route', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route_id', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('route_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'cta', ['Route'])

        # Adding model 'Vehicle'
        db.create_table(u'cta_vehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cta', ['Vehicle'])

        # Adding model 'DirectionToRoute'
        db.create_table(u'cta_directiontoroute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Route'])),
            ('direction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Direction'])),
        ))
        db.send_create_signal(u'cta', ['DirectionToRoute'])


    def backwards(self, orm):
        # Deleting model 'Stop'
        db.delete_table(u'cta_stop')

        # Deleting model 'Direction'
        db.delete_table(u'cta_direction')

        # Deleting model 'Route'
        db.delete_table(u'cta_route')

        # Deleting model 'Vehicle'
        db.delete_table(u'cta_vehicle')

        # Deleting model 'DirectionToRoute'
        db.delete_table(u'cta_directiontoroute')


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