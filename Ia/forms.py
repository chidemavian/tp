from django import forms
from staff.models import *
from Ia.models import *



approved= (('---','----'),('Approved', 'Approved'), ('Not Approved','Not Approved'))


transapproved= (('---','----'),('Approvals', 'Approvals'), ('Payouts','Payouts'))

status = (('---','----'),('Paid', 'Paid'), ('Pending','Pending'))

rrprt = (('---','----'),('daily', 'daily'), ('weekly','weekly'),('monthly','monthly'))

remitted = (('---','----'),('Remitted', 'Remitted'), ('Unremmitted','Unremmitted'), ('All','All'))


trans_report = (('---','----'),('DR', 'Deposit Requests'), ('WR','Withdrawal Requests'))

types = (('Main', 'Main'), ('Commission','Commission'))

avalability = (('Avalable', 'Avalable'), ('Not Available','Not Available'))

reason = ( 

	('Available', 'Available'),
	('Withdrawn','Withdrawn'), 
	('A/M','A/M'), 
	('Loan','Loan')

	)



monthy = (('---','----'),('January','January'),('February','February'),('March','March'),('April', 'April'),
	('May','May'),('June','June'),('July','July'),('August', 'August'),('September','September'),
	('October','October'),('November', 'November'),('December','December'))


month = (('-','----'),(1,'January'),(2,'February'),(3,'March'),(4, 'April'),
	(5,'May'),(6,'June'),(7,'July'),(8, 'August'),(9,'September'),
	(10,'October'),(11, 'November'),(12,'December'))




apps = ( 
	('-----','-----'),

	('Daily Contribution', 'Daily Contribution'),
	('Loans','Loans'),
	)

week = (('-','----'),(1,'Sunday'),(2,'Monday'),(3,'Tuesday'),(4, 'Wednesday'),
	(5,'Thursday'),(6,'Friday'),(7,'Saturday'))



class createwalletform(forms.Form):
    surname = forms.CharField(label='Surname',max_length= 190)
    firstname = forms.CharField(label='Firstname',max_length= 190)
    othername = forms.CharField(label='Otherame',max_length= 190, required=False)
    phone = forms.IntegerField(label='Phone' ,required=False)
    address = forms.CharField(label='Address',max_length= 190)
    email = forms.EmailField(label='E-mail' ,required=False)
    photo = forms.ImageField(label='Passport' ,required=False)

    def __init__(self, *args, **kwargs):
        super(createwalletform, self).__init__(*args)
        self.fields['surname'].widget.attrs['class'] = 'loginTxtbox'


class viewwalletform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')



class viewmerchantform(forms.Form):
	merchant = forms.IntegerField(label = 'Merchant ID')
	date = forms.CharField(label = "Transaction Date",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))


class viewallremittedform(forms.Form):
	status = forms.ChoiceField(label = 'Status' , choices=remitted)
	date = forms.CharField(label = "Transaction Date",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))

class viewtransform(forms.Form):
	status = forms.ChoiceField(label = 'Status' , choices=trans_report)
	date = forms.CharField(label = "Transaction Date",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))


class viewallapprovedform(forms.Form):
	status = forms.ChoiceField(label = 'Status' , choices=transapproved)
	date = forms.CharField(label = "Transaction Date",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))


class viewlogform(forms.Form):
	date = forms.CharField(label = "Transaction Date",max_length = 20)
	merchant = forms.ChoiceField(label='Merchant ID',choices = [(c.id, c.id) for c in tblIaMERCHANT.objects.all()])


class payoutform(forms.Form):
	status = forms.ChoiceField(label = 'Status' , choices=status)
	date = forms.CharField(label = "Transaction Date",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))


class thriftform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=month)
	thrift = forms.IntegerField(label = 'Thrift')
	wallet=forms.IntegerField(label='Wallet Address', required=False)

class kthriftform(forms.Form):
	month = forms.CharField(label = 'Month',required=False)
	thrift = forms.IntegerField(label = 'Thrift')
	wallet=forms.IntegerField(label='Wallet Address', required=False)



class remittalform(forms.Form):
	merchant = forms.IntegerField(label = 'Merchant ID')
	date = forms.CharField(label = "Transaction Date",max_length =10,widget = forms.TextInput(attrs={'readonly':'readonly'}))




class thriftamountform(forms.Form):
	amount = forms.IntegerField(label = 'Amount')
	thrift = forms.IntegerField(label = 'Thrift', required=False)
	wallet = forms.IntegerField(label = 'Wallet Address' ,required=False)
	month = forms.CharField(label = 'Month' ,required=False)


class unremitform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=month)
	status = forms.ChoiceField(label = 'Status' , choices=remitted)


class viewremallform(forms.Form):
	date = forms.CharField(label = "Transaction Date",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))


class withcashform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallete Address')
	date = forms.CharField(label = "Transaction Date",max_length =10,widget = forms.TextInput(attrs={'readonly':'readonly'}))

class merchantreportform(forms.Form):
	ID = forms.ChoiceField(label = "Merchant's ID",choices = [(c.id, c.id) for c in tblIaMERCHANT.objects.all()])
	name = forms.ChoiceField(label ="Name",choices = [(c.surname, c.surname) for c in tblSTAFF.objects.all()])
	date = forms.CharField(label = 'Select Date',max_length =10,widget = forms.TextInput(attrs={'readonly':'readonly'}))
	rtype = forms.ChoiceField(label = 'Report Type', choices=rrprt)


class cashreportform(forms.Form):
	ID = forms.ChoiceField(label = "Cashier's ID")
	name = forms.ChoiceField(label ="Name")
	date = forms.CharField(label = 'Select Date',max_length =10,widget = forms.TextInput(attrs={'readonly':'readonly'}))
	rtype = forms.ChoiceField(label = 'Report Type', choices=rrprt)

class performanceform(forms.Form):

	date = forms.CharField(label = 'Period',max_length =10,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':10}))
	to_date = forms.CharField(label = "To",max_length = 20, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','size':10}))

class trackform(forms.Form):

	from_date = forms.CharField(label = 'Period',max_length =10,required=False,widget = forms.TextInput(attrs={'readonly':'readonly','size':10}))
	to_date = forms.CharField(label = "To",max_length = 20, required=False, widget = forms.TextInput(attrs={'readonly':'readonly','size':10}))



class switchesform(forms.Form):
	merchant = forms.IntegerField(label = 'Current Merchant ID')


class adminreportform(forms.Form):
	ID = forms.ChoiceField(label = "Admin's ID")
	name = forms.ChoiceField(label ="Name")
	date = forms.CharField(label = 'Select Date',max_length =10,widget = forms.TextInput(attrs={'readonly':'readonly'}))
	rtype = forms.ChoiceField(label = 'Report Type', choices=rrprt)


class newswitchform(forms.Form):
	merchant = forms.ChoiceField(label ="Select New Merchant",choices = [(c.id, c.id) for c in tblSTAFF.objects.all()])




class fieldofficerfform(forms.Form):
	email = forms.EmailField(label = 'Staff Email')







