# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'tblIbloantransaction'
        db.create_table(u'Ib_tblibloantransaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbloandapplications'])),
            ('start_date', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('amount', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'Ib', ['tblIbloantransaction'])

        # Adding model 'tblIbinterest'
        db.create_table(u'Ib_tblibinterest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('duration', self.gf('django.db.models.fields.IntegerField')()),
            ('interest', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Ib', ['tblIbinterest'])

        # Adding model 'tblIbloandapplications'
        db.create_table(u'Ib_tblibloandapplications', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='allbranches', to=orm['business.tblBRANCH'])),
            ('date', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='allcustomer', to=orm['Ib.tblIbCUSTOMER'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbstandardloan'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('thrift', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'Ib', ['tblIbloandapplications'])

        # Adding model 'tblIbbankdetail'
        db.create_table(u'Ib_tblibbankdetail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Ib.tblIbCUSTOMER'])),
            ('branch_code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('account_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'Ib', ['tblIbbankdetail'])

        # Adding model 'tblIbsavingsaccount'
        db.create_table(u'Ib_tblibsavingsaccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recieved_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['staff.tblSTAFF'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['business.tblBRANCH'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('rec_date', self.gf('django.db.models.fields.DateField')(default='2020-02-04')),
        ))
        db.send_create_signal(u'Ib', ['tblIbsavingsaccount'])

        # Adding model 'tblIbstandardloan'
        db.create_table(u'Ib_tblibstandardloan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='IB CUSTOMER', to=orm['Ib.tblIbCUSTOMER'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='IB branch', to=orm['business.tblBRANCH'])),
            ('from_week', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('rate', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('to_week', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'Ib', ['tblIbstandardloan'])


    def backwards(self, orm):
        # Deleting model 'tblIbloantransaction'
        db.delete_table(u'Ib_tblibloantransaction')

        # Deleting model 'tblIbinterest'
        db.delete_table(u'Ib_tblibinterest')

        # Deleting model 'tblIbloandapplications'
        db.delete_table(u'Ib_tblibloandapplications')

        # Deleting model 'tblIbbankdetail'
        db.delete_table(u'Ib_tblibbankdetail')

        # Deleting model 'tblIbsavingsaccount'
        db.delete_table(u'Ib_tblibsavingsaccount')

        # Deleting model 'tblIbstandardloan'
        db.delete_table(u'Ib_tblibstandardloan')


    models = {
        u'Ib.tblibbankdetail': {
            'Meta': {'object_name': 'tblIbbankdetail'},
            'account_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'branch_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbCUSTOMER']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
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
        u'Ib.tblibinterest': {
            'Meta': {'object_name': 'tblIbinterest'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'code': ('django.db.models.fields.IntegerField', [], {}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'Ib.tblibloandapplications': {
            'Meta': {'object_name': 'tblIbloandapplications'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'allbranches'", 'to': u"orm['business.tblBRANCH']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'allcustomer'", 'to': u"orm['Ib.tblIbCUSTOMER']"}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbstandardloan']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'thrift': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'Ib.tblibloantransaction': {
            'Meta': {'object_name': 'tblIbloantransaction'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transaction_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Ib.tblIbloandapplications']"})
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
        u'Ib.tblibsavingsaccount': {
            'Meta': {'object_name': 'tblIbsavingsaccount'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['business.tblBRANCH']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rec_date': ('django.db.models.fields.DateField', [], {'default': "'2020-02-04'"}),
            'recieved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['staff.tblSTAFF']"})
        },
        u'Ib.tblibstandardloan': {
            'Meta': {'object_name': 'tblIbstandardloan'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'IB branch'", 'to': u"orm['business.tblBRANCH']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'IB CUSTOMER'", 'to': u"orm['Ib.tblIbCUSTOMER']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'from_week': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'to_week': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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