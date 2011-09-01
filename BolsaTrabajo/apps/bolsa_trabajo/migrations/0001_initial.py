# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('bolsa_trabajo_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('bolsa_trabajo', ['Tag'])

        # Adding model 'UserProfile'
        db.create_table('bolsa_trabajo_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('bolsa_trabajo', ['UserProfile'])

        # Adding M2M table for field tags on 'UserProfile'
        db.create_table('bolsa_trabajo_userprofile_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['bolsa_trabajo.userprofile'], null=False)),
            ('tag', models.ForeignKey(orm['bolsa_trabajo.tag'], null=False))
        ))
        db.create_unique('bolsa_trabajo_userprofile_tags', ['userprofile_id', 'tag_id'])

        # Adding model 'Student'
        db.create_table('bolsa_trabajo_student', (
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['Student'])

        # Adding model 'Enterprise'
        db.create_table('bolsa_trabajo_enterprise', (
            ('website', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rut', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('bolsa_trabajo', ['Enterprise'])

        # Adding model 'EnterpriseCommentRing'
        db.create_table('bolsa_trabajo_enterprisecommentring', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_change', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enterprise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Enterprise'])),
        ))
        db.send_create_signal('bolsa_trabajo', ['EnterpriseCommentRing'])

        # Adding model 'EnterpriseComment'
        db.create_table('bolsa_trabajo_enterprisecomment', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.EnterpriseComment'], null=True)),
            ('unread_replies', self.gf('django.db.models.fields.IntegerField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.EnterpriseCommentRing'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['EnterpriseComment'])

        # Adding model 'OfferLevel'
        db.create_table('bolsa_trabajo_offerlevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('bolsa_trabajo', ['OfferLevel'])

        # Adding model 'Offer'
        db.create_table('bolsa_trabajo_offer', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('liquid_salary', self.gf('django.db.models.fields.IntegerField')()),
            ('enterprise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Enterprise'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['Offer'])

        # Adding M2M table for field level on 'Offer'
        db.create_table('bolsa_trabajo_offer_level', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['bolsa_trabajo.offer'], null=False)),
            ('offerlevel', models.ForeignKey(orm['bolsa_trabajo.offerlevel'], null=False))
        ))
        db.create_unique('bolsa_trabajo_offer_level', ['offer_id', 'offerlevel_id'])

        # Adding M2M table for field tags on 'Offer'
        db.create_table('bolsa_trabajo_offer_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('offer', models.ForeignKey(orm['bolsa_trabajo.offer'], null=False)),
            ('tag', models.ForeignKey(orm['bolsa_trabajo.tag'], null=False))
        ))
        db.create_unique('bolsa_trabajo_offer_tags', ['offer_id', 'tag_id'])

        # Adding model 'OfferComment'
        db.create_table('bolsa_trabajo_offercomment', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.OfferComment'], null=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('Offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Offer'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('new_replies', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['OfferComment'])

        # Adding model 'OfferMessageRing'
        db.create_table('bolsa_trabajo_offermessagering', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Offer'])),
            ('unread_messages', self.gf('django.db.models.fields.IntegerField')()),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Student'])),
            ('last_change', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['OfferMessageRing'])

        # Adding model 'OfferMessage'
        db.create_table('bolsa_trabajo_offermessage', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('ring', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.OfferMessageRing'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('bolsa_trabajo', ['OfferMessage'])

        # Adding model 'Application'
        db.create_table('bolsa_trabajo_application', (
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.OfferMessageRing'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['Application'])

        # Adding model 'ContractFeedbackEvaluation'
        db.create_table('bolsa_trabajo_contractfeedbackevaluation', (
            ('ordering', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('bolsa_trabajo', ['ContractFeedbackEvaluation'])

        # Adding model 'ContractFeedback'
        db.create_table('bolsa_trabajo_contractfeedback', (
            ('evaluation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.ContractFeedbackEvaluation'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('bolsa_trabajo', ['ContractFeedback'])

        # Adding model 'Contract'
        db.create_table('bolsa_trabajo_contract', (
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolsa_trabajo.Application'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enterprise_feedback', self.gf('django.db.models.fields.related.OneToOneField')(related_name='enterprise_contract', unique=True, to=orm['bolsa_trabajo.ContractFeedback'])),
            ('student_feedback', self.gf('django.db.models.fields.related.OneToOneField')(related_name='student_contract', unique=True, to=orm['bolsa_trabajo.ContractFeedback'])),
        ))
        db.send_create_signal('bolsa_trabajo', ['Contract'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('bolsa_trabajo_tag')

        # Deleting model 'UserProfile'
        db.delete_table('bolsa_trabajo_userprofile')

        # Removing M2M table for field tags on 'UserProfile'
        db.delete_table('bolsa_trabajo_userprofile_tags')

        # Deleting model 'Student'
        db.delete_table('bolsa_trabajo_student')

        # Deleting model 'Enterprise'
        db.delete_table('bolsa_trabajo_enterprise')

        # Deleting model 'EnterpriseCommentRing'
        db.delete_table('bolsa_trabajo_enterprisecommentring')

        # Deleting model 'EnterpriseComment'
        db.delete_table('bolsa_trabajo_enterprisecomment')

        # Deleting model 'OfferLevel'
        db.delete_table('bolsa_trabajo_offerlevel')

        # Deleting model 'Offer'
        db.delete_table('bolsa_trabajo_offer')

        # Removing M2M table for field level on 'Offer'
        db.delete_table('bolsa_trabajo_offer_level')

        # Removing M2M table for field tags on 'Offer'
        db.delete_table('bolsa_trabajo_offer_tags')

        # Deleting model 'OfferComment'
        db.delete_table('bolsa_trabajo_offercomment')

        # Deleting model 'OfferMessageRing'
        db.delete_table('bolsa_trabajo_offermessagering')

        # Deleting model 'OfferMessage'
        db.delete_table('bolsa_trabajo_offermessage')

        # Deleting model 'Application'
        db.delete_table('bolsa_trabajo_application')

        # Deleting model 'ContractFeedbackEvaluation'
        db.delete_table('bolsa_trabajo_contractfeedbackevaluation')

        # Deleting model 'ContractFeedback'
        db.delete_table('bolsa_trabajo_contractfeedback')

        # Deleting model 'Contract'
        db.delete_table('bolsa_trabajo_contract')
    
    
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
            'enterprise_feedback': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'enterprise_contract'", 'unique': 'True', 'to': "orm['bolsa_trabajo.ContractFeedback']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'description': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rut': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'bolsa_trabajo.enterprisecomment': {
            'Meta': {'object_name': 'EnterpriseComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.EnterpriseComment']", 'null': 'True'}),
            'ring': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.EnterpriseCommentRing']"}),
            'unread_replies': ('django.db.models.fields.IntegerField', [], {})
        },
        'bolsa_trabajo.enterprisecommentring': {
            'Meta': {'object_name': 'EnterpriseCommentRing'},
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Enterprise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bolsa_trabajo.offer': {
            'Meta': {'object_name': 'Offer'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Enterprise']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bolsa_trabajo.OfferLevel']", 'symmetrical': 'False'}),
            'liquid_salary': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bolsa_trabajo.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bolsa_trabajo.offercomment': {
            'Meta': {'object_name': 'OfferComment'},
            'Offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.Offer']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_replies': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolsa_trabajo.OfferComment']", 'null': 'True'})
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
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'bolsa_trabajo.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'bolsa_trabajo.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['bolsa_trabajo.Tag']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
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
