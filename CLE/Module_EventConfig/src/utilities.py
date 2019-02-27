from Module_TeamManagement.src.utilities import encode,decode
from Module_DeploymentMonitoring.src import aws_util
from CLE.settings import EVENT_SECRET_KEY
import hashlib
from Module_EventConfig.models import *
from Module_DeploymentMonitoring.models import Server_Details
from datetime import datetime
import pytz
import traceback

'''
prepares log for event creation
'''
def writeEventLog(event_type, server_ip ):
    try:
        tz = pytz.timezone('Asia/Singapore')
        now = str(datetime.now(tz=tz))[:19]
        serverDetails = Server_Details.objects.get(IP_address=server_ip)
        event_Entry = Event_Details.objects.create(
            event_type=event_type,
            server_details=serverDetails,
            event_startTime=now,
        )
        event_Entry.save()
    except: 
        traceback.print_exc()
    
    return "True"


'''
Method to record recovery time based on IP as well as start recording the initial start time of the IP
Called by student server
'''
def writeRecoveryTime(ipAddress):   
    
    tz = pytz.timezone('Asia/Singapore')
    now = str(datetime.now(tz=tz))[:19]
    try :
        eventList = Event_Details.objects.filter(server_details=ipAddress,event_type="stop").order_by("id").reverse()
        event = eventList[0]
        event.event_endTime = now
        event.event_recovery= recoveryTimeCaclulation(event.event_startTime , now)
        event.save()
        server = Server_Details.objects.get()

    except:
        pass
        
    
# return in minutes
def recoveryTimeCaclulation(start_Time, end_Time):
    return  (datetime.strptime(end_Time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_Time, '%Y-%m-%d %H:%M:%S')).total_seconds()/60

def hashPlainText(plaintext):
    plaintext_byte = plaintext.encode('utf-8')
    hashedtext = hashlib.sha256(plaintext_byte).hexdigest()
    return hashedtext

def validate(secret_key):
    if hashPlainText(secret_key) != EVENT_SECRET_KEY:
        return False
    return True