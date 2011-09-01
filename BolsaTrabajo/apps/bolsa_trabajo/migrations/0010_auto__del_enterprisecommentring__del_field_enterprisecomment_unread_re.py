# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting model 'EnterpriseCommentRing'
        db.delete_table('bolsa_trabajo_enterprisecommentring')

        # Deleting field 'EnterpriseComment.unread_replies'
        db.delete_column('bolsa_trabajo_enterprisecomment', 'unread_replies')

        # Deleting field 'EnterpriseComment.ring'
        db.delete_column('bolsa_trabajo_enterprisecomment', 'ring_id')

        # Adding field 'EnterpriseComment.enterprise'
        db.add_column('bolsa_trabajo_enterprisecomment', 'enterprise', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='ent', to=orm['bolsa_trabajo.Enterprise']), keep_default=False)

        # Adding field 'EnterpriseComment.new_replies'
        db.add_column('bolsa_trabajo_enterprisecomment', 'new_replies', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding model 'EnterpriseCommentRing'
        db.create_table('bolsa_trabajo_enterprisecommentring', (
            ('enterprise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Enterprise'])),
            ('last_change', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('bolsa_trabajo', ['EnterpriseCommentRing'])

        # Adding field 'EnterpriseComment.unread_replies'
        db.add_column('bolsa_trabajo_enterprisecomment', 'unread_replies', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'EnterpriseComment.ring'
        db.add_column('bolsa_trabajo_enterprisecomment', 'ring', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bolsa_trabajo.EnterpriseCommentRing']), keep_default=False)

        # Deleting field 'EnterpriseComment.enterprise'
        db.delete_column('bolsa_trabajo_enterprisecomment', 'enterprise_id')

        # Deleting field 'EnterpriseComment.new_replies'
        db.delete_column('bolsa_trabajo_enterprisecomment', 'new_replies')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bolsa_trabajo.application': {
            'Meta': {'object_name': 'Application'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.OfferMessageRing']"})
        },
        'bolsa_trabajo.contract': {
            'Meta': {'object_name': 'Contract'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Application']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'enterprise_feedback': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'enterprise_contract'", 'unique': 'True', 'to': "orm['bolsa_trabajo.ContractFeedback']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'student_feedback': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'student_contract'", 'unique': 'True', 'to': "orm['bolsa_trabajo.ContractFeedback']"})
        },
        'bolsa_trabajo.contractfeedback': {
            'Meta': {'object_name': 'ContractFeedback'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'evaluation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.ContractFeedbackEvaluation']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bolsa_trabajo.contractfeedbackevaluation': {
            'Meta': {'object_name': 'ContractFeedbackEvaluation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        },
        'bolsa_trabajo.enterprise': {
            'Meta': {'object_name': 'Enterprise', '_ormbases': ['auth.User']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'rut': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'bolsa_trabajo.enterprisecomment': {
            'Meta': {'object_name': 'EnterpriseComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ent'", 'to': "orm['bolsa_trabajo.Enterprise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_replies': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.EnterpriseComment']", 'null': 'True'})
        },
        'bolsa_trabajo.offer': {
            'Meta': {'object_name': 'Offer'},
            'available_slots': ('django.db.models.fields.IntegerField', [], {}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Enterprise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bolsa_trabajo.OfferLevel']", 'symmetrical': 'False'}),
            'liquid_salary': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolsa_trabajo.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bolsa_trabajo.offercomment': {
            'Meta': {'object_name': 'OfferComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_replies': ('django.db.models.fields.IntegerField', [], {}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Offer']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.OfferComment']", 'null': 'True', 'blank': 'True'})
        },
        'bolsa_trabajo.offerlevel': {
            'Meta': {'object_name': 'OfferLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'bolsa_trabajo.offermessage': {
            'Meta': {'object_name': 'OfferMessage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.OfferMessageRing']"})
        },
        'bolsa_trabajo.offermessagering': {
            'Meta': {'object_name': 'OfferMessageRing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Offer']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Student']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unread_messages': ('django.db.models.fields.IntegerField', [], {})
        },
        'bolsa_trabajo.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['auth.User']},
            'has_cv': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'resume': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolsa_trabajo.Tag']", 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'bolsa_trabajo.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'bolsa_trabajo.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'block_public_access': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolsa_trabajo.Tag']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'validated_email': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['bolsa_trabajo']
