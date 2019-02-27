import os
import shlex, subprocess
from Module_DeploymentMonitoring.src import config


# Return output : tuple, error : default-None
def executeBash(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    return process.communicate()


# Return True is pk is added. ELSE raise Exception
def addPublicKey(username='ec2-user',public_key=None):
    if public_key == None:
        raise Exception('Please define a public key')

    if 'ssh-rsa' not in public_key:
        public_key = 'ssh-rsa ' + public_key

    bashCommand = 'sudo bash -c "echo # ' + username + ' public key >> ' + config.SSH_KEYS_FOLDER + '"'
    bashCommand_1 = 'sudo bash -c "echo ' + public_key + ' >> ' + config.SSH_KEYS_FOLDER + '"'

    try:
        subprocess.Popen(shlex.split(bashCommand), stdout=subprocess.PIPE)
        subprocess.Popen(shlex.split(bashCommand_1), stdout=subprocess.PIPE)
    except:
        raise Exception('Unable to add public key for user ' + username)

    return {'status':True,'message':'Successfully create and added public key into account'}


# Return True is user is create. ELSE raise Exception
def addUser(username='ec2-user',public_key=None):
    try:
        bashCommand = 'sudo adduser ' + username
        executeBash(bashCommand)
    except:
        raise Exception('User ' + username + ' already exists')

    # ========================= Create .ssh folder ========================== #

    bashCommand = 'sudo mkdir /home/' + username + '/.ssh'
    executeBash(bashCommand)

    bashCommand = 'sudo chown ' + username + ':' + username + ' /home/' + username + '/.ssh'
    executeBash(bashCommand)

    bashCommand = 'sudo chmod 700 /home/' + username + '/.ssh'
    executeBash(bashCommand)

    # ===================== Create authorized_keys file ===================== #

    bashCommand = 'sudo touch /home/' + username + '/.ssh/authorized_keys'
    executeBash(bashCommand)

    bashCommand = 'sudo chown ' + username + ':' + username + ' /home/' + username + '/.ssh/authorized_keys'
    executeBash(bashCommand)

    bashCommand = 'sudo chmod 600 /home/' + username + '/.ssh/authorized_keys'
    executeBash(bashCommand)

    # ============================ Add public key =========================== #

    if public_key != None:
        return addPublicKey(username,public_key)

    return {'status':True,'message':'Successfully create a user account'}


# Return output : tuple, error : default-None
def delUser(username=None):
    if username == None:
        raise Exception('Please define a user to delete')
    elif username == 'ec2-user':
        raise Exception('Cannot delete ' + username)

    bashCommand = 'sudo userdel -r ' + username
    executeBash(bashCommand)

    return {'status':True,'message':'Successfully deleted user account'}


# Return public key : String
def getPublicKey(username=None,file_name=None,file_path=None):
    if username == None and file_name == None and file_path == None:
        raise Exception('Please define a username, file name or a file path')

    file_name = username + '.pem' if username != None else file_name
    file_path = os.path.join(config.SSH_KEYS_FOLDER,file_name) if file_name != None else file_path

    bashCommand = 'sudo ssh-keygen -y -f "' + file_path + '"'
    output,error = subprocess.Popen(shlex.split(bashCommand), stdout=subprocess.PIPE).communicate()

    return output


# Return True is successful delete. ELSE False
# def delKeyPairFile(username='ec2-user',file_name=None,file_path=None,):
#     if username == None and file_name == None and file_path == None:
#         raise Exception('Please define a username, file name or a file path')
#
#     file_name = username + '.pem' if username != None else file_name
#     file_path = os.path.join(config.SSH_KEYS_FOLDER,file_name) if file_name != None else file_path
#
#     try:
#         os.remove(file_path)
#     except:
#         return {'status':False,'message':file_path + ' does not exists'}
#
#     return {'status':True,'message':None}


# Return True is successful write. ELSE False
def writeKeyPairToFile(private_key=None,file_path=None):
    if file_path == None:
        file_path = config.SSH_KEYS_FOLDER

    try:
        with open(file_path,'w') as file:
            file.write(private_key)
    except Exception as e:
        return {'status':False,'message':e.args[0]}

    return {'status':True,'message':None}
