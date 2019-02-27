# A router to control all database operations on models in the

class TMRouter:
    list_of_applications = [
        'Module_Account',
        'Module_EventConfig',
        'Module_TeamManagement',
        'Module_DeploymentMonitoring',
        'Module_CommunicationManagement'
    ]

    # Attempts to read Module_TeamManagement models, got to CLE_Data
    def db_for_read(self, model, **hints):
        if model._meta.app_label in TMRouter.list_of_applications:
            return 'CLE_Data'
        return None


    # Attempts to write Module_TeamManagement models, got to CLE_Data
    def db_for_write(self, model, **hints):
        if model._meta.app_label in TMRouter.list_of_applications:
            return 'CLE_Data'
        return None


     # Allow relations if a model in the Module_TeamManagement app is involved
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in TMRouter.list_of_applications or \
            obj2._meta.app_label in TMRouter.list_of_applications:
            return True
        return None


      # Make sure the Module_TeamManagement app only appears in the 'CLE_Data' database
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in TMRouter.list_of_applications:
            return db == 'CLE_Data'
        return None
