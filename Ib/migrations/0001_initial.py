# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'tblIbco'
        db.create_table(u'Ib_tblibco', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['staff.tblSTAFF'])),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('thrift1b', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Ib', ['tblIbco'])

        # Adding model 'tblIbCUSTOMER'
        db.create_table(u'Ib_tblibcustomer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbco'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customer.tblCUSTOMER'])),
            ('UX', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('online', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('sms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('get_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('withdr_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Ib', ['tblIbCUSTOMER'])

        # Adding model 'tblIbsavings_trans'
        db.create_table(u'Ib_tblibsavings_trans', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbco'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbCUSTOMER'])),
            ('recdate', self.gf('django.db.models.fields.DateField')()),
            ('transdate', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('wallet_type', self.gf('django.db.models.fields.CharField')(default='Main', max_length=40)),
            ('code', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('avalability', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'Ib', ['tblIbsavings_trans'])

        # Adding model 'tblIbMERCHANTbank'
        db.create_table(u'Ib_tblibmerchantbank', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbco'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbCUSTOMER'])),
            ('recdate', self.gf('django.db.models.fields.DateField')()),
            ('transdate', self.gf('django.db.models.fields.DateField')()),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('approved_by', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('wallet_type', self.gf('django.db.models.fields.CharField')(default='Main', max_length=30)),
        ))
        db.send_create_signal(u'Ib', ['tblIbMERCHANTbank'])

        # Adding model 'tblIbpayoutrequest'
        db.create_table(u'Ib_tblibpayoutrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbCUSTOMER'])),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbco'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('recdate', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('wallet_type', self.gf('django.db.models.fields.CharField')(default='Main', max_length=40)),
            ('account_type', self.gf('django.db.models.fields.CharField')(default='Main account', max_length=20)),
        ))
        db.send_create_signal(u'Ib', ['tblIbpayoutrequest'])

        # Adding model 'tblIbfieldagent'
        db.create_table(u'Ib_tblibfieldagent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbco'])),
            ('wallet_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('transdate', self.gf('django.db.models.fields.DateField')()),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbCUSTOMER'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'Ib', ['tblIbfieldagent'])

        # Adding model 'tblIbCashier'
        db.create_table(u'Ib_tblibcashier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbCUSTOMER'])),
            ('merchant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbco'])),
            ('transdate', self.gf('django.db.models.fields.DateField')()),
            ('remitdate', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('wallet_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('remitted_by', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'Ib', ['tblIbCashier'])


    def backwards(self, orm):
        # Deleting model 'tblIbco'
        db.delete_table(u'Ib_tblibco')

        # Deleting model 'tblIbCUSTOMER'
        db.delete_table(u'Ib_tblibcustomer')

        # Deleting model 'tblIbsavings_trans'
        db.delete_table(u'Ib_tblibsavings_trans')

        # Deleting model 'tblIbMERCHANTbank'
        db.delete_table(u'Ib_tblibmerchantbank')

        # Deleting model 'tblIbpayoutrequest'
        db.delete_table(u'Ib_tblibpayoutrequest')

        # Deleting model 'tblIbfieldagent'
        db.delete_table(u'Ib_tblibfieldagent')

        # Deleting model 'tblIbCashier'
        db.delete_table(u'Ib_tblibcashier')


    models = {
        u'Ib.tblibcashier': {
            'Meta': {'object_name': 'tblIbCashier'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbCUSTOMER']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbco']"}),
            'remitdate': ('django.db.models.fields.DateField', [], {}),
            'remitted_by': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transdate': ('django.db.models.fields.DateField', [], {}),
            'wallet_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'Ib.tblibco': {
            'Meta': {'object_name': 'tblIbco'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['staff.tblSTAFF']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thrift1b': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Ib.tblibcustomer': {
            'Meta': {'object_name': 'tblIbCUSTOMER'},
            'UX': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['customer.tblCUSTOMER']"}),
            'get_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbco']"}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'withdr_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Ib.tblibfieldagent': {
            'Meta': {'object_name': 'tblIbfieldagent'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbCUSTOMER']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbco']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transdate': ('django.db.models.fields.DateField', [], {}),
            'wallet_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'Ib.tblibmerchantbank': {
            'Meta': {'object_name': 'tblIbMERCHANTbank'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbCUSTOMER']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbco']"}),
            'recdate': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transdate': ('django.db.models.fields.DateField', [], {}),
            'wallet_type': ('django.db.models.fields.CharField', [], {'default': "'Main'", 'max_length': '30'})
        },
        u'Ib.tblibpayoutrequest': {
            'Meta': {'object_name': 'tblIbpayoutrequest'},
            'account_type': ('django.db.models.fields.CharField', [], {'default': "'Main account'", 'max_length': '20'}),
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbCUSTOMER']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbco']"}),
            'recdate': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'wallet_type': ('django.db.models.fields.CharField', [], {'default': "'Main'", 'max_length': '40'})
        },
        u'Ib.tblibsavings_trans': {
            'Meta': {'object_name': 'tblIbsavings_trans'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'avalability': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbCUSTOMER']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbco']"}),
            'recdate': ('django.db.models.fields.DateField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transdate': ('django.db.models.fields.DateField', [], {}),
            'wallet_type': ('django.db.models.fields.CharField', [], {'default': "'Main'", 'max_length': '40'})
        },
        u'business.tblbranch': {
            'Address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'Meta': {'object_name': 'tblBRANCH'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblCOMPANY']"}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'currency_description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '300'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'business.tblcompany': {
            'Meta': {'object_name': 'tblCOMPANY'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'fb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ig': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "'company_logo/thrift.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['partner.tblPARTNER']"}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'ux': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'youtube': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'customer.tblcustomer': {
            'Address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Meta': {'object_name': 'tblCUSTOMER'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'cc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'cs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ivb': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'othername': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.IntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'studentpix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ts': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wallet': ('django.db.models.fields.IntegerField', [], {})
        },
        u'partner.tblpartner': {
            'Meta': {'object_name': 'tblPARTNER'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'othername': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'staff.tblstaff': {
            'Address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Meta': {'object_name': 'tblSTAFF'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '20'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'othername': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.IntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'default': "'staff-pix/user.png'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'types': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['Ib']