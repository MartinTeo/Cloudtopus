from django.contrib import admin
from Module_DeploymentMonitoring.models import *

class AWSCredentialsAdmin(admin.ModelAdmin):
    # define which columns displayed in changelist
    list_display = ('account_number', 'access_key', #'secret_access_key',
     'image_details')
    # add filtering by date
    #list_filter = ('date',)
    # add search field 
    #search_fields = ['email', 'firstname']
    def image_details(self,obj):
        return "\n".join([image.imageId for image in  obj.imageDetails.all()])

class ImageAdmin(admin.ModelAdmin):
    list_display = ('imageName', 'imageId')


class DeploymentPackageAdmin(admin.ModelAdmin):
    list_display = ('deployment_name','deployment_link','shared_sections')

class ServerDetailsAdmin(admin.ModelAdmin):
    list_display= ('IP_address','instanceid', 'state', 'type' )
    list_filter = ('type','state')

# Register your models here.
admin.site.register(AWS_Credentials,AWSCredentialsAdmin)
admin.site.register(Image_Details,ImageAdmin)
admin.site.register(Deployment_Package,DeploymentPackageAdmin)
admin.site.register(Server_Details, ServerDetailsAdmin)
