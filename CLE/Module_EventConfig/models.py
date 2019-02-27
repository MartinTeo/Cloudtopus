from django.db import models
from Module_DeploymentMonitoring.models import Server_Details

class Event_Details(models.Model):
    event_type = models.CharField(
        db_column='Event_Type',
        max_length=255,
    )
    event_startTime = models.CharField(
        db_column='Event_Start_Time',
        max_length=255,
    )
    event_endTime = models.CharField(
        db_column='Event_End_Time',
        max_length=255,
        null=True
    )
    event_recovery = models.CharField(
        db_column='Event_Recovery_Time',
        max_length=255,
        null=True
    )
    server_details = models.ForeignKey(
        Server_Details,
        on_delete= models.CASCADE,
        db_column='Server_Details',
        null=True,
    )
    class Meta:
        managed = True
        db_table = 'Event_Details'

