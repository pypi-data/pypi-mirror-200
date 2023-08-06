import json

from e2e_cli.core.py_manager import Py_version_manager
from e2e_cli.core.alias_service import get_user_cred
from e2e_cli.core.request_service import Request
from e2e_cli.core.helper_service import Checks
from e2e_cli.core.constants import BASE_URL


def response_output(status, req):
    if Checks.status_result(status, req):
            try:
                Checks.show_json(status["data"])
                return
            except Exception as e:
                    Checks.show_json(status, e)
                    return

class ImageCrud:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if(get_user_cred(kwargs['alias'])):
            self.API_key=get_user_cred(kwargs['alias'])[1]
            self.Auth_Token=get_user_cred(kwargs['alias'])[0]
            self.possible=True
        else:
            self.possible=False
    

    def create_image(self):
        node_id = Py_version_manager.py_input("please enter node id ")
        new_image_name= Py_version_manager.py_input("please enter a name for your new image ")
        my_payload= json.dumps({
                        "name": new_image_name,
                        "type": "save_images"
                }) 
        
        while(not Checks.is_int(node_id)):
              node_id = Py_version_manager.py_input("please enter node id (integer only) ")
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/nodes/"+ node_id +"/actions/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        response_output(status, req)                
        

    def delete_image(self):
        image_id = Py_version_manager.py_input("please enter image id ")
        while(not Checks.is_int(image_id)):
              image_id = Py_version_manager.py_input("please enter image id (integer only) ")
        my_payload= json.dumps({
                        "action_type": "delete_image"
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/images/"+ image_id +"/?apikey="+API_key+"&location=Delhi"
        req="POST"
        if(Py_version_manager.py_input("Are you sure you want to delete : ").lower()=="y"):
            status=Request(url, Auth_Token, my_payload, req).response.json()

        response_output(status, req)


    def rename_image(self):
        image_id = Py_version_manager.py_input("please enter image id ")
        while(not Checks.is_int(image_id)):
              image_id = Py_version_manager.py_input("please enter image id (integer only) ")
        new_name= Py_version_manager.py_input("please enter a name for your new image ")
        my_payload= json.dumps({
                        "name": new_name,
                        "action_type": "rename"
                }) 
        
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/images/"+ image_id +"/?apikey="+API_key+"&location=Delhi"
        req="POST"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        response_output(status, req)


    def list_image(self):
        my_payload= {}
        API_key=self.API_key
        Auth_Token=self.Auth_Token
        url =  BASE_URL+"myaccount/api/v1/images/saved-images/?apikey="+API_key+"&location=Delhi"
        req= "GET"
        status=Request(url, Auth_Token, my_payload, req).response.json()

        response_output(status, req)