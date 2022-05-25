from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from partner.forms import *
from sysadmin.models import *
from staff.models import *
from customer.models import *
from datetime import date
import calendar
import random

from django.db.models import Max,Sum
today=date.today()





def welcome(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.partner==0:
			return render_to_response('partner/404.html')

		return render_to_response('partner/welcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')


def registration(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render_to_response('partner/404.html')
		if request.method == 'POST':
			name=request.POST['Name']
			web=request.POST['website']
			insta = request.POST['instagram']
			facebook = request.POST['facebook']
			twit= request.POST['twitter']
			youtube = request.POST['youtube']
			try:
				mycom = tblCOMPANY.objects.get(name=name)
			except:
				tblCOMPANY(engine='tts',web=web,code='43',name=name,twitter=twit,
					youtube=youtube,fb=facebook,ux=0,logo='company_logo/thrift.png',
					partner=partnerfff,ig=insta,size=20).save()
				mycom = tblCOMPANY.objects.get(name=name)

				return render_to_response('partner/busregistersuccess.html',{'company':mybranch,'user':varuser,'business':mycom})
		else:
			pass

		return render_to_response('partner/register.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/')


def branch(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render_to_response('partner/404.html')


		if request.method == 'POST':
			form = companyform(request.POST)

			if form.is_valid():
				companygg= form.cleaned_data['company']

			try:
				k = tblCOMPANY.objects.get(id =companygg,partner=partnerfff)
				try:
					br = tblBRANCH.objects.get(company=k)
					return render_to_response('partner/branch_detail.html',{'company':mybranch,'user':varuser,'comp':br})

				except:
					return render_to_response('partner/savebus.html',{'company':mybranch,'user':varuser,'comp':k})

			except :
				msg = 'Details not found'

		else:
			form = companyform()
			msg=''

		return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/')


def branch1(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render_to_response('partner/404.html')
		if request.method=='POST':
			partnerfff = tblPARTNER.objects.get(email=varuser)
			company=request.POST['company']
			k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
			return render_to_response('partner/savebus.html',{'company':mybranch,'user':varuser,'comp':k})

	else:
		return HttpResponseRedirect('/login/')




def address(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.partner==0:
			return render_to_response('partner/404.html')

		if request.method == 'POST':
			address= request.POST['address']
			phone = request.POST['phone']
			company=request.POST['company']

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])

			try:
				phone=int(phone)
			except:
				msg = 'Incomplete phone number'
				return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser})

			det=[]
			partner=tblPARTNER.objects.get(email=varuser)

			try:
				k = tblCOMPANY.objects.get(id =company,partner=partner)

				tblBRANCH(company=k,code=k.code,Address=address,phone=phone,types='Head',currency_code='NGN').save()
				bre = tblBRANCH.objects.get(company=k)
				return render_to_response('partner/branchsuccess.html',{'company':mybranch,'user':varuser,'comp':bre})
			except:
				return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser})
		else:
			form = companyform()

		return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')



def ceo(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render_to_response('partner/404.html')

		if request.method == 'POST':
			form = companyform(request.POST)
			detail =[]

			if form.is_valid():
				companygg= form.cleaned_data['company']
			try:
				k = tblCOMPANY.objects.get(id =companygg,partner=partnerfff)
				ad= tblBRANCH.objects.get(company=k)
				jk = {'name':k.name.upper(),'address':ad.Address,'id':k.id}
				detail.append(jk)
				try :
					oona = Userprofile.objects.get(branch=ad, ceo = 1)
					return render_to_response('partner/ceo_details.html',{'company':mybranch,'user':varuser,'comp':detail})
				except:
					return render_to_response('partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail})


			except :
				msg = 'Reocrd not found'
		else:
			form = companyform()
			msg = ''

		return render_to_response('partner/ceo.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')




def regceo(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render_to_response('partner/404.html')

		if request.method == 'POST':
			company=request.POST['company']
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])


			try:
				phone=int(phone)
			except:
				msg = 'Incomplete phone number'
				return render_to_response('thrift/ceoreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

			try:
				staff= tblstaff.objects.get(email=email)
				return render_to_response('partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail})
			except:
				k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
				branch= tblBRANCH.objects.get(company=k)

				tblSTAFF(branch=branch,status = 1, code=k.code,surname=surname,firstname=firstname,
					othername=othername,photo='staff-pix/user.png',email=email,
					phone=phone,Address=address,types='Field').save()

				staff= tblSTAFF.objects.get(email=email)

				Userprofile(status=1,branch=branch,code=k.code,ceo=1,
					staffrec=staff,password=12345,email=email).save()

				tblapp(branch=branch,partner=partnerfff).save()

				return render_to_response('partner/ceosuccess1.html',{'company':mybranch,'user':varuser,'comp':branch})
	else:
		return HttpResponseRedirect('/login/')


def ceo1(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render_to_response('partner/404.html')

		detail=[]

		if request.method == 'POST':
			company= request.POST['company']
			k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
			ad= tblBRANCH.objects.get(company=k)
			jk = {'name':k.name.upper(),'address':ad.Address,'id':k.id}
			detail.append(jk)
			return render_to_response('partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail})
	else:
		return HttpResponseRedirect('/login/')



def app(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render_to_response('partner/404.html')

		if request.method == 'POST':
			form = branchform(request.POST)
			myy =[]

			if form.is_valid():
				branch= form.cleaned_data['branch']
			try:
				ad = tblBRANCH.objects.get(id =branch)
				cid = ad.company.id
				company=tblCOMPANY.objects.get(id=cid,partner=partnerfff)

				try:
					apps = tblapp.objects.get(branch=ad,partner=partnerfff)


					if apps.thrift1a is True:
						dc= 'checked'

					else:
						dc='unchecked'

					if apps.thrift1b is True:
						gs= 'checked'
					else:
						gs='unchecked'



					if apps.loan1b is True:
						glm= 'checked'
					else:
						glm='unchecked'


					if apps.thrift3a is True:
						mcc= 'checked'
					else:
						mcc='unchecked'

					if apps.thrift3b is True:
						mcp='checked'
					else:
						mcp='unchecked'
					if apps.loan3b is True:
						lcp='checked'
					else:
						lcp='unchecked'

					s= { 'name':ad.company.name.upper(),'address':ad.Address,
					'id':ad.id,'dc':dc,'gs':gs,'glm':glm,'mcc':mcc, 'mcp':mcp,'lcp':lcp}

					myy.append(s)

					return render_to_response('partner/applist.html',{'company':mybranch,'user':varuser,'list':myy})
				except:
					msg='jkgk'

			except:
				msg ='Details not found'
				return render_to_response('partner/app.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		else:
			form = branchform()
			msg =''

		return render_to_response('partner/app.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def app_update(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)


		if staff.partner==0:
			return render_to_response('partner/404.html',{'company':mybranch, 'user':varuser})

 #Thrifts*********************
 		if request.method=='POST' :
 			branch_code= request.POST['branch']
 			branch = tblBRANCH.objects.get(id=branch_code)

 			# memstaff=tblSTAFF.objects.get(branch=branch,email=varuser)

 			sub = []
 			unsub=[]
 			oldd = tblapp.objects.get(branch=branch)


			k = random.randint(0,9)
			y = random.randint(0,9)
			x = random.randint(0,9)
			z = random.randint(0,9)
			a = random.randint(0,9)
			pin =  str(k) + str(y) + str(x) + str(z)+ str(a)


 			######*****************#daily contribution*****************8

			if 'dc' in request.POST:
				dc=request.POST['dc']
				tblapp.objects.filter(branch=branch).update(thrift1a=1)
				tblCUSTOMER.objects.filter(branch=branch, status=1).update(dc=1)

				Userprofile.objects.filter(branch = branch).update(thrift1a=1)
				ceo = Userprofile.objects.get(branch = branch, ceo=1)
				ceo.admin=1
				ceo.cashier=1
				ceo.save()
				ceo_staff= ceo.staffrec.id
				ceo_staff=tblSTAFF.objects.get(id=ceo_staff)

				sdr = tblMERCHANT.objects.filter(branch=branch, staff=ceo_staff, status=1).count()
				if sdr < 1 :
					tblMERCHANT(branch=branch, code=pin, staff= ceo_staff ,status=1,thrift1a=1).save()

				tblMERCHANT.objects.filter(branch=branch).update(thrift1a=1)


			else:
				Userprofile.objects.filter(branch = branch).update(thrift1a=0)
				Userprofile.objects.filter(branch = branch, ceo=1).update(admin=0,cashier=0)
				tblapp.objects.filter(branch=branch).update(thrift1a=0)
				tblMERCHANT.objects.filter(branch=branch).update(thrift1a=0)
				tblCUSTOMER.objects.filter(branch=branch, status=1).update(dc=0)

				#### handl the entry at tblmerhant


###########Ib savings Variable thrift*****************************
			if 'gs' in request.POST:
				gs=request.POST['gs']
				Userprofile.objects.filter(branch = branch).update(thrift1b=1)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift1b_admin=1,thrift1b_cashier=1,thrift1b_officer=1)
				tblapp.objects.filter(branch=branch).update(thrift1b=1)
				tblCUSTOMER.objects.filter(branch=branch, status=1).update(ivb=1)

			else:
				Userprofile.objects.filter(branch = branch).update(thrift1b=0)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift1b_admin=0,thrift1b_cashier=0,thrift1b_officer=0)
				tblapp.objects.filter(branch=branch).update(thrift1b=0)
				tblCUSTOMER.objects.filter(branch=branch, status=1).update(ivb=0)

###########loan* for variable thrift******************

			if 'glm' in request.POST:
				glm=request.POST['glm']
				Userprofile.objects.filter(branch = branch).update(loan1b=1)
				tblapp.objects.filter(branch=branch).update(loan1b=1)

			else:
				Userprofile.objects.filter(branch = branch).update(loan1b=0)
				tblapp.objects.filter(branch=branch).update(loan1b=0)



			if 'mcc' in request.POST:
				mcc=request.POST['mcc']
				Userprofile.objects.filter(branch = branch).update(thrift3a=1)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3a_admin=1,thrift3a_cashier=1)
				tblapp.objects.filter(branch=branch).update(thrift3a=1)


			else:
				Userprofile.objects.filter(branch = branch).update(thrift3a=0)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3a_admin=0,thrift3a_cashier=0)
				tblapp.objects.filter(branch=branch).update(thrift3a=0)


			if 'mcp' in request.POST:
				mcp=request.POST['mcp']
				Userprofile.objects.filter(branch = branch).update(thrift3b=1)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3b_admin=1,thrift3b_cashier=1,thrift3b_officer=1)
				Userprofile.objects.filter(branch = branch).update(thrift3b_officer=1)
				tblapp.objects.filter(branch=branch).update(thrift3b=1)
			else:
				Userprofile.objects.filter(branch = branch).update(thrift3b=0)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3b_admin=0,thrift3b_cashier=0,thrift3b_officer=0)
				Userprofile.objects.filter(branch = branch).update(thrift3b_officer=0,thrift3b_cashier=0)
				tblapp.objects.filter(branch=branch).update(thrift3b=0)

			if 'lcp' in request.POST:
				dc=request.POST['lcp']
				Userprofile.objects.filter(branch = branch).update(loan3b=1)
				tblapp.objects.filter(branch=branch).update(loan3b=1)
			else:
				Userprofile.objects.filter(branch = branch).update(loan3b=0)
				tblapp.objects.filter(branch=branch).update(loan3b=0)

			neww = tblapp.objects.get(branch=branch)


			if oldd.thrift1a == 0 :
				if neww.thrift1a == 1 :
					msg1 = 'Thrift1a'
					sub.append(msg1)
			else :
				if neww.thrift1a == 0 :
					msg1 = 'Thrift1a'
					unsub.append(msg1)


			if oldd.thrift1b == 0 :
				if neww.thrift1b == 1 :
					msg1 = 'Thrift1b'
					sub.append(msg1)
			else :
				if neww.thrift1b == 0 :
					msg1 = 'Thrift1b'
					unsub.append(msg1)



			if oldd.loan1b == 0 :
				if neww.loan1b == 1 :
					msg1 = 'Loan1b'
					sub.append(msg1)
			else :
				if neww.loan1b == 0 :
					msg1 = 'Loan1b'
					unsub.append(msg1)



			if oldd.thrift3a == 0 :
				if neww.thrift3a == 1:
					msg1 = 'Thrift3a'
					sub.append(msg1)
			else :
				if neww.thrift3a == 0 :
					msg1 = 'Thrift3a'
					unsub.append(msg1)

			if oldd.thrift3b == 0 :
				if neww.thrift3b == 1 :
					msg1 = 'Thrift3b'
					sub.append(msg1)
			else :
				if neww.thrift3b == 0 :
					msg1 = 'Thrift3b'
					unsub.append(msg1)

			if oldd.loan3b == 0 :
				if neww.loan3b == 1 :
					msg1 = 'loan3b'
					sub.append(msg1)
			else :
				if neww.loan3b == 0 :
					msg1 = 'loan3b'
					unsub.append(msg1)



			return render_to_response('partner/app_update_success.html',{'company':branch,
				'user':varuser,
				'unsub':unsub,
				'comp':branch,
				'sub':sub})

	else:
		return HttpResponseRedirect('/login/')


def app1(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render_to_response('partner/404.html')


		detail=[]

		if request.method == 'POST':
			company= request.POST['company']
			k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
			ad= tblBRANCH.objects.get(company=k)
			appr = tblapp.objects.get(branch=ad)
			jk = {'name':k.name.upper(),'address':ad.Address,'id':k.id}
			detail.append(jk)
			return render_to_response('partner/app.html',{'company':mybranch,'user':varuser,'comp':detail})
	else:
		return HttpResponseRedirect('/login/')

