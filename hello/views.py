from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import re

import email

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    # greeting = Greeting()
    # greeting.save()

    # greetings = Greeting.objects.all()
    mailData={}
    greetings=['hi','hello']
    if request.method == 'POST':
    	encodedMail=request.POST['mailHeader']
    	encodedMail=encodedMail.encode('utf-8').strip()
    	try:
    		decodedMail = email.message_from_string(encodedMail)
    		if decodedMail.keys():
    			#Find to
    			try:
    				mailData['To']=decodedMail['Delivered-To']
    			except:
    				mailData['To']="NOT ABLE TO PARSE"


    			#Find From
    			try:
    				mailData['From']=decodedMail['From']
    			except:
    				mailData['From']="NOT ABLE TO PARSE"


    			#Find senders ip
    			try:
    				for item in decodedMail['Received-SPF'].split(';'):
    					if 'client-ip' in item.lower():
    						mailData['Sender_IP']=item.split('=')[-1]
    				mailData['Sender_IP']=mailData['Sender_IP']
    			except Exception as err:
    				print (err)
    				mailData['Sender_IP']="NOT ABLE TO PARSE"

    			#Set of IPs
    			try:
    				mailData['Mail_Trace_Path']=[]
    				for item in decodedMail.keys():
    					if 'received' == item.lower():
    						mailData['Mail_Trace_Path']=mailData['Mail_Trace_Path']+re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(decodedMail[item]))

    				mailData['Mail_Trace_Path']=list(set(mailData['Mail_Trace_Path']))
    				mailData['Mail_Trace_Path']=[mailData['From']]+list(reversed(mailData['Mail_Trace_Path']))+[mailData['To']]

    			except Exception as err:
    				print (err)
    				mailData['Mail_Trace_Path']=[mailData['From']]+[mailData['To']]
    				# mailData['Mail_Trace_Path']="NOT ABLE TO PARSE"


    			#Content 
    			try:
    				mailData['Content']=''
    				if decodedMail.is_multipart():
    					for payload in decodedMail.get_payload():
    						mailData['Content']=mailData['Content']+str(payload.get_payload())
    				else:
    					mailData['Content']=str(decodedMail.get_payload())
					    

    				

    			except Exception as err:
    				print (err)
    				mailData['Content']="NOT ABLE TO PARSE"

    			

    		else:
    			return render(request, 'db.html')
    	except Exception as err:
            print (err)
            return render(request, 'db.html')
    return render(request, 'db.html',mailData)

