from django.conf.urls import patterns, include, url


urlpatterns = patterns('Ib.views',
	 url(r'^thrift/home/$', 'welcome'),
	 url(r'^thrift/admin/home/$', 'adminwelcome'),
	 url(r'^thrift/admin/user/$', 'adminuserguide'),


###*************Credit officers*******************
	url(r'^staff/merchant/$', 'regcreditofficer'),
	url(r'^staff/merchant/mycos/$', 'mycos'),
	url(r'^staff/merchant/manage/$', 'managecos'),
	url(r'^staff/merchant/changestatus/$','changestatus'),
	url(r'^staff/manage/manage/$','editstaf'),

##********************Subscription***************
	 url(r'^thrift/newsub/$', 'subscribe'),
	 url(r'^thrift/newsub/subscribe/$', 'gensave'),
	  url(r'^customer1b/list/$','mylist'),


##********************Create Wallet***************

	 url(r'^thrift/editwallet/wallet/$', 'asserteditwallet'),

	 #*************** pay request********************
	 url(r'^thrift/payrequest/$', 'payrequests'),
	 url(r'^findthrift//$', 'autocomplete'),
	 url(r'^thrift/history/$', 'history'),
	 url(r'^thrift/statement/$', 'statement'),
	 url(r'^thrift/addmythrift/$','addmythrift'),


	 #*************** activity log********************

	 url(r'^thrift/log/$', 'log'),
	 url(r'^thrift/log/merchant_ajax/$', 'fillmerchant'),
	 url(r'^thrift/log/autopostlog/$', 'fillmerchantb'),

	 url(r'^thrift/log/payouts/$', 'payouts'),
	 url(r'^thrift/log/payouts/merchant_ajax/$', 'fillmerchant'),
	 url(r'^thrift/log/payouts/autopostlog/$', 'fillmerchantb'),

	 

	 url(r'^thrift/log/approvals/$', 'logapprove'),
	 url(r'^thrift/log/approvals/merchant_ajax/$', 'fillmerchantappr'),
	 url(r'^thrift/log/approvals/autopostlog/$', 'showtrans'),


	 url(r'^thrift/log/dr/$', 'log7'),
	 url(r'^thrift/log/dr/merchant_ajax/$', 'fillmerchant7'),
	 url(r'^thrift/log/dr/autopostlog/$', 'fillmerchantb7'),




	 #*************** deposit********************
	 url(r'^thrift/requests/cashin/$', 'cashin'),
	 url(r'^thrift/requests/cashin/cash/$', 'cashin_cash'),
	 url(r'^thrift/requests/cashin/agent/$', 'cashin_agent'),


	 url(r'^thrift/unremmitted/$', 'unremmitted'),
	 url(r'^thrift/user/report/$', 'userreport'),
	 url(r'^thrift/cashout/$', 'cashout'),
	url(r'^thrift/funding/getsource/$','source'),
     url(r'^thrift/requests/payout_request/$', 'cashoutrequest'),


	 #***********************8*Remittals***************
	url(r'^thrift/remittals/$', 'individual'),
	 url(r'^thrift/seedit/$','seedit'),

	url(r'^thrift/requests/adminpayfund/canceloptions/$','canceloptions'),
url(r'^thrift/requests/adminpayfund/withdraw/$','withdrawoptions'),
	 url(r'^thrift/reedit/$','reedit'),

	  # url(r'^thrift/apprvind/$','seedit'),
	   url(r'^thrift/approvall/Cashier/$','appppprooovennn'),
	   url(r'^thrift/approvall/co/$','aproveCO'),

	url(r'^thrift/remittals/remit/$', 'remitcash'),
	url(r'^thrift/remittals/individualremit/$', 'indremitcash'),
	url(r'^thrift/report/$', 'report'),
	

	#******************Approvals****************
    url(r'^thrift/approvalsmenu/$', 'approvalsmenu'),
  	url(r'^thrift/aprrovals/approvalsingletrans/$', 'approveone'),
	url(r'^thrift/approvals/approvebulk/$', 'approvebulkcash'),
    
    url(r'^thrift/approvalsmenu/approveCo/$', 'approveallco'),

    # url(r'^thrift/approvals/$', 'approvals'),
    
        url(r'^thrift/approvalsmenu/approvefund/$', 'approvecash'),
    url(r'^thrift/allapprovals/$', 'allapproval'),

	url(r'^thrift/approvals/approvereport/$','approvereport'),

	url(r'^thrift/approvalforindv/$','approveind'),
	url(r'^thrift/approvalsmenu/approvefundforcustomer/$','approveindividualcash'),

###***************************Payout***************
      url(r'^thrift/payouts/$', 'payout'),
       url(r'^thrift/requests/adminpayfund/$', 'adminpayfund'),
      url(r'^thrift/payoutreport/$', 'payoutreport'),

      url(r'^thrift/requests/adminpayfund/cancel/nos/$','cancelreq'),
      url(r'^thrift/payouts/adminwithdraw/yes/$','withdrawfunds'),


##****************General Reports***********************
      url(r'^thrift/reports/home/$', 'repome'),



##########****************##Vaults******************
      url(r'^thrift/reports/sales/merchant/$','merchantreport'),
      url(r'^thrift/reports/getmereport/$','getmereportajax'),
      url(r'^thrift/reports/getdatemereport/$','getmereportajaxdate'),



#####***********************performance*********************************
      url(r'^thrift/reports/sales/cashier/$','cashierreport'),


#####***********************profits*********************************
      url(r'^thrift/reports/sales/admn/$','adminreport'),
      url(r'^thrift/reports/getprofit/$','getprofit'),
      url(r'^thrift/reports/getdateprofit/$','getdateprofit'),


#####***********************Unaprovals*********************************
       url(r'^thrift/reports/sales/unapproved/$','unapprovals'),

#####***********************withdrawals*********************************       
        url(r'^thrift/reports/sales/withdrawwa/$','clientwithdraw'),
        url(r'^thrift/reports/getwithdraw/$','getwithdraw'),
        url(r'^thrift/reports/getdatewithdraw/$','getdatewithdraw'),




        
      		#******merchants*******
      url(r'^thrift/reports/getmerchants/$','getmerchantid'),
      url(r'^thrift/reports/getmyname/$','getmerchantname'),

      url(r'^thrift/reports/getmydate/$','getmydate113'),
      
      



      #*****Cashier**************



       url(r'^thrift/reports/getcashreport/$','getcashreportajax'),


###*****************************MISC************************
	url(r'^thrift/misc/switches/$', 'switches'),
	url(r'^thrift/misc/getstaff/$','getallstall'),
	url(r'^thrift/misc/getswitch/$','getbutton'),
	url(r'^thrift/misc/showselect/$','openoption'),

###**************sales******************************
	url(r'^thrift/sales/admin/daily/$','daily'),
	url(r'^thrift/sales/admin/weekly/$','saless'),
	url(r'^thrift/sales/admin/monthly/$','saless'),
	url(r'^thrift/sales/month_ajax/$','saless_1'), 
	url(r'^thrift/sales/admin/monthly/$','saless'),
	url(r'^thrift/sales/getmerchantid/$','getid'),
	)
