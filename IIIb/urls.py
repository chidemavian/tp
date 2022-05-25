from django.conf.urls import patterns, include, url


urlpatterns = patterns('IIIb.views',
	 url(r'^threeb/home/$', 'welcome'),
	 url(r'^threeb/admin/home/$', 'adminwelcome'),

	 ####m membership***************
	 url(r'^threeb/registeration/$', 'newregistration'),
	 url(r'^threeb/registeration/mass/$', 'massReg'),

	 url(r'^threeb/loans/approve/$', 'bookloan'),

	 url(r'^threeb/savings/deposit/$', 'deposit'),
	 url(r'^threeb/savings/deposit/save/$', 'save_deposit'),



	 url(r'^threeb/vas/utils/$', 'massReg'),
	 url(r'^threeb/loans/settings/$', 'loan_setup'), 
	 url(r'^threeb/staff/home/$', 'staffwelcome'), 

####*******officer request loan*******************
	url(r'^threeb/staff/request_loan/$', 'reqloan'),
	url(r'^threeb/staff/request_loan/performance/$', 'loanperformance'),
	url(r'^threeb/staff/request_loan/history/$', 'loanhistory'),

	url(r'^threeb/staff/repay_loan/$', 'repay'),

     url(r'^threeb/staff/request_loan/loan_packages/$', 'getloanpacks'),
     url(r'^threeb/staff/request_loan/individual/$', 'loandetails'),
     url(r'^threeb/staff/request_loan/apply/$', 'apply'),

     ###MISC****************************
     url(r'^threeb/staff/changepass/$', 'changepass'),
     # url(r'^threeb/staff/profile/$', 'my_Profile'),
     url(r'^threeb/loans/scenarios/$', 'loanscene'),

     url(r'^threeb/loans/repayment/$', 'optionx'),
     url(r'^threeb/staff/repay_loan/repay/$', 'yesrepayloan'),

     url(r'^threeb/loans/canceloptions/$','canceloptions'),

     url(r'^threeb/loans/withdraw/$','withdrawoptions'),
     url(r'^threeb/staff/request_loan/approve/yes/$','yesapprovaloan'),
     # url(r'^threeb/staff/request_loan/decline/yes/$','yesdecline'),
	)

