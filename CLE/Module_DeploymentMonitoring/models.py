from django.db import models

class Image_Details(models.Model):
    imageId = models.CharField(
        db_column='Image_ID',
        max_length=255,
        primary_key=True,
    )
    imageName = models.CharField(
        db_column='Image_Name',
        max_length=255,
        null = True
    )
    sharedAccNum = models.TextField(
        db_column='List_of_shared_account_number',
        null = True
    )

    class Meta:
        managed = True
        db_table = 'Image_Details'


class AWS_Credentials(models.Model):
    account_number = models.CharField(
        db_column='Account_Number',
        max_length=255,
        primary_key=True,
    )
    access_key = models.TextField(
        db_column='Access_Key',
        null= True
    )
    secret_access_key = models.TextField(
        db_column='Secret_Access_Key',
        null= True
    )
    imageDetails = models.ManyToManyField(
        Image_Details,
        db_column='Image_Details',
        null=True,
    )

    class Meta:
        managed = True
        db_table = 'AWS_Credentials'


class Server_Details(models.Model):
    SERVER_TYPE = (
        ('Parent','Parent'),
        ('Slave','Slave'),
    )

    SERVER_STATE = (
        ('Live','Live'),
        ('Pending','Pending'),
        ('Down','Down'),
    )

    IP_address = models.CharField(
        db_column='IP_Address',
        max_length=255,
        primary_key=True,
    )
    instanceid = models.CharField(
        db_column='Instance_ID',
        max_length=255,
    )
    instanceName = models.CharField(
        db_column='Instance_Name',
        max_length=255,
        null=True
    )
    state = models.CharField(
        db_column='Server_State',
        max_length=255,
        null=True,
        choices=SERVER_STATE,
    )
    account_number = models.ForeignKey(
        AWS_Credentials,
        on_delete= models.CASCADE,
        db_column='AWS_Account_Number',
        null=True,
    )
    type = models.CharField(
        db_column='Server_Type',
        max_length=255,
        null=True,
        choices=SERVER_TYPE,
    )

    class Meta:
        managed = True
        db_table = 'Server_Details'


class Deployment_Package(models.Model):
    deployment_id = models.AutoField(
        db_column='Deployment_ID',
        primary_key=True,
    )
    deployment_name = models.CharField(
        db_column='Deployment_Name',
        max_length=255,
        null=True,
    )
    deployment_link = models.TextField(
        db_column='Deployment_Link',
        null=True,
    )
    shared_sections = models.TextField(
        db_column='Shared_Sections',
        null=True,
    )
    course_section = models.ManyToManyField(
        'Module_TeamManagement.Course_Section',
        db_column='Course_Section',
        null=True,
    )

    class Meta:
        managed = True
        db_table = 'Deployment_Package'
