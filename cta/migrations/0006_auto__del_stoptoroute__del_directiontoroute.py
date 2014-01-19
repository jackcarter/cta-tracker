# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'StopToRoute'
        db.delete_table(u'cta_stoptoroute')

        # Deleting model 'DirectionToRoute'
        db.delete_table(u'cta_directiontoroute')

        # Adding M2M table for field directions on 'Route'
        m2m_table_name = db.shorten_name(u'cta_route_directions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('route', models.ForeignKey(orm[u'cta.route'], null=False)),
            ('direction', models.ForeignKey(orm[u'cta.direction'], null=False))
        ))
        db.create_unique(m2m_table_name, ['route_id', 'direction_id'])

        # Adding M2M table for field stops on 'Route'
        m2m_table_name = db.shorten_name(u'cta_route_stops')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('route', models.ForeignKey(orm[u'cta.route'], null=False)),
            ('stop', models.ForeignKey(orm[u'cta.stop'], null=False))
        ))
        db.create_unique(m2m_table_name, ['route_id', 'stop_id'])


    def backwards(self, orm):
        # Adding model 'StopToRoute'
        db.create_table(u'cta_stoptoroute', (
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Route'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Stop'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cta', ['StopToRoute'])

        # Adding model 'DirectionToRoute'
        db.create_table(u'cta_directiontoroute', (
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Route'])),
            ('direction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cta.Direction'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'cta', ['DirectionToRoute'])

        # Removing M2M table for field directions on 'Route'
        db.delete_table(db.shorten_name(u'cta_route_directions'))

        # Removing M2M table for field stops on 'Route'
        db.delete_table(db.shorten_name(u'cta_route_stops'))


    models = {
        u'cta.direction': {
            'Meta': {'object_name': 'Direction'},
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cta.route': {
            'Meta': {'object_name': 'Route'},
            'directions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cta.Direction']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'route_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stops': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cta.Stop']", 'null': 'True', 'blank': 'True'})
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