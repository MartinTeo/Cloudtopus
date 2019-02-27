import json
import boto3
import traceback
from datetime import datetime
import requests as req
from background_task import background
from Module_DeploymentMonitoring.models import *
from Module_DeploymentMonitoring.src import aws_util
from Module_TeamManagement.src.utilities import encode,decode
from Module_EventConfig.src import utilities

@background(schedule=0)
def test_tasks(message):
    print(message)


@background(schedule=0)
def stopServer(server_list=None,server=None,section_numbers=None,server_type=None):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] : Running background event: Stop Server')

    if server != None and server_list != None:
        server_list.append(server)
    elif server != None and server_list == None:
        server_list = [server]

    counter = 1
    for server in server_list:
        credentialsObj = AWS_Credentials.objects.get(account_number=server['server_account'])
        access_key = decode(credentialsObj.access_key)
        secret_access_key = decode(credentialsObj.secret_access_key)

        results = aws_util.stopServer(server['server_id'],access_key,secret_access_key)

        if results != None:
            print('Debug: ' + str(results['StoppingInstances'][0]['CurrentState']['Code']))

        if results['StoppingInstances'][0]['CurrentState']['Code'] == 64:
            utilities.writeEventLog("stop", server['server_ip'] )
            print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(counter) + '. Successfully stopped ' + str(server_type) + ' server: ' + server['server_ip'])
        else:
            print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(counter) + '. Unsuccessfully stopped ' + str(server_type) + ' server: ' + server['server_ip'])
        counter += 1

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] : Ending background event: Stop Server')


@background(schedule=0)
def stopWebApplication(server_list=None,server=None,section_numbers=None,server_type=None):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] : Running background task: Stop Web App')

    if server != None and server_list != None:
        server_list.append(server)
    elif server != None and server_list == None:
        server_list = [server]

    counter = 1
    for server in server_list:
        server_ip = server['server_ip']

        server_url = 'http://' + server_ip + ':8999/event/stop/deployment/'
        payload = {'port_number':8000}

        try:
            server_response = req.get(server_url, params=payload, timeout=3)
            server_jsonObj = json.loads(server_response.content.decode())

            if server_jsonObj['HTTPStatusCode'] == 200:
                print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(counter) + '. Successfully stopped ' + str(server_type) + ' web app: ' + server['server_ip'])
            else:
                httpStatus = server_jsonObj['HTTPStatus']
                print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(counter) + '. Unsuccessfully stopped ' + str(server_type) + ' web app: ' + server['server_ip'] + ' due to ' + httpStatus)

        except req.exceptions.ConnectTimeout:
            print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + str(counter) + '. Unsuccessfully stopped ' + str(server_type) + ' web app: ' + server['server_ip'] + ' due to a connection timeout')

        counter += 1

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] : Ending background event: Stop Web App')


@background(schedule=0)
def dosAttack(server_list=None,server=None,section_numbers=None):
    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] : Running background task: DDOS Attack')

    # If sending to one server
    if server !=  None:
        pass

    # If sending to  multiple servers
    if server_list != None:
        pass

    print('[' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] : Ending background event: DDOS Attack')
