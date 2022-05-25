from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
from thrift.forms import *


from sysadmin.models import *
from customer.models import *
from merchant.models import *
from savings.models import *


from datetime import *
import calendar

#######import only merchant.models******
from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random


def welcome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		
		if staff.thrift_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('thrift/welcome.html',{'company':mybranch, 'user':varuser})
	
	else:
		return HttpResponseRedirect('/login/user/')



def admindash(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.admin==0 and staff.cashier==0 and staff.thrift_officer==0:
			return render_to_response('Ia/404loan.html',{'company':mybranch, 'user':varuser})

		# return render_to_response('thrift/adminwelcome.html',{'company':mybranch, 'user':varuser})
		return render_to_response('thrift/dashboardIa.html',{'company':mybranch, 'user':varuser,'pincode':staff})

	else:
		return HttpResponseRedirect('/login/user/')


def adminuserguide(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		
		if staff.admin==0 and staff.cashier==0 and staff.thrift_officer==0:
			return render_to_response('Ib/404loan.html',{'company':mybranch, 'user':varuser})

		elif staff.admin:
			return render_to_response('thrift/adminwelcome.html',{'company':mybranch, 'user':varuser})
		elif staff.cashier:
			return render_to_response('thrift/adminwelcome4.html',{'company':mybranch, 'user':varuser})
		elif staff.thrift_officer:
			return render_to_response('thrift/adminwelcome5.html',{'company':mybranch, 'user':varuser})
	
	else:
		return HttpResponseRedirect('/login/user/')





### THRIFT AFFAIRS*************************


def thriftrep(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		

		if request.method == 'POST':
			form = unremitform(request.POST)
			if form.is_valid()==False:
				month=form.cleaned_data['month'] #month in figures
				if month=="-":
					pass
				else:

					monthname = calendar.month_name[int(month)]

					dll=[]				
					details=tblCUSTOMER.objects.filter(branch=mybranch, merchant=memmerchant,status=1)
					for  k in details:
						try:
							thriftrec=tblthrift.objects.get(account_type = 'Main account',customer=k,number=month)
							dl={'wallet':k.wallet,'thrift':thriftrec.thrift}				
						except:
							dl={'wallet':k.wallet,'thrift':0}
						dll.append(dl)

					return render_to_response('thrift/thriftrep.html',{'company':mybranch,'user':varuser,'thriftrec':dll,'month':monthname})

		else:
			form=unremitform()
		return render_to_response('thrift/repthr.html',{'company':mybranch,'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/user/')



def addthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
					myform = thriftform()
					return render_to_response('thrift/myadd.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/addthrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')


def account_type(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')
    		
    		if month== '-' : 
    			msg = 'Select a month'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    		
    		if acccode== '-----' : 
    			msg = 'Select account type'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
  
    		else : 
    			try : 
 					www=int(month)

					monthname = calendar.month_name[www] #converts month_index to month_name
				
					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

					memmerchant=tblMERCHANT.objects.get(staff= staffid ,status=1)
					
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=wallet,status=1)
					
					thriftrec=tblthrift.objects.get(account_type = acccode, merchant=memmerchant, number=month,customer=details)
									
					return render_to_response('thrift/aaa.html',{'month':monthname,'wallet':wallet,
						'thriftrec':thriftrec,'acccode':acccode})
	    			
    			except : 

	    			myform = thriftform()
	    			return render_to_response('thrift/main_account.html',{'form':myform,
	    				'wallet':wallet,'account_type':acccode,'month':month})
	    	
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')




def putthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch,
				'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch,
				'user':varuser})
	

		yday = date.today().year

		if request.method == 'POST':
			form = thriftform(request.POST)
			if form.is_valid():
				number=request.POST['month']  #returns month number as directed in form
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']
				account_type=request.POST['account_type']

				month=calendar.month_name[int(number)] #converts month number to month name

				customer=tblCUSTOMER.objects.get(merchant=memmerchant,
					wallet=wallet,status=1)

				k = random.randint(0,9)
				y = random.randint(0,9)
				x = random.randint(0,9)
				z = random.randint(0,9)
				a = random.randint(0,9)
				pin =  str(k) + str(y) + str(x) + str(z)+ str(a)

				
				countt= tblthrift.objects.filter(account_type = account_type, 
					month=month,
					branch=mybranch,
					merchant= memmerchant,
					customer=customer).count()

				if countt<1:
					tblthrift(account_type = account_type,month=month,thrift=mythrift,branch=mybranch,
						merchant= memmerchant,customer=customer,
						code=pin,number=number,year=yday).save()
				return render_to_response('thrift/addthriftsuccess.html',{'company':mybranch, 
					'user':varuser,'wallet':wallet,'account':account_type,'year':yday,
					'thrift':mythrift,'month':month})
			
			else:
				msg = "Enter valid amount"
	else:
		return HttpResponseRedirect('/login/user/')



def addmythrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)

		tdate= date.today()
		mday=tdate.month
		month = calendar.month_name[mday]
		myform = kthriftform()


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			myform = kthriftform(request.POST)
			details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
			return render_to_response('thrift/comeadd.html',{'company':mybranch,'user':varuser,'form':myform,
			'wallet':mywallet,'month':month})
		else:
			return HttpResponseRedirect('/login/user/')


def putinthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		
		if request.method == 'POST':
			form = kthriftform(request.POST)
			if form.is_valid():
				month=request.POST['month']  # month in words
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']

				today=date.today()
				yday=today.year

				month1 = datetime.strptime(month,"%B") #converts month_name to month_index
				month2=month1.month
				customer=tblCUSTOMER.objects.get(merchant=memmerchant,wallet=wallet,
					status=1)
				
				tblthrift(account_type = 'Main account',month=month,year=yday,thrift=mythrift,branch=mybranch,
					merchant= memmerchant,customer=customer,
					code=8797,number=month2).save()

				return render_to_response('thrift/addthriftsuccess.html',{'company':mybranch, 'user':varuser,'wallet':wallet,'thrift':mythrift,'month':month})
			else:
				msg = 'im me'
				return render_to_response('thrift/comeadd.html',{'msg':month})

		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')

def viewthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
					myform = thriftform()
					return render_to_response('thrift/myview.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/viewthrifthistory.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')


def account_view(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')
    		


    		if month== '-' : 
    			msg = 'Select a month'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    		
    		if acccode== '-----' : 
    			msg = 'Select account type'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
  
    		else : 
    			try : 
 					www=int(month)

					monthname = calendar.month_name[www]
				
					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

					memmerchant=tblMERCHANT.objects.get(staff= staffid ,status=1)
					
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=wallet,status=1)
					
					thriftrec=tblthrift.objects.get(account_type = acccode, merchant=memmerchant, number=month,customer=details)
					
					return render_to_response('thrift/vvv.html',{'month':monthname,'wallet':wallet,
						'thriftrec':thriftrec,'acccode':acccode})
	    			
    			except : 
    				msg = 'No entries found'

	    			myform = thriftform()
	    			return render_to_response('thrift/selectloan.html',{'msg':msg,})
	    	
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')

def changethrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to month_number to month_name

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
					myform = thriftform()
					return render_to_response('thrift/mychange.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/changethrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')


def account_change(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')
    		
    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)




    		if month== '-' : 
    			msg = 'Select a month'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    		
    		if acccode== '-----' : 
    			msg = 'Select account type'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
  
    		else : 
    			try : 
 					www=int(month)

					monthname = calendar.month_name[www]

					staff = Userprofile.objects.get(email=user,status=1)

					staffid = staff.staffrec.id

					memmerchant=tblMERCHANT.objects.get(staff= staffid ,status=1)
					
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=wallet,status=1)
					
					thriftrec=tblthrift.objects.get(account_type = acccode, merchant=memmerchant, number=month,customer=details)
					
					transactions=tblthrift_trans.objects.filter(account_type=acccode,recdate__month=www,
						merchant=memmerchant,branch=mybranch)
					
					if transactions.count() == 0 : 
						transactions=0
						msg = 'Click the change link to begin'
					else: 
						msg = ' you cannot change thrift value at this time'
						transactions=transactions.count()

					return render_to_response('thrift/ccc.html',{'count':transactions,
						'month':monthname,'wallet':wallet,'user':user,'acccode':acccode,
						'msg':msg,'thriftrec':thriftrec})

    			except : 
    				msg = 'No entries found'
	    			return render_to_response('thrift/selectloan.html',{'msg':msg,})
	    	
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def edit_thrift_popup(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		wallet,month,account_type,user=acccode.split(':')

    		staff = Userprofile.objects.get(email=user,status=1)
    		staffdet=staff.staffrec.id
    		branch=staff.branch.id
    		mycompany=staff.branch.company
    		company=mycompany.name
    		comp_code=mycompany.id
    		ourcompany=tblCOMPANY.objects.get(id=comp_code)
    		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
    		customer=tblCUSTOMER.objects.get(wallet=wallet)


    		mycom = tblthrift.objects.get(
    			customer=customer,
    			month=month,
    			account_type=account_type)
    		thrift=mycom.thrift
	    	return render_to_response('thrift/thrif_edit.html',{'thrift':thrift,
	    		'income':mycom,'month':month,'wallet':wallet})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def thriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month
		

		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			dd=request.POST['date'] #month in fnumber
			dd = calendar.month_name[int(dd)] #converts to month name

			return render_to_response('thrift/prevchan.html',{'company':mybranch, 'user':varuser,'month':dd,'wallet':mywallet,'thrift':ttr})

	else:
		return HttpResponseRedirect('/login/user/')


def safethriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month
		

		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			dd=request.POST['month'] #month in words
			newthrift = request.POST['newt']

			if newthrift !='':
				customer=tblCUSTOMER.objects.get(wallet=mywallet,status=1)
				firstthrift = tblthrift.objects.get(
					account_type = 'Main account',
					month=dd,
					customer=customer)
				firstthrift.thrift=newthrift
				firstthrift.save()
				return render_to_response('thrift/savethriftsuccess.html',{'company':mybranch, 'user':varuser,'month':dd,'wallet':mywallet,'thrift':ttr,'newt':newthrift})
			else:
				return HttpResponseRedirect('/thrift/thrift/changethrift/')
	else:
		return HttpResponseRedirect('/login/user/')


def rolloverthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
		
		mydatee=date.today().month #month in figures
		current_date =int(mydatee)
		yday = date.today().year
		ddt= calendar.month_name[int(mydatee)] #month in words

		if mydatee == 12:
			nextmonth = 1
			yday=yday+1
		else:
			nextmonth=mydatee + 1

		nnm= calendar.month_name[int(nextmonth)]

		if request.method=='POST':
			details=tblCUSTOMER.objects.filter(branch=mybranch, merchant=memmerchant,status=1)
			for  k in details:
				try:
					thriftrec=tblthrift.objects.get(account_type = 'Main account',customer=k,number=mydatee)							
					
					if tblthrift.objects.filter(account_type = 'Main account',customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm, number=nextmonth).count() == 0:
						tblthrift(account_type = 'Main account',customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm,thrift=thriftrec.thrift,code = 87867, number=nextmonth).save()
			
				except:

					if tblthrift.objects.filter(account_type = 'Main account',customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm,number=nextmonth).count()==0:
						tblthrift(account_type = 'Main account',customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm,thrift=0,code = 87867, number=nextmonth).save()
			return render_to_response('thrift/rollsuccess.html',{'company':mybranch, 'user':varuser,'month':ddt,'nextmonth':nnm})

		else:
			return render_to_response('thrift/rolloverthrift.html',{'company':mybranch, 'user':varuser,'month':ddt,'nextmonth':nnm})

	else:
		return HttpResponseRedirect('/login/user/')




####  CAsh iN prOcedures************************

def payrequests(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.filter(staff=memstaff,status=1).count()
		
		if staff.thrift_officer==0  or memmerchant<1:
			return render_to_response('thrift/404.html',{'company':mybranch, 'user':varuser})

	      
					
		mydate=date.today().month #gives month in number
		month= calendar.month_name[mydate] #converts month number to month name
		datee= date.today()

		
		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
					myform = thriftform()
					return render_to_response('thrift/deposit.html',{'company':mybranch,'user':varuser,'form':myform,
					'month':month,'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'
		else:
			form=viewwalletform()
		return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form})

		
	else:
		return HttpResponseRedirect('/login/user/')


def account_dep(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')
    		   		
    		if acccode== '-----' : 
    			msg = 'Select account type'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
  
    		else : 
    			try : 	


					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

		 			branch=staff.branch.id
					mycompany=staff.branch.company
					company=mycompany.name
					comp_code=mycompany.id
					ourcompany=tblCOMPANY.objects.get(id=comp_code)
					mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


					memmerchant=tblMERCHANT.objects.get(staff= staffid ,status=1)
					
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=wallet,status=1)
					
					thriftrec=tblthrift.objects.get(account_type = acccode,merchant=memmerchant,month=month,branch=mybranch,customer=details)

					thrift = thriftrec.thrift
					year=thriftrec.year

					month1 = datetime.strptime(month,"%B") #converts month_name to month_index
					month2=month1.month

					number_count= tblthrift_trans.objects.filter(
						account_type = acccode,
						wallet_type='Main',
						branch=mybranch,
						avalability='Available',
						reason='Available',
						merchant=memmerchant,
						customer=details,
						recdate__month = month2)

					
					if number_count.count() == 0:  

						request_count= tblpayoutrequest.objects.filter(
							account_type = acccode,
							wallet_type='Main',
							branch=mybranch,
							merchant=memmerchant,
							status='Unpaid',
							customer=details,
							recdate__month = month2)

						if request_count.count() == 0 :
							add = 0
						else: 
							add=request_count.aggregate(Sum('amount'))
							add = add['amount__sum']

							add= 'N',add , ' Requested'
					else : 
						add=number_count.aggregate(Sum('number'))
						add = add['number__sum']
				
					return render_to_response('thrift/dep.html',{'month':month,'wallet':wallet,
							'thrift':thrift,'year':year, 'cccode':acccode
							,'add':add
							})	

    			except : 
    				msg = 'No thrift record found for  ' + month + ' for this ' + acccode
    				return render_to_response('thrift/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def source(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,thrift,month,account=acccode.split(':')
    		if acccode== '-----': 
    			msg = 'Select funding source'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    		elif acccode=='Cash': 
    			myform = thriftamountform()
    			return render_to_response('thrift/cash.html',{'form':myform,
    				'wallet':wallet,'thrift':thrift,'month':month,'account_type':account})
    		elif acccode=='Transfer':
    			msg = 'This option is coming soon !!!'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')




def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request):
    term = request.GET.get('term')

	# varuser=request.session['userid']
	# staff = Userprofile.objects.get(email=varuser,status=1)

	# if staff.thrift==0:
	# 	return render_to_response('404.html',{'company':mybranch, 'user':varuser})

	# staffdet=staff.staffrec.id
	# branch=staff.branch.id

	# mycompany=staff.branch.company
	# company=mycompany.name
	# comp_code=mycompany.id
	# ourcompany=tblCOMPANY.objects.get(id=comp_code)

	# mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

	# memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


    
    suggestions = []
    qset = tblthrift.objects.get(account_type = 'Main account',code =8797)#[:10]
    thrift  = 1000
    thrr = 2000
    suggestions.append(thrr)
    
    # for x in range(1,6): 
    # 	thrr = x * thrift
    # 	suggestions.append({'label': '%s :%s :%s :%s ' % (x, thrr), 'number': x,'amount':thrr})
    # 	# suggestions.append({'amount':thrr})
    return suggestions

    # for i in qset:
    #     suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    # return suggestions


def history(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
	
		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
					myform = thriftform()
					return render_to_response('thrift/conthistory.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/payhistory.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')




def account_history(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,month,user=acccode.split(':')
    		
    		if month== '-' : 
    			msg = 'Select a month'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
    		
    		if acccode== '-----' : 
    			msg = 'Select account type'
    			return render_to_response('thrift/selectloan.html',{'msg':msg})
  
    		else : 

    			try :					
					www=int(month)

					monthname = calendar.month_name[www] #converts month_index to month_name
				
					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

					memmerchant=tblMERCHANT.objects.get(staff= staffid ,status=1)
					
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=wallet,status=1)
					
					thriftrec=tblthrift.objects.get(account_type = acccode, merchant=memmerchant, number=month,customer=details)
					
					
					thriftrec= tblthrift_trans.objects.filter(
						account_type = acccode,
						wallet_type='Main', 
						customer=details, 
						reason='Available',
						avalability='Available',
						recdate__month=www).order_by('recdate').reverse()
					

					if thriftrec.count() > 0 :  
						add=thriftrec.aggregate(Sum('amount'))
						add = add['amount__sum']

					else: 

						request_count= tblpayoutrequest.objects.filter(
							account_type = acccode,
							wallet_type='Main',
							merchant=memmerchant,
							status='Unpaid',
							customer=details,
							recdate__month = www)

						rqt = request_count.count()

						if rqt  > 0 : 
							add=request_count.aggregate(Sum('amount'))
							add = add['amount__sum']

							add= add , ' Requested'
							
						else: 
							#go check tblpayoutbank
							add= 0

					return render_to_response('thrift/bal.html',{
						'customer':details,
						'wallet':wallet,
						'thriftrec':thriftrec,
						'bal':add})
	    			
    			except : 
    				msg = 'Account balance = N 0.00'

	    			return render_to_response('thrift/selectloan.html',{'msg':msg})
	    	
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')





def cashin(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		if staff.thrift_officer==0: 
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
	
		if request.method == 'POST':
			form = thriftamountform(request.POST)
			if form.is_valid():
				amount=form.cleaned_data['amount']
				mythrift=request.POST['thrift']
				wallet=request.POST['wallet']
				account_type=request.POST['account_type']
				amount=int(amount)
				mythrift=int(mythrift)

				lump,l=divmod(amount,mythrift)

				if l == 0 : 
					fdate= datetime.today()
					month=fdate.month #in figures
					year=fdate.year
					weekday=date.today().isocalendar()[1]

					customer=tblCUSTOMER.objects.get(wallet=wallet,status=1,merchant=memmerchant,branch=mybranch)
					
					tyu= tblthrift.objects.get(customer=customer,number=month,account_type=account_type,merchant=memmerchant,branch=mybranch,year=year)

					pin = tyu.code

					number_count= tblthrift_trans.objects.filter(account_type = account_type,wallet_type='Main', branch=mybranch,merchant=memmerchant,
						customer=customer, recdate__month=month)

					if number_count.count() == 0:  
						add = 0 
					else : 
						add=number_count.aggregate(Sum('number'))
						add = add['number__sum']
		
					p = (monthrange(fdate.year, fdate.month))[-1]

					if  add + lump <= p : 

						countt= tblMerchantTrans.objects.filter(
							account_type = account_type,
							branch=mybranch,
							customer=customer,
							merchant=memmerchant,
							recdate=fdate,
							amount=amount,
							wallet_type='Main',
							remitted='Unremmitted',
							approved='Not Approved').count()
						
						if countt<1:
							tblMerchantTrans(account_type = account_type, 
								weekno=weekday, 
								branch=mybranch,
								customer=customer,
								merchant=memmerchant,
								recdate=fdate,
								amount=amount,
								wallet_type='Main',
								remitted='Unremmitted',
								approved='Not Approved',
								code=pin).save()

							return render_to_response('thrift/cashinthriftsuccess.html',{'account_type':account_type, 
								'company':mybranch, 
								'user':varuser,
								'wallet':wallet,
								'thrift':mythrift,
								'amount':amount})
						else:
							msg ='YOU CANNOT POST SAME AMOUNT TWICE, SAME DAY'

					else : 
						msg = 'Amount too large'
				else:
					msg ='This amount is not applicable'
		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')

def unremmitted(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		
		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				yday,mday,dday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)

				# thismonth= calendar.month_name[mday]

				thriftrec=[]

				# thismonth= calendar.month_name[mday]
				# month_name = calendar.month_abbr[2]
				# month_number = list(calendar.month_abbr).index('Feb')


				if mystatus == '---' or tdate == '---':
					return HttpResponseRedirect('/thrift/thrift/unremmitted/')
				
				elif mystatus=='Remitted':				

					trec=tblmerchantBank.objects.filter(merchant=memmerchant,branch=mybranch,
						recdate=oydate,
						# status=mystatus
						)

				elif mystatus=='Unremmitted':
					trec = tblMerchantTrans.objects.filter(branch=mybranch,merchant=memmerchant,
						wallet_type='Main',recdate=oydate,remitted=mystatus)
					
				else:
					trec=tblmerchantBank.objects.filter(merchant=memmerchant,branch=mybranch,
						recdate=oydate,)


					trec = tblMerchantTrans.objects.filter(branch=mybranch,merchant=memmerchant,
						wallet_type='Main',recdate=oydate,remitted=mystatus)

				countt=trec.count()

				if countt>0:
					add=trec.aggregate(Sum('amount'))
					add = add['amount__sum']
					dl={'amount':add,'date':oydate}
					thriftrec.append(dl)

				else:
					add=trec.aggregate(Sum('amount'))
					add = add['amount__sum']
					dl={'amount':0,'date':oydate}
					thriftrec.append(dl)

				return render_to_response('thrift/merchantpayhistory.html',{'company':mybranch, 'user':varuser,'thriftrec':thriftrec,'status':mystatus})
			


				msg = 'invalide Details'
				return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

		else:
			form=viewallremittedform()
			# form=unremitform()
		return render_to_response('thrift/unremmitted.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/user/')



def cashout(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.thrift_officer==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
	


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
					myform = thriftform()
					return render_to_response('thrift/reqcash.html',{'company':mybranch,
						'user':varuser,
						'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/cashout.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')




def account_withdraw(request): 
	if request.is_ajax(): 
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')
			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
			
			if month== '-':	
				msg = 'Select a month'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

			if acccode== '-----' : 
				msg = 'Select account type'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

			try: 
				www=int(month)
				memmerchant=tblMERCHANT.objects.get(
					staff= staffdet ,status=1)
				customer=tblCUSTOMER.objects.get(
					merchant=memmerchant,
					wallet=wallet,
					status=1)
				dll = []
				paydetail=tblthrift_trans.objects.filter(
					account_type = acccode,
					wallet_type='Main', 
					merchant=memmerchant,
					branch=mybranch,
					recdate__month=www,
					customer=customer,
					avalability="Available",
					reason="Available")

				cus_thrift=tblthrift.objects.get(
					account_type = acccode,
					branch=mybranch,
					merchant=memmerchant,
					customer=customer,
					number = www)
				mythrift=cus_thrift.thrift

				for d in paydetail: 
					avalability=d.avalability
					add=paydetail.aggregate(Sum('amount'))
					add = add['amount__sum']

					num=paydetail.aggregate(Sum('number'))
					num = num['number__sum']
					jdjd= {'amount':add,'num':num,'status':avalability}

				dll.append(jdjd)
				return render_to_response('thrift/withdrr.html',{'thriftrec':dll, 'wallet':wallet,'month':www,'account_type':acccode,'thrift':mythrift})

			except : 
				transit = tblpayoutrequest.objects.filter(
					status='Unpaid',
					branch=mybranch,
					account_type=acccode,
					customer=customer,
					wallet_type='Main',
					merchant= memmerchant,
					recdate__month=www)

				job_count = transit.count()

				if job_count > 0 : 
					add=transit.aggregate(Sum('amount'))
					add = add['amount__sum']

					msg = add, 'requested'

				else : 
					paid =tblpayoutrecord.objects.filter(
						status='Paid',
						branch=mybranch,
						merchant=memmerchant,
						account_type=acccode,
						wallet_type='Main',
						recdate__month=www,
						customer=customer)
					paid_paid = paid.count()
					
					if paid_paid > 0 :

						add=paid.aggregate(Sum('amount'))
						add = add['amount__sum']
						
						msg	= add , 'Withdrawn by you'
					
					else:
						msg= 'No record found'
				
				msg=msg
				return render_to_response('thrift/selectloan.html',{'msg':msg})

		
		else: 
			return HttpResponseRedirect('/dalogin/')

	else: 
		return HttpResponseRedirect('/dalogin/')



def cashoutrequest(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		if staff.thrift_officer==0:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})
			

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			month =request.POST['month'] #month_index
			account =request.POST['account'] #account_type

			myydate = date.today() #the date the merchant made the request


			customer=tblCUSTOMER.objects.get(
				merchant=memmerchant,
				wallet=wallet,status=1)
			
			paydetail=tblthrift_trans.objects.filter(
				account_type = account,
				wallet_type='Main', 
				merchant=memmerchant,
				branch=mybranch,
				recdate__month=month,
				customer=customer,
				avalability="Available",
				reason="Available")

			ggg=paydetail.aggregate(Sum('amount'))
			ggg =ggg['amount__sum']

			

			for d in paydetail:
				code = d.code
				amount=d.amount
				daat = d.recdate

				try:
					tblpayoutrequest.objects.get(
						branch=mybranch,
						merchant=memmerchant,
						customer=customer,

						recdate=daat,
						status='Unpaid',
						amount=amount,

						account_type=account,
						wallet_type='Main',
						code=code)

				except:
					tblpayoutrequest(
						branch=mybranch,
						merchant=memmerchant,
						customer=customer,

						recdate=daat,
						status='Unpaid',
						amount=amount,
						request_date=myydate,
						account_type=account,
						wallet_type='Main',
						code=code).save()

					d.reason='requested'
					d.avalability='Not Available'
					d.save()

			return render_to_response('thrift/payoutsuccess.html',{'company':mybranch, 'tot':ggg,'user':varuser,'thriftrec':paydetail})#'tot':total})
	
	else:
		return HttpResponseRedirect('/login/user/')

def individual(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch,'user':varuser})

		if request.method == 'POST':
			form = remittalform(request.POST)
			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date']  #JavaScript Date Object

				yday,mday,dday = mydate2.split('/') 
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday) #Python Date Object

        		try:
        		    memmerchant=tblMERCHANT.objects.get(id=merchant,status=1,branch=mybranch)
        		except:
        		    form=remittalform()
        		    msg = 'INVALID MERCHANT ID'
        		    return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
        		
        		ddt=[]
        		thriftrec= tblMerchantTrans.objects.filter(
        			branch=mybranch,
        			merchant=merchant,
					recdate=mydate,
					wallet_type='Main',
					remitted='Unremmitted',
					approved='Not Approved')

        		mycount= thriftrec.count()

        		if mycount >0:
        			add=thriftrec.aggregate(Sum('amount'))
        			add = add['amount__sum']
        			dl={'amount':add}
        			ddt.append(dl)

        			return render_to_response('thrift/remhistory.html',{'company':mybranch,'dates':mydate2, 
        				'merchant':memmerchant,
        				'user':varuser,'thriftrec':ddt,
        				'date':mydate,'ttt':thriftrec})
        		
        		else:
        			msg ='NO TRANSACTION FOUND'
		else:
			form=remittalform()
			msg=''
		return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def reedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,trandate=acccode.split(':')

        	yday,mday,dday = trandate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydatwwwe=date(yday,mday,dday)

        	merchant1=tblMERCHANT.objects.get(id=merchant,status=1)
        	mybranch=merchant1.branch.id

    		ddt=[]

    		thriftrec= tblMerchantTrans.objects.filter(
    			branch=mybranch,
    			merchant=merchant1,
				recdate=mydatwwwe,
				wallet_type='Main',
				remitted='Unremmitted',
				approved='Not Approved')

    		mycount= thriftrec.count()

    		if mycount >0:
    			add=thriftrec.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			dl={'amount':add}
    			ddt.append(dl)
    			return render_to_response('thrift/remall.html',{
    				'company':mybranch,
    				'dates':trandate, 
    				'merchant':merchant1,
    				'thriftrec':ddt,
    				'date':mydatwwwe,
    				'ttt':thriftrec})
  
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')

def seedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')

    		try: 
	    		mycom = tblMerchantTrans.objects.get(id=state) #details of the trans on merchant tab

	    		return render_to_response('thrift/remtrans.html',{'income':mycom,'date1':trandate})

	    	except : 
				msg='error !!!'
				return render_to_response('thrift/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def indremitcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
        
        staffdet=staff.staffrec.id

        branch=staff.branch.id

        mycompany=staff.branch.company

        company=mycompany.name
        comp_code=mycompany.id
        
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

        if staff.cashier==0:
        	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
        
     
        if request.method == 'POST':
        	merchant=request.POST['merchant']
        	transid = request.POST['trans']
        	cash =request.POST['cash'] #posted
        	mmm =request.POST['mmm'] #carry come
        	mydate2=request.POST['date1'] #Javascript date object

        	yday,mday,dday = mydate2.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydate=date(yday,mday,dday) #python date object

        	
        	fdate= datetime.today()
        	remterr=date(fdate.year,fdate.month,fdate.day)
        	
        	weekday=mydate.isocalendar()[1]

        	ddt5=[]

        	merchanttt=tblMERCHANT.objects.get(id=merchant,status=1)

        	if mmm == cash: 

        		try: 


		    		mymy = tblMerchantTrans.objects.get(id=transid)
	        		code= mymy.code
	        		account_type=mymy.account_type
		    		cid =mymy.customer.id	    		
		    		jjf= tblCUSTOMER.objects.get(id=cid,status=1)
	        		mycom = tblMerchantTrans.objects.get(
	        			customer=jjf,
	        			recdate=mydate,
	        			id=transid)	

	        		thrrr = tblthrift.objects.get(
	        			customer=jjf,
	        			number=mday,
	        			year=yday,
	        			account_type=account_type)
	        		thrift= thrrr.thrift



	        		try:
		    			tblmerchantBank.objects.get(
		    				branch=mybranch,
		    				recdate=mydate,
		    				amount=cash,
		    				status='Remitted',
		    				customer = jjf,
		    				account_type =account_type,
		    				weekno=weekday,
		    				merchant=merchanttt,
		    				code=code)

	        		except:
	        	
		    			tblmerchantBank(
		    				branch=mybranch,
		    				recdate=mydate,
		    				amount=cash,
		    				thrift=thrift,
		    				status='Remitted',
		    				customer = jjf, 
		    				account_type =account_type,
		    				weekno=weekday,
		    				merchant=merchanttt,
		    				code=code,
		    				remitted_by = varuser,
		    				rem_date=remterr).save()

		    			mycom.delete()
			

		    			mymerchant = tblmerchantBank.objects.get(
		    				branch=mybranch,
		    				recdate=mydate,
		    				amount=cash,
		    				status='Remitted', 
		    				remitted_by = varuser,
		    				customer = jjf,
		    				weekno=weekday,
		    				merchant=merchanttt,
		    				code=code,
		    				rem_date=remterr,
		    				account_type =account_type)

		    			trans_id=mymerchant.id
		    			account_type=mymerchant.account_type

		    			
		    			thriftrec= tblMerchantTrans.objects.filter(
		    				branch=mybranch,
		    				merchant=merchanttt,
		    				recdate=mydate,
		    				wallet_type='Main',
		    				remitted='Unremmitted',
		    				approved='Not Approved')

		    			mycount= thriftrec.count()

		        		if mycount >0:
		        			add=thriftrec.aggregate(Sum('amount'))
		        			add = add['amount__sum']
		        			dl={'amount':add}
		        			ddt5.append(dl)

		        			return render_to_response('thrift/remhistory.html',{'company':mybranch,'dates':mydate2,'date':mydate,
		        				'merchant':merchanttt,'user':varuser,
		        				'thriftrec':ddt5,'ttt':thriftrec})
	        	
	    		


			        	else:
			        		return render_to_response('thrift/remsuccess_indiv.html',{'company':mybranch,
			        				'cdate':mydate2,
			        				'merchant':merchant,
			        				'account_type':account_type,
			        				'transid':trans_id,
			        				'cid':cid,
			        				'user':varuser,
			        				'total':cash})





        		except:
        			return HttpResponseRedirect('/thrift/thrift/remittals/')


      		else:
        		msg = "YOU ENTERED A WRONG FIGURE"
        		return HttpResponseRedirect("/thrift/thrift/remittals/")
        	
    else:
       	return HttpResponseRedirect('/login/user/')



def approveind(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		
		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']
			mydate2=request.POST['cdate']  #JavaScript Date Object
			cid = request.POST['cid']
			amount=request.POST['total']
			account_type=request.POST['account_type']
			transid=request.POST['transid']

			yday,mday,dday = mydate2.split('/') 
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #Python Date Object
			
			customer = tblCUSTOMER.objects.get(id =cid,status=1)
			customer1=customer.id
			mymerchant= tblMERCHANT.objects.get(id=merchant,status=1)

			myadmin = tblmerchantBank.objects.get(id = transid)

			add =myadmin.amount
			remtotal=myadmin.amount
		
			return render_to_response('thrift/approvalindv.html',{'company':mybranch,
				'merchant':mymerchant,'customer':customer1,
				'user':varuser,'date':mydate,
				'thriftrec':myadmin, 'trannsid':transid,
				'cdate':mydate2,'total':add,'rem':remtotal})

	else:
		return HttpResponseRedirect('/logout/')


def approveindividualcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
        
        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
    		return render_to_response('404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
        	merchant =request.POST['merchant']
    		mydate=request.POST['date']
    		customer=request.POST['customer'] #already a database instance
    		amount=request.POST['rem']
    		transid=request.POST['transid']

    		yday,mday,dday = mydate.split('/')

    		yday=int(yday)
        	mday=int(mday)
    		dday=int(dday)

    		transdate=date(yday,mday,dday)
    		ddt=[]

    		merchant=tblMERCHANT.objects.get(status=1,id=merchant)

    		remit = tblmerchantBank.objects.get( id = transid)

    		account_type=remit.account_type
    		code=remit.code

    		customer=tblCUSTOMER.objects.get(id=customer,status=1)
    		
    		mythrift=tblthrift.objects.get(account_type = account_type,branch=mybranch,
            	customer=customer,number=mday,year=yday)

    		customer_thrift = mythrift.thrift

    		number= remit.amount / customer_thrift
    		
    		pl= number-1
    		
    		new_amount = remit.amount - customer_thrift
    		
    		mont_contribution = tblthrift_trans.objects.filter(account_type =account_type ,wallet_type='Main', branch=mybranch,merchant=merchant,
                customer=customer,recdate__month=mday).count()
            
        	
        	if mont_contribution < 1: 
        	
        		if number == 1: 
        			tblthrift_trans(
        				account_type = account_type,
        				wallet_type='Main',
        				branch=mybranch,
                    	code=code,
                    	merchant=merchant,
                    	customer=customer,
                        number=1,
                        recdate=transdate,
                        amount=customer_thrift,
                        avalability='Not Available',
                        reason='Account Maintenance').save()

        		else : 
        			tblthrift_trans(
        				account_type = account_type,
        				wallet_type='Main',
        				branch=mybranch,
                    	code=code,
                    	merchant=merchant,
                    	customer=customer,
                        number=1,
                        recdate=transdate,
                        amount=customer_thrift,
                        avalability='Not Available',
                        reason='Account Maintenance').save()
                    
        			tblthrift_trans(
        				account_type = account_type,
        				wallet_type='Main',
        				branch=mybranch,
                    	code=code,
                    	merchant=merchant,
                    	customer=customer,
                        number=pl,
                        recdate=transdate,
                        amount=new_amount,
                        avalability='Available',
                        reason='Available').save()
                  
    		else: 
    			tblthrift_trans(
    				account_type = account_type,
    				wallet_type='Main', 
                	branch=mybranch,
                	merchant=merchant,
                	customer=customer,
                    number=number,
                    recdate=transdate,
                    amount=remit.amount,
                    code=code,
                    avalability='Available',
                    reason='Available').save()
                
    		remit.status='Approved'
    		remit.approved_by=varuser
    		remit.save()

        	return render_to_response('thrift/approve_success.html',{'company':mybranch,'tot':1,'user':varuser})

        else:
            form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})
        
    else:
        return HttpResponseRedirect('/login/user/')



def remitcash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
                    
        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

        if staff.cashier==0:
        	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
     
        if request.method == 'POST':
            merchant1 =request.POST['merchant']
            cashe1=request.POST['cash']
            amount= request.POST['amount']

            mydate1=request.POST['dates'] #JS date object
            yday,mday,dday = mydate1.split('/')
            yday=int(yday)
            mday=int(mday)
            dday=int(dday)
            mydate=date(yday,mday,dday) #python date object
            weekno=mydate.isocalendar()[1]   #week no of date         
            

            fdate= datetime.today()
            remdate=date(fdate.year,fdate.month,fdate.day)


            merchant=tblMERCHANT.objects.get(id=merchant1,status=1)
          
            if cashe1 == amount:
            	thriftrec= tblMerchantTrans.objects.filter(
            		branch=mybranch,
            		merchant=merchant,
            		recdate=mydate, #date of transaction
            		wallet_type='Main',
            		remitted='Unremmitted',
            		approved='Not Approved')

            	for k in thriftrec:
            		code=k.code
            		amount = k.amount
            		account_type=k.account_type
            		customer=k.customer.id
            		customer=tblCUSTOMER.objects.get(
            			id=customer,
            			status=1)

            		thrrr = tblthrift.objects.get(
	        			customer=customer,
	        			number=mday,
	        			year=yday,
	        			account_type=account_type)
            		thrift= thrrr.thrift

            		try:
            			tblmerchantBank.objects.get(
            				account_type=account_type, 
            				branch=mybranch,
            				recdate=mydate,
            				amount=amount,
            				customer = customer, 
            				status='Remitted', 
            				merchant=merchant,
            				code=code)
            		except:

            			tblmerchantBank(
            				account_type=account_type,
            				weekno=weekno,
            				branch=mybranch,
            				recdate=mydate,
            				amount=amount,
            				thrift=thrift,
            				status='Remitted', 
            				remitted_by = varuser,
            				rem_date=remdate,
            				customer = customer, 
            				merchant=merchant,
            				code=code).save()
            			
            			k.delete()
            		    		
            	return render_to_response('thrift/remsuccess.html',{
            		'company':mybranch,
            		'merchant':merchant.id,
            		'cdate':mydate1, #js date object
            		'user':varuser,
            		'total':cashe1})

            else:
            	return HttpResponseRedirect('/thrift/thrift/remittals/')
        else:
            form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})
        
    else:
        return HttpResponseRedirect('/login/user/')





def all(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		
		staff=Userprofile.objects.get(email=varuser,status=1)
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.filter(staff=memstaff,status=1)

		if request.method == 'POST':
			form = viewremallform(request.POST)
			if form.is_valid():
				# checkbox =request.POST['checkbox']
				mydate=form.cleaned_data['date']
				yday,mday,dday = mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				ddt=[]

				ddd= dday+1

				for d in xrange(ddd):
					if d == 0:
						pass
					else:
						mydate= date(yday,mday,d)

						for merchant in memmerchant:
							thrifing= tblMerchantTrans.objects.filter(branch=mybranch,
								recdate=mydate,wallet_type='Main',remitted='Unremmitted',merchant=merchant)
							
							mycount= thrifing.count()

							if mycount >0:
								add=thrifing.aggregate(Sum('amount'))
								add = add['amount__sum']
								dl={'date':mydate,'amount':add,'merchant':merchant,'remitted':'Unremmitted'}
								ddt.append(dl)
							else:
								pass

				return render_to_response('thrift/allrem.html',{'company':mybranch, 'user':varuser,'thriftrec':ddt,'date':mydate})

		else:
			form=viewremallform()
		return render_to_response('thrift/all.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/user/')


def report(request):
	if 'userid' in request.session:
		varuser=request.session['userid']		
		staff=Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]
								
				allmerchant = tblMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1
				
				if checkbox==1:
					if status == 'Remitted':						
						for k in allmerchant:
							thriftrec= tblmerchantBank.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Unremmitted':
						for p in allmerchant:
							thriftrec= tblMerchantTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=mydate,merchant=p)
							add =0
							
							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)
						
					return render_to_response('thrift/remreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):		
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:								
								thriftrec= tblmerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblMerchantTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

					return render_to_response('thrift/histremreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':all_data,'month':month,'year':yday,'status':status})
		
		else:
			form=viewallremittedform()
		return render_to_response('thrift/report.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/user/')



def approvalsmenu(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 

			merchant_id=request.POST['merchant']
			mydate=request.POST['date'] #js date object
			yday,mday,dday=mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)

			memmerchant=tblMERCHANT.objects.get(id=merchant_id, status=1)
			
			remit = tblmerchantBank.objects.filter( 
				branch=mybranch,
				recdate = transdate,
				merchant=memmerchant, 
				status='Remitted')


			remamount = tblmerchantBank.objects.filter( 
				branch=mybranch,
				recdate=transdate,
				merchant=memmerchant,
				status='Remitted')

			ggt=[]
		
			for k in remit:
				name=k.customer.surname + "   "+k.customer.firstname
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)
				account_type=k.account_type
			
				cus_thrift = tblthrift.objects.get(
					customer=customer,
					merchant=memmerchant,
					number = mday,
					account_type=account_type,
					year=yday)
				cus_thrift=cus_thrift.thrift
				df={'thrift':cus_thrift,'amount':k.amount,'name':name,'status':'Not Approved'}
				ggt.append(df)

			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)


			remtotal=remamount.aggregate(Sum('amount'))
			remtotal = remtotal['amount__sum']
			remtotal = int(remtotal)
		
			return render_to_response('thrift/approvalhistory.html',{
				'company':mybranch,
				 'merchant':memmerchant,
				 'user':varuser,
				 'date':transdate,
				 'thriftrec':ggt,
				 'cdate':mydate,
				 'total':add,
				 'rem':remtotal})
						
	else:
		return HttpResponseRedirect('/login/user/')

def approvecash(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
        
        staffdet=staff.staffrec.id
        branch=staff.branch.id

        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

     	if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
    		return render_to_response('404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant =request.POST['merchant']

            mydate=request.POST['date'] #JS date object
            yday,mday,dday = mydate.split('/')
            yday=int(yday)
            mday=int(mday)
            dday=int(dday)
            transdate=date(yday,mday,dday) #python date object
            
            ddt=[]
            merchant=tblMERCHANT.objects.get(status=1,id=merchant)

            remit = tblmerchantBank.objects.filter(
            	branch=mybranch,
            	merchant=merchant,
            	recdate = transdate,
            	status='Remitted')

            msg='wahalla'
            
            count=remit.count()

            for k in remit: 
            	code=k.code
            	amount=k.amount
            	customer=k.customer.id
            	account_type=k.account_type
            	customer=tblCUSTOMER.objects.get(id=customer,status=1)
            	mythrift=tblthrift.objects.get(
		        	account_type = account_type, 
		        	branch=mybranch,
		        	customer=customer, 
		        	number = mday,
		        	year=yday)
            	customer_thrift = mythrift.thrift
            	number= int(amount / customer_thrift)

            	pl= number-1
            	new_amount = amount - customer_thrift

            	mont_contribution = tblthrift_trans.objects.filter(
		        	account_type = account_type,
		        	wallet_type='Main', 
		        	branch=mybranch,
		        	merchant=merchant,
		            customer=customer,
		            recdate__month=mday).count() 

            	if mont_contribution < 1: 

            		if number == 1: 
            			msg = 'i am 1'
            			tblthrift_trans(
		                	branch=mybranch,
		                	merchant=merchant,
		                	code=code,
		                	customer=customer,
		                    number=1,
		                    recdate=transdate,
		                    amount=customer_thrift,
		                    account_type = account_type,
		                    wallet_type='Main',
		                    avalability='Not Available',
		                    reason='Account Maintenance').save()

            		elif number > 1:  
            			msg = ' i  am 2'
            			tblthrift_trans(
		                	branch=mybranch,
		                	merchant=merchant,
		                	code=code,
		                	customer=customer, 
		                	number=1,
		                	recdate=transdate,
		                	amount=customer_thrift,
		                	account_type = account_type,
		                	wallet_type='Main',
		                    avalability='Not Available',
		                    reason='Account Maintenance').save()

            			tblthrift_trans(
		                	branch=mybranch,
		                	merchant=merchant,
		                	code=code,
		                	customer=customer,
		                    number=pl,
		                    recdate=transdate,
		                    amount=new_amount,
		                    account_type = account_type,
		                    wallet_type='Main',
		                    avalability='Available',
		                    reason='Available').save()

            	elif mont_contribution > 0 : 
            		msg = 'i am 3'
            		tblthrift_trans(
		            	account_type = account_type,
		            	wallet_type='Main', 
		            	branch=mybranch,
		            	merchant=merchant,
		            	customer=customer,
		                code=code,
		                number=number,
		                recdate=transdate,
		                amount=k.amount,
		                avalability='Available',
		                reason='Available').save()

            	k.status='Approved'
            	k.approved_by=varuser
            	k.save()

            msg=msg
            # return render_to_response('thrift/selectloan.html',{'msg':msg})


            return render_to_response('thrift/apsuccess.html',{'company':mybranch,'tot':count,'user':varuser})

        else:
        	form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})

    else:
    	return HttpResponseRedirect('/login/user/')


def approvals(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant2=form.cleaned_data['merchant']
				mydate=form.cleaned_data['date']
			

				yday,mday,dday=mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				memmerchant=tblMERCHANT.objects.get(id=merchant2, status=1)

				transdate=date(yday,mday,dday)

				remit = tblmerchantBank.objects.filter(branch=mybranch,merchant=memmerchant,recdate = transdate, status='Remitted')

				remamount = tblmerchantBank.objects.filter(branch=mybranch,recdate=transdate,merchant=merchant2,status='Remitted')


				count=remit.count()
				ggt=[]

				if count>0:
					for k in remit:
						name=k.customer.surname + "   "+k.customer.firstname
						customer=k.customer.id
						customer=tblCUSTOMER.objects.get(id=customer,status=1)
						cus_thrift = tblthrift.objects.get(customer=customer,merchant=memmerchant,number = mday,year=yday)
						cus_thrift=cus_thrift.thrift
						df={'thrift':cus_thrift,'amount':k.amount,'name':name,'status':'Not Approved'}
						ggt.append(df)

					add=remit.aggregate(Sum('amount'))
					add = add['amount__sum']
					add = int(add)


					remtotal=remamount.aggregate(Sum('amount'))
					remtotal = remtotal['amount__sum']
					remtotal = int(remtotal)
				
					return render_to_response('thrift/ppp.html',{'company':mybranch,
						'account_type':account_type, 'merchant':memmerchant,'user':varuser,'date':transdate,'thriftrec':ggt,'cdate':mydate,'total':add,'rem':remtotal})
				else:
					
					return render_to_response('thrift/nilem.html',{'company':mybranch, 'user':varuser,'form':form})
		else:
			form=viewmerchantform()
		return render_to_response('thrift/approvals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})



def allapproval(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			merchant =request.POST['merchant']
			mydate=request.POST['date']
			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)
		else:
			form=viewallremittedform()
		return render_to_response('thrift/allapproval.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')



def approvereport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form  = form=viewallapprovedform(request.POST)
			status =request.POST['status']
			mydate=request.POST['date'] #javascript date object
			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			realmonth=calendar.month_name[mday]
	
			allmerchant = tblMERCHANT.objects.filter(branch=mybranch,status=1)
			remm=[]
			all_data=[]

			if 'checkbox'  in request.POST:
				checkbox=request.POST['checkbox']
			else:
				checkbox=1

			if checkbox==1:
				if status=="Approved":
					for k in allmerchant:
						thriftrec= tblmerchantBank.objects.filter(status=status, branch=mybranch,recdate=mydate,merchant=k)
						
						add=thriftrec.aggregate(Sum('amount'))
						add = add['amount__sum']

						if add > 0:
							gh={'my_merchant':k,'amount':add}
							remm.append(gh)

				elif status=="Not Approved":

					for k in allmerchant:
						thriftrec= tblmerchantBank.objects.filter(status='Remitted', branch=mybranch,recdate=mydate,merchant=k)
						
						add=thriftrec.aggregate(Sum('amount'))
						add = add['amount__sum']

						if add > 0:
							gh={'my_merchant':k,'amount':add}
							remm.append(gh)
					
				return render_to_response('thrift/appreport.html',{'company':mybranch, 'user':varuser,
					'thriftrec':remm,'date':mydate,'status':status})


			else:
				P = (monthrange(yday, mday))[-1]
				for n in range (P,0,-1):
					realdate = date(yday,mday,n)
					k =0
					if status=="Not Approved":
						for kp in allmerchant:
							thriftrec= tblmerchantBank.objects.filter(status='Remitted', branch=mybranch,recdate=realdate,merchant=kp)			
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kp,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)				
				
					elif status=="Approved":
						for kpo in allmerchant:								
							thriftrec= tblmerchantBank.objects.filter(status=status, branch=mybranch,recdate=realdate,merchant=kpo)
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kpo,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)
				
				return render_to_response('thrift/monthrep.html',{'company':mybranch, 'user':varuser,
					'thriftrec':all_data,'status':status,'month':realmonth,'year':yday})
		
	
		else:
			form=viewallapprovedform()
		return render_to_response('thrift/approvalsreport.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')


def payout(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant=form.cleaned_data['merchant']
				
				datte=form.cleaned_data['date'] #JS date Object
				yday,mday,dday = datte.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				month=calendar.month_name[mday] #month_index to month_name

				mydate=date(yday,mday,dday)

				try:
					memmerchant=tblMERCHANT.objects.get(id=merchant,status=1,branch=mybranch)
				except:
					return render_to_response('404.html',{'company':mybranch, 'user':varuser})
				ddt=[]	
				frf=[]
				allunpaid= tblpayoutrequest.objects.filter(
					merchant=memmerchant,
					branch=mybranch,
					request_date =mydate,
					wallet_type='Main',
					status='Unpaid')

				mycost=[]
				myc=[int(q.customer.id) for q in allunpaid]
				[mycost.append(x) for x in myc if x not in mycost] #removes duplicates in lost

				for kid in mycost:
					customer=tblCUSTOMER.objects.get(id = kid,status=1)

					rtpp = tblpayoutrequest.objects.filter(
						customer=customer,
						request_date=mydate,
						status='Unpaid',
						wallet_type='Main')

					custo=rtpp.aggregate(Sum('amount'))
					custo = custo['amount__sum']

					fd ={'sum':custo,'customer':customer}
					frf.append(fd)

				add = allunpaid.aggregate(Sum('amount'))
				add = add['amount__sum']
				dl={'total':add}
				ddt.append(dl)

				return render_to_response('thrift/adminpayout.html',
					{'total':ddt,
					'company':mybranch,
					'merchant':memmerchant,
					'user':varuser,
					'mydate':mydate,
					'date':datte,
					'thriftrec':frf})
			else:
				msg ='Fill up all boxes'
				
		else:
			form=viewmerchantform()
			msg=''
		return render_to_response('thrift/payout.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')





def withdrawoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')
    		customer=tblCUSTOMER.objects.get(id=state)

    		return render_to_response('thrift/adminwithdrawfund.html',{
    			'date1':trandate,
    			'customer':state,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def withdrawfunds(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer_id=request.POST['customer']
			
			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #only useful fo me to know request date

			customer=tblCUSTOMER.objects.get(id=customer_id)
			merchant=customer.merchant.id
			merchant=tblMERCHANT.objects.get(id=merchant)


			allreq = tblpayoutrequest.objects.filter(
				status='Unpaid',
				branch=mybranch,
				request_date=mydate,
				customer = customer)

			mycount=allreq.count()

			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']

			account_type_list=[]
			myc=[(str(q.account_type),q.recdate) for q in allreq]

			[account_type_list.append(x) for x in myc if x not in account_type_list] #removes duplicates in lost
			
			yyu= len(account_type_list)
			t_date= date.today()

			if yyu > 0 : 
			
				for account_type in account_type_list : 
					
					month = str(account_type[1]).split('-')[-2] #month_index
					year = str(account_type[1]).split('-')[0]
					
					request_item = tblpayoutrequest.objects.filter(
						status='Unpaid',
						branch=mybranch,
						account_type = account_type[0],
						customer = customer,
						wallet_type='Main',
						recdate=account_type[1]).delete()		

					transactions = tblthrift_trans.objects.filter(
						branch=mybranch,
						account_type = account_type[0],
						customer=customer,
						wallet_type='Main',						
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],						
						merchant=merchant).delete()


					bankk = tblmerchantBank.objects.filter(
						status= 'Approved',
						branch=mybranch,
						account_type=	account_type[0],
						wallet_type='Main',							
						merchant=merchant,
						recdate=account_type[1],
						customer=customer).delete()

				thrift = tblthrift.objects.get(
					account_type = account_type[0],
					branch = mybranch, 
					customer=customer,
					number=month,
					year=year)

				thrift_mi=int(thrift.thrift)

				transactions = tblthrift_trans.objects.get(
					account_type = account_type[0],
					wallet_type='Main', 
					branch=mybranch,
					recdate__month=month,
					avalability='Not Available',
					reason='Account Maintenance',
					customer=customer,
					merchant=merchant).delete()

				thrift.delete() 

				try : 
					tblpayoutrecord.objects.get(
						status='Paid',
						branch=mybranch,
						customer=customer,
						account_type=account_type[0],					
						paid_by=varuser,
						wallet_type='Main',					
						amount=payable_sum,
						recdate= mydate,
						merchant=merchant,
						thrift=thrift_mi)						
				except : 
					tblpayoutrecord(
						status='Paid',
						branch=mybranch,
						customer=customer,

						account_type=account_type[0],					
						paid_by=varuser,
						wallet_type='Main',					
						amount=payable_sum,
						paid_date=t_date,
						recdate=mydate,
						merchant=merchant,
						thrift=thrift_mi).save()


				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render_to_response('thrift/reqestwithdrawsuccess.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else : 
				msg = N,payable_sum, 'cash withdrawn' 
				return render_to_response('thrift/selectloan.html',{'msg':msg})
		
		else:
			return HttpResponseRedirect('/thrift/thrift/payouts/')
	else:
		return HttpResponseRedirect('/login/user/')





def canceloptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')
    		customer=tblCUSTOMER.objects.get(id=state)

    		return render_to_response('thrift/admiinpayoutoption.html',{'date1':trandate,
    			'customer':state,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def cancelreq(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer_id=request.POST['customer']
			# account_type=request.POST['account_type']
			
			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			month=calendar.month_name[mday]

			

			customer=tblCUSTOMER.objects.get(id=customer_id)
			merchant=customer.merchant.id
			merchant=tblMERCHANT.objects.get(id=merchant)

			allreq = tblpayoutrequest.objects.filter(
				status='Unpaid',
				branch=mybranch,
				request_date=mydate,
				customer = customer)
		
			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']


			account_type_list=[]
			myc=[(str(q.account_type),q.recdate) for q in allreq]
			[account_type_list.append(x) for x in myc if x not in account_type_list] #removes duplicates in lost
			yyu= len(account_type_list)


			if yyu > 0 : 
			
				for account_type in account_type_list : 
					
					month = str(account_type[1]).split('-')[-2] #month_index
					year = str(account_type[1]).split('-')[0]
					
					request_item = tblpayoutrequest.objects.filter(
						status='Unpaid',
						branch=mybranch,
						account_type = account_type[0],
						customer = customer,
						wallet_type='Main',
						recdate=account_type[1]).delete()		

					transactions = tblthrift_trans.objects.get(
						branch=mybranch,
						account_type = account_type[0],
						customer=customer,
						wallet_type='Main',					
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],						
						merchant=merchant)

					transactions.avalability='Available'
					transactions.reason='Available'
					transactions.save()


				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render_to_response('thrift/reqestcancel.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else: 
				return HttpResponseRedirect('/thrift/thrift/payouts/')

	else:
		return HttpResponseRedirect('/login/user/')





def adminpayfund(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 and staff.thrift3a_admin==0 and staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant= request.POST['merchant']
			datte=request.POST['date'] #date the request was made
			
			merchant=tblMERCHANT.objects.get(id=merchant,status=1)

			yday,mday,dday = datte.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			mydate=date(yday,mday,dday)

			month=calendar.month_name[mday]

			ddt=[]

			allunpaid= tblpayoutrequest.objects.filter(merchant=merchant,branch=mybranch,recdate=mydate,
				month=month,status='Unpaid') #request by all customers thru the merchant

			mycost=[]
			myc=[int(q.customer.id) for q in allunpaid]
			[mycost.append(x) for x in myc if x not in mycost] #Unique list of customers who request cash

			mycount= len(mycost)
			

			transactions = tblthrift_trans.objects.filter(
				account_type = 'Main account',
				wallet_type='Main', 
				merchant=memmerchant,
				branch=mybranch,
				reason='requested',
				avalability='Available',
				recdate__month=mday)
			
			code=[]
			for k in allunpaid: #Allunpaid = gross number of requests
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

				try:
					tblpayoutrecord.objects.get(branch=mybranch,merchant=merchant,customer=customer,recdate=mydate,
						amount=k.amount,status='Paid')
				except:
					tblpayoutrecord(branch=mybranch,merchant=merchant,customer=customer,amount=k.amount,status='Paid',
						recdate=mydate).save()
					code.append(int(k.code))

					k.delete()
			

			for j in transactions:
				dc=j.code
				customer=j.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

			 	for k in code:
			 		trans_code = int(k.code)
			 		code.append(trans_code)
			 		if dc==k:
			 			k.reason='Withdrawn'
			 			k.save()
			 			j.delete()

			return render_to_response('thrift/adminpayoutsuccess.html',{'count':mycount,'company':mybranch,'merchant':merchant,'user':varuser})

		else:
			form=viewmerchantform()
		return render_to_response('thrift/payout.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/user/')



def payoutreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('404.html')

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if request.method == 'POST':
			form = payoutform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]
								
				allmerchant = tblMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1
				
				if checkbox==1:
					if status == 'Paid':						
						for k in allmerchant:
							thriftrec= tblpayoutrecord.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Pending':
						for p in allmerchant:
							thriftrec= tblpayoutrequest.objects.filter(month=month,status='Unpaid', branch=mybranch,recdate=mydate,merchant=p)
							add =0
							
							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)
						
					return render_to_response('thrift/payoutdayreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'fund':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):		
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:								
								thriftrec= tblmerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblMerchantTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)


		else:
			form=payoutform()
		return render_to_response('thrift/payoutreport.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/user/')

#######******** ceo reports *********************
def repome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		return render_to_response('thrift/reporthome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')

def merchantreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		form=merchantreportform()
		return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')

def getmerchantid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)
    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allmerchants = tblMERCHANT.objects.filter(branch=branchcode, status=1)
    		
    		for j in allmerchants:
    			j = j.id
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')



def getmerchantname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblMERCHANT.objects.get(id=acccode,status=1)
    		data =data.staff.id
    		data = tblSTAFF.objects.get(id =data)
    		j = data.surname #+ " " + data.firstname+ " " + data.othername
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/user/')




def getmereportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])
                relmerchant = tblMERCHANT.objects.get(id=ID,status=1)

                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(merchant=relmerchant,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(merchant=relmerchant,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(merchant=relmerchant,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')





def cashierreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		form=cashreportform()
		return render_to_response('thrift/reportcash.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')


def getcashid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)

    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allcashier = Userprofile.objects.filter(cashier=1,status=1,branch=branchcode)
    		
    		for j in allcashier:
    			j = j.staffrec.id  #uses ID from tblSTAFF
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')

def getcashname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]

    		data=tblSTAFF.objects.get(id=acccode)
    		j = data.surname
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/user/')


def getcashreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email
              
                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')



def adminreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		form=adminreportform()
		return render_to_response('thrift/reportadmin.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')




def getadminid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)

    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		alladmin = Userprofile.objects.filter(admin=1,status=1,branch=branchcode)
    		
    		for j in alladmin:
    			j = j.staffrec.id
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')

def getadminname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblSTAFF.objects.get(id=acccode)
    		j = data.surname
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/user/')

def getadminreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email
              
                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')

def getadminreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email
              
                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(approved_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(approved_by=relcashier,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(approved_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/user/')



def customerslist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
	
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==1 : 
			client_list = tblCUSTOMER.objects.filter(branch=mybranch)
			return render_to_response('thrift/cust_list.html',{'company':mybranch,'user':varuser,'client_list':client_list})
		
		elif staff.thrift_officer== 1: 
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
			client_list = tblCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)
			return render_to_response('thrift/cust_list_merc.html',{'company':mybranch,'user':varuser,'client_list':client_list})
		else: 
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')


def switches(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0:
				return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = switchesform(request.POST)
			if form.is_valid():
				mymerchant=form.cleaned_data['merchant']
				
				merch_count = tblMERCHANT.objects.filter(branch=mybranch,status=1).count()
				if merch_count> 1: 

					try : 
						msg = 'Coming soon'
						mmme= tblMERCHANT.objects.get(branch=mybranch,status=1,id=mymerchant)
						cus_list = tblCUSTOMER.objects.filter(branch=mybranch,merchant=mmme,status=1)
						if cus_list > 0 : 
							form = newswitchform()
							return render_to_response('thrift/switchproc.html',{'company':mybranch,'user':varuser,
								'merchant':mmme,'customer':cus_list,'form':form})
						else : 
							msg = 'No customers found'
					except: 
						msg = 'Invalid ID'
				else:
					msg='YOU MUST HAVE A MINIMUM OF 2 FIELD WORKERS'
		else:
			form=switchesform()
			msg = ''
		return render_to_response('thrift/switch.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/user/')

def getallstall(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		mrp = tblMERCHANT.objects.get(id=acccode)
    		branch=mrp.branch.id
    		branch=tblBRANCH.objects.get(id=branch)
    		merc = tblMERCHANT.objects.filter(branch=branch,status=1).exclude(id=acccode)
    		kk=[]
    		kk.append('-----')
    		for jj in merc : 
    			gh =  jj.id
    			kk.append(gh)

    		return HttpResponse(json.dumps(kk), mimetype='application/json')

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')

def getbutton(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		if acccode== '-----': 
    			return render_to_response('thrift/selmerch.html')
    		
    		else: 
    			merchant=tblMERCHANT.objects.get(id=acccode)
    			return render_to_response('thrift/switchmerc.html',{'merchant':merchant})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def openoption(request):
    if request.is_ajax():
    	if request.method == 'POST':

    		if 'ggg' in request.POST : 
    			a= request.POST['ggg']

	    		# post = request.POST.copy()

	    		# acccode = post['userid']
	    		# if acccode== '-----': 
	    		return render_to_response('thrift/selmerch.html',{'sd':a})
    		
    		else: 
    		# 	merchant=tblMERCHANT.objects.get(id=acccode)
    			return render_to_response('thrift/switchmerc.html')
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')

















