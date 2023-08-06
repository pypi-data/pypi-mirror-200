import subprocess

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.image.image_crud.image import ImageCrud
from e2e_cli.image.image_listing.image_list import ImageListing

class ImageRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        

    def route(self):
        if (self.arguments.image_commands is None) and (self.arguments.list_by is None):
            subprocess.call(['e2e_cli', 'alias','image', '-h'])

        elif (self.arguments.image_commands is not None) and (self.arguments.list_by is not None):
              Py_version_manager.py_print("Only one action at a time !!")

        elif self.arguments.image_commands == 'create' or self.arguments.image_commands=="save":
            image_operations = ImageCrud(alias=self.arguments.alias)
            if(image_operations.possible):
                        try:
                           image_operations.create_image()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")  
                              
        elif self.arguments.image_commands == 'delete':
            image_operations = ImageCrud(alias=self.arguments.alias)
            if(image_operations.possible):
                        try:
                           image_operations.delete_image()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        elif self.arguments.image_commands == 'rename':
            image_operations = ImageCrud(alias=self.arguments.alias)
            if(image_operations.possible):
                        try:
                           image_operations.rename_image()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                                                 
        elif self.arguments.image_commands == 'list':
            image_operations = ImageCrud(alias=self.arguments.alias)
            if(image_operations.possible):
                        try: 
                           image_operations.list_image()
                        except KeyboardInterrupt:
                            Py_version_manager.py_print(" ")
                        
        # elif self.arguments.list_by == 'image_type':
        #     image_operations=ImageListing(alias=self.arguments.alias)     
        #     if(image_operations.possible):
        #                 try: 
        #                    image_operations.all()
        #                 except KeyboardInterrupt:
        #                     Py_version_manager.py_print(" ")

        else:
            Py_version_manager.py_print("command not found!!")
