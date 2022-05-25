from __future__ import division

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json




from loans.forms import *
from IIIb.forms import *
from IIIb.models import *
from sysadmin.models import *
from customer.models import *
from merchant.models import *
from savings.models import *

from IIIb.utils import *

import locale


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

		if staff.thrift3b_cashier==0 or staff.thrift3b_admin==0 or staff.thrift3b_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/manager.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')



def adminwelcome(request):
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


		if staff.thrift3b_officer==0 or staff.thrift3b_cashier==0 or staff.thrift3b_admin==0:
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/dashboardIIIb.html',{'company':mybranch, 'user':varuser,'pincode':staff})

	else:
		return HttpResponseRedirect('/login/')

def changepass(request):
	if 'userid' in request.session:
		varuser = request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			return HttpResponseRedirect('/login/')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if request.method=='POST':
			oldpass= request.POST['oldpass']
			newpass1=request.POST['newpass1']
			newpass2=request.POST['newpass2']

			if oldpass== staff.password :
				if newpass2 == newpass1:
					msg= 'password change successfull'
					rr=Userprofile.objects.filter(email=varuser,status=1).update(password=newpass1)
					return render_to_response('IIIb/changepass_success.html',{'user':varuser,'company':mybranch,
						'menu':staff,'msg':msg})
				else:
					msg = 'the passwords do not match'
			else:
				msg='your old pass is not correct'
		else :
			msg=''
		return render_to_response('IIIb/changepass.html',{'user':varuser,'company':mybranch,
				'menu':staff,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def massReg(request):
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
		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']

			try :


				acc_cus=tblCUSTOMER.objects.get(surname=surname,firstname=firstname,othername=othername,
					phone=phone,Address=address,wallet=wallet,code=68768,email=email,
					UX=0,branch=mybranch,merchant=memmerchant,status=1,
					online=0,sms=0,get_email=0)

				tblsavingsaccount(customer=acc_cus,branch=mybranch,UX=0,status=1,online=0,sms=0,get_email=0,withdr_status=1).save()

				return render_to_response('thrift/success.html',{'company':mybranch,'user':varuser,'wallet':wallet})

			except:
				msg = 'Incomplete phone number'

		return render_to_response('staff/massreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')




def newregistration(request):
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


		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])

			if 'photo' in request.FILES:
				photo=request.FILES['photo']
			else:
				photo = 'staff_pix/user.png'


			try:
				phone1=int(phone)


				try:
					msg = 'Eimail already in use'
					countt=tblSTAFF.objects.get(email=email,phone=phone)

				except:
					k = random.randint(0,9)
					y = random.randint(0,9)
					x = random.randint(0,9)
					z = random.randint(0,9)
					a = random.randint(0,9)
					pin =  str(k) + str(y) + str(x) + str(z)+ str(a)

					tblSTAFF(code = pin, status=1, branch=mybranch,surname=surname,
						firstname=firstname,othername=othername,
						Address=address,types='Office', phone=phone,photo=photo, email=email).save()

					new_staff = tblSTAFF.objects.get(email=email)
					name = new_staff.surname + " " + new_staff.firstname + " " + new_staff.othername


					Userprofile(branch =mybranch, password='cooperative', staffrec=new_staff,code =pin, status=1, email=email,thrift3b=1,thrift3b_officer=1).save()

					email=[email]
					sendMailMembership(email)

				return render_to_response('IIIb/success.html',{'company':mybranch,'user':varuser,'name':name})

			except:
				msg = 'Incomplete phone number'
		else:
			msg=''

		return render_to_response('IIIb/registration.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def massReg(request):
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


		if staff.thrift3a_cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/adminwelcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')




def deposit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0 or staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if request.method == 'POST':
			form = savingsform(request.POST)
			if form.is_valid():
				email=form.cleaned_data['email']
				try :

					find_staff = tblSTAFF.objects.get(email=email,branch=mybranch,status=1)
					return render_to_response('IIIb/savings.html',{'company':mybranch, 'user':varuser,'msg':find_staff})

				except:
					msg = 'Invalid email'
			else:
				msg='kindly supply staff email'

		else:
			form = savingsform()
			msg=''
		return render_to_response('IIIb/deposit.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def save_deposit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0 or staff.thrift3b_admin==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		tdate= date.today()


		if request.method == 'POST':
			form = amountform(request.POST)
			if form.is_valid():
				amount=form.cleaned_data['amount']
				email=request.POST['email']
				find_staff = tblSTAFF.objects.get(email=email,branch=mybranch,status=1)
				tblIIIbsavingsaccount(recieved_by=memstaff,branch = mybranch,
					amount=amount,email=email,rec_date=tdate).save()
				return render_to_response('IIIb/saving_success.html',{'company':mybranch, 'user':varuser,'mail':find_staff, 'amount':amount})

			else:
				msg='kindly enter amount'
				form = savingsform()
			return render_to_response('IIIb/savings.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})



	else:
		return HttpResponseRedirect('/login/')

def bookloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift3b_admin==0 or staff.thrift3b_cashier == 0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = individualform(request.POST)

			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date'] #JavaScript Date Object
			else:
				pass

		else:
			form=approveform()
			msg=''
		return render_to_response('IIIb/bookindividualloan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def loan_setup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_cashier==0 or staff.thrift3b_admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			description=request.POST['package']
			rate= request.POST['rate']
			fromm= request.POST['fromm']
			to= request.POST['to']
			pack_count=loans.count()

			if pack_count == 0 :
				tblstandardloanIIIB(rate = 0 ,description='-----', staffrec=user,branch=mybranch,status='ACTIVE',from_week=0,to_week=0).save()
				tblstandardloanIIIB(rate = rate ,description=description, staffrec=user,branch=mybranch,status='ACTIVE',from_week=fromm,to_week=to).save()
			else:
				tblstandardloanIIIB(rate = rate ,description=description, staffrec=user,branch=mybranch,status='ACTIVE',from_week=fromm,to_week=to).save()
			msg = "package added successfully"
			return render_to_response('IIIb/addpackage.html',{'company':mybranch, 'user':varuser,'msg':msg})

		return render_to_response('IIIb/set_uploan.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')


def staffwelcome(request):
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


		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('IIIb/welcome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/')




################OFFICER VIEWS****************************************
def reqloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		if request.method == 'POST':
			form = savingsform(request.POST)
			if form.is_valid():
				email=form.cleaned_data['email']
				try :

					find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
					return render_to_response('IIIb/savings.html',{'company':mybranch,
						 'user':varuser,'msg':find_staff})

				except:
					msg = 'Invalid email'
			else:
				msg='kindly supply staff email'

		else:
			form = loanreqform()

			if staff.thrift3b_cashier==1:
				return render_to_response('IIIb/req_cash_admin.html',{'company':mybranch,'name':find_staff,'user':varuser,'form':form})

			return render_to_response('IIIb/req_cash.html',{'company':mybranch,
			'name':find_staff,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')



def loanhistory(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		loan_list = tblIIIbloandapplications.objects.filter(branch=mybranch,staffrec=memstaff)

		if staff.thrift3b_cashier==0:
				return render_to_response('IIIb/loanhist.html',{'company':mybranch,
					'name':find_staff,'user':varuser,'list':loan_list})
		elif staff.thrift3b_cashier==1:
			return render_to_response('IIIb/loanhist_admin.html',{'company':mybranch,
					'name':find_staff,'user':varuser,'list':loan_list})


	else:
		return HttpResponseRedirect('/login/')



def loanperformance(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		p=[]

		try:
			loan_detail =  tblIIIbloandapplications.objects.get(status='Not Approved', branch=mybranch,	staffrec=memstaff)
			y,m,d =loan_detail.date.split("-")
			month = calendar.month_name[int(m)]

			if staff.thrift3b_cashier==0:
				return render_to_response('IIIb/not_approved.html',{'company':mybranch,
					'k':loan_detail,
					'month':month,
					'year': y,
					'user':varuser})

			elif staff.thrift3b_cashier == 1 :
				return render_to_response('IIIb/notappadmin.html',{'company':mybranch,
					'k':loan_detail,
					'month':month,
					'year': y,
					'user':varuser})

		except :

			try:
				loan_detail =  tblIIIbloandapplications.objects.get(status='Running', branch=mybranch,
					staffrec=memstaff)

				loan_pack = loan_detail.package

				trans = tblIIIbloantransaction.objects.filter(transaction_source=loan_detail)



				for k in trans:
					month= k.start_date
					year,month,day=month.split('-')
					year=str(year)
					month =str(month)
					month =int(month)
					monthnam = calendar.month_name[month]
					det = {'month':monthnam, 'year':year,'amount':k.amount,'status':k.status}
					p.append(det)


			except :
				msg = ''

			if staff.thrift3b_cashier==0:
				return render_to_response('IIIb/loanperf.html',{'p':p,'company':mybranch,'name':find_staff,'user':varuser})

			elif staff.thrift3b_cashier == 1 :
				return render_to_response('IIIb/loanperf_admin.html',{'p':p,'company':mybranch,'name':find_staff,'user':varuser})


	else:
		return HttpResponseRedirect('/login/')


def getloanpacks(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':
				post = request.POST.copy()
				acccode = post['userid']

				staff = Userprofile.objects.get(email=acccode,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
				t1= tblstandardloanIIIB.objects.filter(branch=mybranch)
				sdic={}
				kk=[]

				for j in t1:
					j = j.description
					s = {j:j}
					sdic.update(s)
					klist = sdic.values()
				for p in klist:
					kk.append(p)
				kk.sort()
			else :
				kk.append('NO LOAN PACKAGES FOUND')
			return HttpResponse(json.dumps(kk), mimetype='application/json')
		else:
			gdata = ""
			return render_to_response('index.html',{'gdata':gdata})


def loandetails(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,loan,amount=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		if amount== '':
        			msg='enter amount'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})
        		elif loan == '-----':
        			msg='select a loan package'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})

        		else :
        			pending = tblIIIbloandapplications.objects.filter(branch=mybranch,staffrec=memstaff,status='Not Approved')
        			running = tblIIIbloandapplications.objects.filter(branch=mybranch,staffrec=memstaff,status='Running')

        			if pending.count() > 0 :
        				msg='you have a pending loan request, Select history to view'
        				return render_to_response('IIIb/selectloan.html',{'msg':msg})

        			if running.count() > 0 :
        				msg='you have a running loan, fresh loans are not applicable at this moment'
        				return render_to_response('IIIb/selectloan.html',{'msg':msg})


        			det = tblstandardloanIIIB.objects.get(description=loan, branch=mybranch)
        			loan_rate = int(det.rate)
        			amount=int(amount)
        			duration = int(det.to_week)
        			thrift  = (100 + loan_rate )
        			thrift = thrift / 100
        			thrift = thrift * amount
        			thrift=  thrift / duration
        			thrift=  locale.format("%.2f",thrift,grouping=True)
        			return render_to_response('IIIb/staffbookloan.html',{'email':user,'amount':amount,'loan':loan,'duration':duration,'thrift':thrift})
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')


def apply(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.thrift3b_officer==0: # or staff.thrift3b_cashier==0  or staff.thrift3b_admin==0:
			return render_to_response('IIIb/404loan.html',{'company':mybranch, 'user':varuser})


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		if request.method == 'POST':
			thrift=request.POST['thrift']
			amount= request.POST['amount']
			package=request.POST['package']

			fdate= datetime.today()
			todayy=date(fdate.year,fdate.month,fdate.day)

			loan_package = tblstandardloanIIIB.objects.get(description=package, branch=mybranch)

			try:
				etwtwer
			except:

				tblIIIbloandapplications(branch=mybranch,staffrec=find_staff,package=loan_package,
					volume=amount,status='Not Approved', date= todayy,thrift=thrift).save()

				email = [varuser]
				sendMailapplyloan(email)

				if staff.thrift3b_cashier==1:
					return render_to_response('IIIb/booking_cashier.html',{'company':mybranch, 'user':varuser,'customer':0})
				else:
					return render_to_response('IIIb/booking_officer_success.html',{'company':mybranch, 'user':varuser,'customer':0})


	else:
		return HttpResponseRedirect('/login/')


def loanscene(request):
    if  "userid" in request.session:
        if request.is_ajax():
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,status,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		if status=='-----':
        			msg='Select loan Status'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})

        		if month=='-':
        			msg='Select valid Month'
        			return render_to_response('IIIb/selectloan.html',{'msg':msg})



        		month=int(month)
        		monthnam = calendar.month_name[month]

        		if status=='All' :
        			scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,date__month=month)
        			return render_to_response('IIIb/application.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})

        		elif status=='Approved' or status== 'Declined':
        			scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,date__month=month,status=status)
        			return render_to_response('IIIb/app_decl.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})


        		else :
        			status='Not Approved'
        			scsenario = tblIIIbloandapplications.objects.filter(branch=mybranch,date__month=month,status=status)
        			return render_to_response('IIIb/scenario.html',{'email':user,'msg':scsenario,'status':status, 'month':monthnam})
        	else:
        		gdata = ""
        		return render_to_response('index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render_to_response('lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/')





def canceloptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')
    		customer=tblSTAFF.objects.get(id=state)

    		return render_to_response('IIIb/admiinpayoutoption.html',{'date1':trandate,
    			'customer':state,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')



def withdrawoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')
    		customer=tblSTAFF.objects.get(id=state)

    		return render_to_response('IIIb/approve_opt.html',{
    			'date1':trandate,
    			'customer':state,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def yesapprovaloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		f= datetime.today()
		mday=f.day
		mmonth =f.month
		myear=f.year
		fdate=date(myear,mmonth,mday)


		if staff.thrift3b_cashier==0 or staff.thrift3b_admin==0 or staff.thrift3b_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			staff =request.POST['staff']

		 	customer=tblSTAFF.objects.get(id =staff, status=1)
		 	email=customer.email
		 	email=[email]


		 	details = tblIIIbloandapplications.objects.get(staffrec=customer,status='Not Approved',branch=mybranch)

		 	thrift=(details.thrift)
		 	duration= int(details.package.to_week)
		 	duration=duration+1
		 	volume=details.volume


		 	trans = tblIIIbloantransaction.objects.filter(transaction_source=details,start_date=fdate, status='DR',amount=thrift)
		 	trans_count= trans.count()

		 	if trans_count== 0 :
			 	for n in range (1,duration):
					mmonth+=1
					if mmonth > 12 :
						mmonth=1
						myear+=1

					fdate=date(myear,mmonth,02)

			 		tblIIIbloantransaction(transaction_source=details,start_date=fdate, status='DR',amount=thrift).save()

			 	details = tblIIIbloandapplications.objects.filter(staffrec=customer).update(status='Running')

			 	sendMailapproveloan(email)
				return render_to_response('IIIb/approve_success.html',{'company':mybranch, 'user':varuser,'sum':volume,'customer':customer})
		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')





def repay(request):
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


		if staff.thrift3b_cashier==0:
				return render_to_response('404cr.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			email=request.POST['email']
			p=[]

			try :
				memstaff = tblSTAFF.objects.get(branch=mybranch,email=email)
				lln=tblIIIbloandapplications.objects.get(staffrec=memstaff,branch=mybranch,
					status='Running')

				ltrans = tblIIIbloantransaction.objects.filter(transaction_source=lln)

				for k in ltrans:
					month= k.start_date
					year,month,day=month.split('-')
					year=str(year)
					month =str(month)
					month =int(month)
					monthnam = calendar.month_name[month]
					det = {'month':monthnam, 'year':year,'amount':k.amount,'status':k.status,'id':k.id}
					p.append(det)

				return render_to_response('IIIb/repay_hist.html',{'name':memstaff,'email':email,'company':mybranch,'user':varuser,'p':p})

			except:

				msg='no loan to repay'

				return render_to_response('IIIb/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

		else:
			msg = ''
			return render_to_response('IIIb/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def optionx(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,email=acccode.split(':')
    		myloan=tblIIIbloantransaction.objects.get(id=acccode)
    		mydate = int(myloan.start_date.split('-')[1])
    		monthnam = calendar.month_name[mydate]

    		return render_to_response('IIIb/repayopt.html',{'code':acccode,'hhh':myloan,'date':monthnam,'email':email})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def yesrepayloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		f= datetime.today()
		mday=f.day
		mmonth = f.month
		myear=f.year
		fdate=date(myear,mmonth,mday)

		if staff.thrift3b_cashier==0 or staff.thrift3b_admin==0 or staff.thrift3b_officer==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			email =request.POST['email']
			loan_code=request.POST['myid']
			myloan=tblIIIbloantransaction.objects.get(id= loan_code)
			myloan.status="CR"
			myloan.save()
			y,m,d =myloan.start_date.split("-")
			month = calendar.month_name[int(m)]
			email=[email]

			sendMailrepayloan(email,mmonth,y)

			soou = myloan.transaction_source.id
			loandet = tblIIIbloandapplications.objects.get(id=soou)

			myloancount=tblIIIbloantransaction.objects.filter(transaction_source=loandet, status="DR")

			if myloancount.count() < 1:
				tblIIIbloandapplications.objects.filter(status='Running').update(status= 'Fully Paid')
				sendMailfullypaid(email)
			return HttpResponseRedirect('/dashboard/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')


