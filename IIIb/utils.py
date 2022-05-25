
from django.core.mail import send_mail
from django.conf import settings


import smtplib, ssl






def sendMailapproveloan(receiver_email):
    messageSent = False
    subject = "Loan approval Successful"
    message = "your load has been approved"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	receiver_email,
    	fail_silently=False)
    messageSent = True



def sendMailfullypaid(receiver_email):
    messageSent = False
    subject = "Loan Repayment Complete"
    message = "your current loan is fully repaid. Thank you"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	receiver_email,
    	fail_silently=False)
    messageSent = True


def sendMailMembership(receiver_email):
    messageSent = False
    subject = "Registration Successful"
    message = "you are now a member of the cooperative. Thank you"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	receiver_email,
    	fail_silently=False)
    messageSent = True



def sendMailapplyloan(receiver_email):
    messageSent = False
    subject = "Loan application Successful"
    message = "Your application for loan is Successful. You will be notified when it gets approved"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	receiver_email,
    	fail_silently=False)
    messageSent = True



def sendMailrepayloan(receiver_email, month, year):
    messageSent = False
    subject = "Loan Repayment"
    message = "your loan is repaid for %s, %d" % (month, year)
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	receiver_email,
    	fail_silently=False)
    messageSent = True

"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and 
the number of months left or when the loan will be fully repaid 

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details
"""

