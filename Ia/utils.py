

from django.conf import settings
from django.shortcuts import render_to_response
from django.core.mail import send_mail

import smtplib, ssl


from staff.models import *
from Ia.models import *
from datetime import *
from django.db.models import Max,Sum
from calendar import monthrange



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# send_mail(
# 	subject,
# 	message,
# 	EMAIL_HOST_USER,
# 	[recepient],
# 	fail_silently = False)




##Sending alternative content types
def customer_activationIaa(emails):
    subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def another_one(receiver_email,wallet,account,thrift,month,year):
    plaintext = get_template('Ia/email.txt')
    htmly     = get_template('Ia/deposit_email.html')

    d = Context({ 'email': email,
        'wallet': wallet,
        'account': account,
        'thrift': thrift,
        'month': month,
        'year': year })

    subject = 'ACCOUNT CREDITED SUCCESFULLY'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def rrt(receiver_email):
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()



def customer_activationIa(receiver_email):
    messageSent = False
    subject = "Daily Contribution activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED FOR DAILY CONTRIBUTION"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True





def register_field_officerIa(receiver_email):
    messageSent = False
    subject = "Field officer activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED AS A FIELD OFFICER"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True


def Direct_creditingIa(receiver_email):
    messageSent = False
    subject = "ACCOUNT CREDITED SUCCESSFULLY"
    message = "YOUR ACCOUNT HAS BEEN CREDITED SUCCESFULLY"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	[receiver_email],
    	fail_silently=False)
    messageSent = True


def direct_depositIa(receiver_email):
    messageSent = False
    subject = "ACCOUNT CREDITED SUCCESSFULLY"
    message = "YOUR ACCOUNT HAS JUST BEEN CREDITED SUCCESFULLY"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True


def direct_withrawalIa(receiver_email):
    messageSent = False
    subject = "CASH WITHDRAWAL SUCCESSFUL"
    message = "YOU HAVE SUCCESFULLY WITHDRAWN FROM YOUR ACCOUNT"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = Truee



def selenco(bra,fd,td):


    mybranch= tblBRANCH.objects.get(id = bra)
    allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1,thrift1a=1)

    dday,mday,yday = fd.split('/') #JSON Dates Object
    yday=int(yday)
    fmday=int(mday)
    fday=int(dday)

    fd=date(yday,fmday,fday)

    dday,mday,yday = td.split('/') #JSON Dates Object
    yday=int(yday)
    tmday=int(mday)
    tday=int(dday)


    td=date(yday,tmday,tday)


    if fmday <= tmday:
        a = range(fmday,tmday+1)
    else:
        a = range(tmday,fmday+1)

        fd=date(yday,tmday,tday)

        td=date(yday,fmday,fday)


    if fmday == tmday:
        if fday < tday:
            dddd=tday #to date
            tttt=fday #from date

        elif tday<fday:
            dddd=fday
            tttt=tday
        else:
            dddd =tttt=fday


    detli=[]
    toot=0


    if fd.year== td.year:

        merchant_sales=0
        for k in a: # a is the months covered in the search
            if k == a[0]: #if month is the first month
                if k == a[-1]: #use the boundaries set by the dates
                    # dddd = td.day
                    # tttt = fd.day
                    fff=0
                    fff= fff + tttt
                    while fff <= dddd :
                        fd1=date(yday,k,fff)
                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()

                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr

                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1

                else: #boundaries = from_date to month end

                    fff=0
                    fff= fff+ fd.day
                    dddd = (monthrange(fd.year, fd.month))[-1]

                    while fff <= dddd :
                        fd1=date(yday,k,fff) #k is month integer

                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()
                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr

                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1

            else:
                if k == a[-1]: #boundaries = 1st to to_date
                    dddd = td.day

                    fff=1
                    fff += 1
                    while fff <= dddd :
                        fd1=date(yday,k,fff)
                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()
                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr
                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1

                else: # loop thru the whole month

                    fff=0
                    fff += 1
                    dddd= (monthrange(td.year, k))[-1]

                    while fff <= dddd :
                        fd1=date(yday,k,fff)
                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()
                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr

                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1


        if detli !=[] :
            ddd= {'total':toot}
            detli.append(ddd)


        return detli



"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and
the number of months left or when the loan will be fully repaid

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details. This is called MIME emails.........woooow
"""

