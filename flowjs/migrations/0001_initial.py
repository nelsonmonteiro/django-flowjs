# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FlowFile'
        db.create_table(u'flowjs_flowfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('original_filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('total_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_chunks', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_chunks_uploaded', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'flowjs', ['FlowFile'])

        # Adding model 'FlowFileChunk'
        db.create_table(u'flowjs_flowfilechunk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='chunks', to=orm['flowjs.FlowFile'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'flowjs', ['FlowFileChunk'])


    def backwards(self, orm):
        # Deleting model 'FlowFile'
        db.delete_table(u'flowjs_flowfile')

        # Deleting model 'FlowFileChunk'
        db.delete_table(u'flowjs_flowfilechunk')


    models = {
        u'flowjs.flowfile': {
            'Meta': {'object_name': 'FlowFile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_chunks': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_chunks_uploaded': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'flowjs.flowfilechunk': {
            'Meta': {'ordering': "['number']", 'object_name': 'FlowFileChunk'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'chunks'", 'to': u"orm['flowjs.FlowFile']"})
        }
    }

    complete_apps = ['flowjs']