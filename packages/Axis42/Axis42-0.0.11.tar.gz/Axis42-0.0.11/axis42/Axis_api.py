import json
import subprocess
from axis42.User import User

class Axis_api:
    """Axis api will handle all the requests to the Axis server.
    
    Requests:
        create_axis_user: create a new axis user
        remove_user_by_token: remove a user by user token that you can get with __axis_user_list
        set_credentials: set the credentials for the user, like the card number, if the user is enabled or not     
    """

    def __init__(self, axis_username: str, axis_password: str, axis_url: str):
        self.__axis_username: str = axis_username
        self.__axis_password: str = axis_password
        self.__axis_url: str = axis_url
        self.__axis_credentials_list: list[dict] = self.__get_axis_credentials()
        self.__axis_users_list: list[dict] = self.__get_axis_users()
        self.__axis_groups_list: list[dict] = self.__get_axis_groups()


    def get_axis_credentials(self, refresh: bool = False) -> list[dict]:
        """Makes a request to the Axis server to get the list of credentials.
            
        Args:
            refresh: If the list of credentials should be refreshed.
           
        Returns:
            list of credentials
            
        """
        if refresh:
            self.__axis_credentials_list = self.__get_axis_credentials()
        return self.__axis_credentials_list

    def __get_axis_credentials(self) -> list[dict]:
        """Does curl request to axis platform to get all the credential list.
           
        Returns: 
           list of credentials
        """
        return json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{{"pacsaxis:GetCredentialList":{{}}}}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))['Credential']

    def get_axis_users(self, refresh: bool = False) -> list[dict]:
        """Makes a request to the Axis server to get the list of users.
        
        Args:
            refresh (bool): If the list of users should be refreshed.
           
        Returns:
            list of users
        """
        if refresh:
            self.__axis_users_list = self.__get_axis_users()
        return self.__axis_users_list

    def __get_axis_users(self) -> list[dict]:
        """Does curl request to axis platform to get all the users.
           
        Returns:
            list of user from axis
        """
        return json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{{"axudb:GetUserList":{{}}}}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))['User']
    
    
    def get_axis_groups(self, refresh: bool = False) -> list[dict]:
        """Makes a request to the Axis server to get the list of groups.
        
        Args:
            refresh (bool): If the list of groups should be refreshed.
           
        Returns:
            list of groups
        """
        if refresh:
            self.__axis_groups_list = self.__get_axis_groups()
        return self.__axis_groups_list

    def __get_axis_groups(self) -> list[dict]:
        """Does curl request to axis platform to get all the groups list.
           
        Returns: 
           list of groups
        """
        return json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{{"pacsaxis:GetAccessProfileList":{{}}}}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))['AccessProfile']

    def get_axis_user_by_token(self, user_token: str) -> list[dict]:
        """Does curl request to axis platform to get a specific user with a user token.
           
        Returns:
            user information
        """
        json_data: str = f'{{"axudb:GetUser":{{"Token": ["{user_token}"]}}}}'
        return json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{json_data}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))['User'][0]
    
    def get_axis_credential_by_token(self, credential_token: str) -> dict:
        """Does curl request to axis platform to get a specific credential with a credential token.
           
        Returns:
            credential information
        """
        json_data: str = f'{{"pacsaxis:GetCredential":{{"Token":["{credential_token}"]}}}}'
        return json.loads(subprocess.check_output(
            f'''curl -s '{self.__axis_url}/vapix/pacs' \
                    --digest -u '{self.__axis_username}:{self.__axis_password}' \
                    -H 'Connection: keep-alive' \
                    -H 'Content-Type: application/json' \
                    -H 'Origin: {self.__axis_url}' \
                    --data-raw '{json_data}' \
                    --compressed \
                    --insecur''',
            shell=True
        ))['Credential'][0]
    
    def create_axis_user(self, firstname: str, lastname: str) -> str:
        """Does curl request to axis platform to create a new axis user.
           
        Args:
            firstname (str): The name of the user.
            lastname (str): A tag for identification with this format [42 student], and if it's a 42 student their intra login.
        
        Returns:
            Returns the token of the created user.
        """
        return json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{{"axudb:SetUser":{{"User":[{{"Name":"{lastname}, {firstname}","Description":"","Attribute":[{{"type":"","Name":"FirstName","Value":"{firstname}"}},{{"Name":"LastName","Value":"{lastname}"}}]}}]}}}}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))['Token']


    def remove_user(self, user: User) -> None:
        """Does curl request to axis platform to remove a axis user.
           
        Args:
            firstname (str): The name of the user.
            lastname (str): A tag for identification with this format [42 student], and if it's a 42 student their intra login.

        """
        json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{{"axudb:RemoveUser":{{"Token":["{user.user_token}"]}}}}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))
    
    def set_credential(self, credential: str) -> str:
        """Does curl request to update the credentials for a user in Axis platform. 
        This can be used for enabling or disabling the user, or even create one

        Args:
            user (User): User to set the credentials for.
        
        Returns:
            Credential token generated. 
        """
        json_data: str = f'{{"pacsaxis:SetCredential":{{"Credential":[{credential}]}}}}'
        return json.loads(subprocess.check_output(
                f'''curl -s '{self.__axis_url}/vapix/pacs' \
                        --digest -u '{self.__axis_username}:{self.__axis_password}' \
                        -H 'Connection: keep-alive' \
                        -H 'Content-Type: application/json' \
                        -H 'Origin: {self.__axis_url}' \
                        --data-raw '{json_data}' \
                        --compressed \
                        --insecure''',
                shell=True
        ))['Token'][0]
    
    # Dar delete a um user no axis.
    def remove_credential(self, user: User) -> list[dict]:
        json_data = f'{{"axudb:GetUser":{{pacsaxis:RemoveCredential":{"Token":[{user.axis_credential}]}}}}}'
        return json.loads(subprocess.check_output(
            f'''curl -s 'http://10.63.249.228/vapix/pacs' \ 
                    --digest -u '{self.__axis_username}:{self.__axis_password}' \
                    -H 'Content-Type: application/json' 
                    -H 'Origin: http://10.63.249.228' 
                    -H 'Connection: keep-alive'
                    -data-raw '{json_data}'
                    --compressed 
                    --insecur''',
            shell=True
        ))

