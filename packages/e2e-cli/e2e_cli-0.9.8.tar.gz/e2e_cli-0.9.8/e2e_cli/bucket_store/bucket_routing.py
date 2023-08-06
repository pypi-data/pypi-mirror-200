import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.bucket_store.bucket_crud.bucket_storage import bucketCrud
from e2e_cli.bucket_store.bucket_actions.bucket_actions import BucketActions

class BucketRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        
        
    def route(self):
        if (self.arguments.bucket_commands is None) and (self.arguments.action is None):
            subprocess.call(['e2e_cli', 'alias', 'bucket', '-h'])

        elif (self.arguments.bucket_commands is not None) and (self.arguments.action is not None):
              Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.bucket_commands == 'create':
            bucket_operations = bucketCrud(alias=self.arguments.alias )
            if(bucket_operations.possible):
                        try:
                            bucket_operations.create_bucket()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.bucket_commands == 'delete':
            bucket_operations = bucketCrud(alias=self.arguments.alias)
            if(bucket_operations.possible):
                        try:
                            bucket_operations.delete_bucket()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.bucket_commands == 'list':
            bucket_operations = bucketCrud(alias=self.arguments.alias)
            if(bucket_operations.possible):
                        try:
                            bucket_operations.list_bucket()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.action == 'enable_versioning':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.enable_versioning()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.action == 'disable_versioning':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.disable_versioning()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        

        elif self.arguments.action == 'create_key':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.create_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.action == 'delete_key':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.delete_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'list_key':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.list_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                            
        elif self.arguments.action == 'lock_key':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.lock_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
        
        elif self.arguments.action == 'unlock_key':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.unlock_key()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")

        elif self.arguments.action == 'add_permission':
            Bucket_operations=BucketActions(alias=self.arguments.alias)     
            if(Bucket_operations.possible):
                        try: 
                           Bucket_operations.add_permission()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
