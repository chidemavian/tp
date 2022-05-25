from django.db import models

# Create your models here.



from staff.models import *



class tblstandardloanIIIB(models.Model):
	staffrec=models.ForeignKey(tblSTAFF, related_name='IIIB Staff')
	branch=models.ForeignKey(tblBRANCH, related_name='IIIB branch')
	from_week=models.CharField(max_length=20)
	rate=models.CharField(max_length=20)
	to_week=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	status=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.from_week)

class tblIIIb_bankdetail(models.Model):
	staff_rec=models.ForeignKey(tblSTAFF)
	branch_code=models.ForeignKey(tblBRANCH)
	bank_name=models.CharField(max_length=20)
	account_number=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.bank_name,self.account_number,self.branch)
	

class tblIIIbloandapplications(models.Model):
	branch=models.ForeignKey(tblBRANCH, related_name='allbranch')
	date =models.CharField(max_length=20)
	staffrec=models.ForeignKey(tblSTAFF, related_name='allStaff')
	package=models.ForeignKey(tblstandardloanIIIB)
	status=models.CharField(max_length=20)
	volume=models.CharField(max_length=20)
	thrift=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.volume,self.package)



class tblIIIbloantransaction(models.Model):
	transaction_source=models.ForeignKey(tblIIIbloandapplications)
	start_date=models.CharField(max_length=20)
	status=models.CharField(max_length=20)
	amount=models.CharField(max_length=20)
	

	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.start_date,self.status)


class tblIIIbsavingsaccount(models.Model):
	recieved_by=models.ForeignKey(tblSTAFF)
	branch=models.ForeignKey(tblBRANCH)
	amount=models.IntegerField()
	email=models.EmailField()
	rec_date =models.DateField(default= '2020-02-04')


	def __unicode__(self):
		return '%s %s %s'%(self.staff_rec,self.amount,self.saving_date)

