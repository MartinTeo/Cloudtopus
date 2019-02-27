import boto3
import traceback
from botocore.exceptions import ClientError
from Module_DeploymentMonitoring.src import config, server_util

# Get and connects to AWS SDK via boto3, client
def getClient(access_key,secret_access_key,region_name=None,service=None):
    if region_name == None:
        region_name = config.REGION_NAME

    if service == None:
        service = 'ec2'

    client = boto3.client(service,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name=region_name
    )

    return client


# Get and connects to AWS SDK via boto3, resource
def getResource(access_key,secret_access_key,region_name=None,service=None):
    if region_name == None:
        region_name = config.REGION_NAME

    if service == None:
        service = 'ec2'

    resource = boto3.resource(service,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name=region_name
    )

    return resource


# Checks if valid server
def validateServer(server_ip,server_id,access_key=None,secret_access_key=None,client=None):
    if client == None:
        client = getClient(access_key,secret_access_key)

    try:
        instances = client.describe_instances(
            InstanceIds=[
                server_id,
            ]
        )

        if server_ip == instances['Reservations'][0]['Instances'][0]['PublicIpAddress']:
            return None, True
        else:
            return "Invalid parameters. Please specify a valid ip address", False

    except ClientError as e:
        return "Invalid parameters. Please specify a valid instance id", False


# Check if valid account number
def validateAccountNumber(account_number,access_key,secret_access_key):
    client = getClient(access_key,secret_access_key,service='sts')
    try:
        account = client.get_caller_identity()
    except ClientError as e:
        raise Exception("Invalid parameters. Please specify a valid access key and secret access key.")

    return account_number == account['Account']


# Get all images from user account via Boto3
def getAllImages(account_number,access_key=None,secret_access_key=None,client=None):
    images = []

    if client == None:
        client = getClient(access_key,secret_access_key)

    try:
        images_results = client.describe_images(
            Owners=[
                account_number,
            ],
        )

        for image in images_results['Images']:
            image_id = image['ImageId']

            image_attribute_results = client.describe_image_attribute(
                Attribute='launchPermission',
                ImageId=image_id,
            )

            images.append(
                {
                    'Image_ID':image_id,
                    'Image_Name':image['Name'],
                    'Launch_Permissions':image_attribute_results['LaunchPermissions']
                }
            )

    except ClientError as e:
        raise Exception('Invalid Access_Key and Secret_Access_Key. Please key in a valid one')

    return images


# Add user to Image launch permission
def addUserToImage(image_id,account_number_list,access_key=None,secret_access_key=None,client=None):
    if client == None:
        client = getClient(access_key,secret_access_key)

    shared_response = client.modify_image_attribute(
        Attribute='launchPermission',
        ImageId=image_id,
        OperationType='add',
        UserIds=account_number_list,
    )


# Remove user from Image launch permission
def removeUserFromImage(image_id,account_number_list,access_key=None,secret_access_key=None,client=None):
    if client == None:
        client = getClient(access_key,secret_access_key)

    shared_response = client.modify_image_attribute(
        Attribute='launchPermission',
        ImageId=image_id,
        OperationType='remove',
        UserIds=account_number_list,
    )


# Stop a server via AWS
def stopServer(server_id,access_key=None,secret_access_key=None,client=None):
    if client == None:
        client = getClient(access_key,secret_access_key)

    # Do a dryrun first to verify permissions
    try:
        client.stop_instances(InstanceIds=[server_id], DryRun=True)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            raise Exception('HTTPStatusCode: 401, HTTPStatus: Unauthorized, Message: Dry run failed, Error: ' + e.args[0])

    # Dry run succeeded, call stop_instances without dryrun
    try:
        return client.stop_instances(InstanceIds=[server_id], DryRun=False)
    except Exception as e:
        raise e


# Start a server via AWS
def startServer(server_id,access_key=None,secret_access_key=None,client=None):
    if client == None:
        client = getClient(access_key,secret_access_key)

    # Do a dryrun first to verify permissions
    try:
        client.start_instances(InstanceIds=[server_id], DryRun=True)
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            raise Exception('HTTPStatusCode: 401, HTTPStatus: Unauthorized, Message: Dry run failed, Error: ' + e.args[0])

    # Dry run succeeded, call stop_instances without dryrun
    try:
        return client.start_instances(InstanceIds=[server_id], DryRun=False)
    except Exception as e:
        raise e
