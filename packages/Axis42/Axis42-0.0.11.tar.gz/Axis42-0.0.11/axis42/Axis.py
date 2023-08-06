from dotenv import load_dotenv
load_dotenv()

from axis42.settings import AXIS_USER, AXIS_PASSWORD, AXIS_URL, CAMPUS_ID, LOG_FILE_PATH
from axis42.Axis_api import Axis_api
from axis42.utils import substring
from axis42.User import User

#TODO: Do some error handling functions
#TODO: Switch to a more pythonic way of doing this

def debug_message(title: str, object, log_file) -> None:
    if __debug__:
        print(title, file=log_file)
        print("-" * 20, file=log_file)
        print(str(object), file=log_file)
        print("-" * 20, file=log_file)


class Axis(object):

    def __init__(self):
        self.__axis_username: str | None = AXIS_USER # Sets axis username for authentication
        self.__axis_password: str | None = AXIS_PASSWORD # Sets axis password for authentication
        self.__axis_url: str | None = AXIS_URL # Sets campus_id for dropi
        self.__campus_id: str | None = CAMPUS_ID # Sets campus_id for dropi
        try:
            self.__log_file = open(LOG_FILE_PATH, "a") # Opens log file
        except Exception as e:
            print(e) # Prints error message if file cannot be opened
        self.axis_api = Axis_api(self.__axis_username, self.__axis_password, self.__axis_url) # Creates axis_api object
        self.__users: list[User] = [] # Creates empty list of users

    def __init_users(self) -> list[User]:
        """Gets information from axis for users and credentials, it merges them into a list of User objects

        Returns: 
            list of User objects
        """
        axis_users_list = self.axis_api.get_axis_users(refresh=True)
        axis_credential_list = self.axis_api.get_axis_credentials(refresh=True)

        debug_message("axis_users_list", axis_users_list[0], self.__log_file)
        debug_message("axis_credential_list", axis_credential_list[0], self.__log_file)
  
        ret: list[User] = []
        for axis_user in axis_users_list:
            for axis_credential in axis_credential_list:
                # Find user of token in credentials
                if axis_credential['UserToken'] == axis_user['token']:
                    lastname: str = [attribute['Value'] for attribute in axis_user['Attribute'] if attribute['Name'] == 'LastName'][0]
                    tag: str = substring(lastname, lastname.find('['), lastname.find(']') + 1)
                    login: str = substring(lastname, lastname.find(']') + 1, len(lastname)).strip(" ")
                    if len(tag) == 0:
                        print(f"User {login} has invalid lastname (No tag)")
                        continue
                    ret.append(User({
                        'login': login,
                        'tag': tag,
                        'fullname': [attribute['Value'] for attribute in axis_user['Attribute'] if attribute['Name'] == 'FirstName'][0],
                        'user_token': axis_user['token'],
                        'enabled': axis_credential['Enabled'],
                        'credential_groups': [credential_group['AccessProfile'] for credential_group in axis_credential['CredentialAccessProfile']],
                        'credential_token': axis_credential['token'],
                        'card_number': [number['Value'] for number in axis_credential['IdData'] if number['Name'] == 'CardNr'][0],
                        'axis_credential': axis_credential,
                        'axis_user': axis_user
                    }))
                    continue
        return ret

    @property
    def users(self) -> list[User]:
        """Returns all users from axis

        Returns:
            list[User]: list of User objects
        """
        if len(self.__users) == 0:
            print("Getting all users...")
            self.__users: list[User] = self.__init_users()
        return self.__users

    def get_user_by_login(self, login: str) -> User | None:
        """Find user by login in users list

        Args:
            login (str): intra login

        Returns:
            User: user found in users, None otherwise
        """
        if not login:
            return None
        users: list[User] = self.users
        for user in users:
            if user.login == login:
                return user
        print(f"User {login} not found")
        return None
    
    def get_user_by_fullname(self, fullname: str) -> User | None:
        """Find user by fullname in users list

        Args:
            fullname (str): fullname of user

        Returns:
            User: user found in users, None otherwise
        """
        users: list[User] = self.users
        for user in users:
            if user.fullname == fullname:
                return user
        print(f"User {fullname} not found")
        return None
    
    def get_user_by_id(self, user_id: int) -> User | None:
        """Find user by id in users list

        Args:
            id (str): intra user_id

        Returns:
            User: user found in users, None otherwise
        """
        users: list[User] = self.users
        for user in users:
            if user.id == user_id:
                return user
        print(f"User {user_id} not found")
        return None
    
    def get_user_by_card_number(self, card_number: str) ->  User | None:
        """Find user by his card_number in users list

        Args:
            card_number (str): card number of user in axis platform

        Returns:
            User: user found in users, None otherwise
        """
        users: list[User] = self.users
        for user in users:
            # print(f"user={user.login} card_number={user.card_number}")
            if user.card_number == card_number:
                return user
        print(f"User {card_number} not found")
        return None

    def get_user_by_user_token(self, user_token: str) -> User | None:
        """Find user by his user_token in users list

        Args:
            user_token (str): token of user in axis platform

        Returns:
            User: user found in users, None otherwise
        """
        users: list[User] = self.users
        for user in users:
            # print(f"user={user.login} user_token={user.user_token}")
            if user.user_token == user_token:
                return user
        print(f"User {user_token} not found")
        return None


    def get_user_by_credential_token(self, credential_token: str) -> User | None:
        """Find user by his credential_token in users

        Args:
            credential_token (str): token of credential in axis platform

        Returns:
            User: user found in users, None otherwise
        """
        users: list[User] = self.users
        for user in users:
            # print(f"user={user.login} credential_token={user.credential_token}")
            if user.credential_token == credential_token:
                return user
        print(f"User {credential_token} not found")
        return None
    
    def get_users_by_tag(self, tag: str) -> list[User]:
        """Find user by his tag in users

        Args:
            credential_token (str): token of credential in axis platform

        Returns:
            User: user found in users, empty list otherwise
        """
        return [user for user in self.users if user.tag == tag]

    # TODO: Test this function
    # TODO: Document this function
    def get_all_tags(self) -> list[str]:
        """Get every tag in axis platform

        Returns:
            A list of all tags in axis platform
        """
        tags: list[str] = []
        for user in self.users:
            if user.tag not in tags:
                tags.append(user.tag)
        return tags

    ########################################################################
    #                           ACTIONS                                    #
    ########################################################################

    def create_user(self, fullname: str, login: str, tag: str, card_number: str, group_name: str = "Geral") -> User | None:
        """Creates a new user in axis, set's card_number and group for the user

        Args:
            fullname (str): fullname of user
            login (str): login of user
            tag (str): tag of user
            card_number (str): card number of user
            group_name (str, optional): group name of user. Defaults to "Geral".

        Returns:
            User: user created in axis, None otherwise            
        """
        if not tag or not fullname:
            print(f"tag '{tag}' or fullname '{fullname}' cannot be empty")
            return None

        if not login:
            user_token: str = self.axis_api.create_axis_user(fullname, f"{tag}")[0]
        else:
            user_token: str = self.axis_api.create_axis_user(fullname, f"{tag} {login}")[0]
        
        print(f"Created user...")
        groups = self.axis_api.get_axis_groups()
        for group in groups:
            if group['Name'] == group_name:
                group_token = group['token']

        print(f"Setting credentials for user '{tag} {login}' with card number '{card_number}' and in group '{group_name}'")
        credential = f'{{"Enabled":true,"Status":"Enabled","IdData":[{{"Name":"CardNr","Value":"{card_number}"}},{{"Name":"PIN","Value":""}},{{"Name":"Card","Value":""}}],"ValidFrom":"","ValidTo":"","UserToken":"{user_token}","CredentialAccessProfile":[{{"AccessProfile":"{group_token}"}}]}}'
        credential_token: str = self.axis_api.set_credential(credential)
        new_credential: dict = self.axis_api.get_axis_credential_by_token(credential_token)

        user = User({
            'login': login,
            'tag': tag,
            'fullname': fullname,
            'user_token': user_token,
            'enabled': new_credential['Enabled'],
            'credential_groups': [credential_group['AccessProfile'] for credential_group in new_credential['CredentialAccessProfile']],
            'credential_token': credential_token,
            'card_number': card_number,
            'axis_credential': credential,
            'axis_user': self.axis_api.get_axis_user_by_token(user_token),
        })
        self.__users.append(user)
        return user

    def delete_user(self, user: User | str, warning: bool = True) -> None:
        """Deletes the user from axis!
        
        Args:
            user (User | str): Can be a User type which already has all the values that we need if it's a login or card_number,
            we will find the user by those values.
            warning (bool, optional): If True, will ask for input validation to delete the user. Defaults to True.
        """
        if isinstance(user, str):
            temp_user: User | None = self.get_user_by_login(user)
            if not temp_user:
                print("User not found, trying card number")
                temp_user: User | None = self.get_user_by_card_number(user)
                if not temp_user:
                    print("Card not found, I give up")
                    raise Exception("Error, User not found")
                else:
                    user: User = temp_user
            else:
                user: User = temp_user
 
        if warning:
            answer = input(f"Are you sure you want to delete user {user.login} ? [y/n] ")
            if answer.lower() in ['n', 'no', 'nao']:
                return
        self.axis_api.remove_user(user)
        self.__users.remove(user)
            

    def suspend_user(self, user: User | str, warning: bool = True) -> None:
        """Checks if user is not enabled on axis, and if it is, it will disable the user!
        
        Args:
            user (User | str): Can be a User type which already has all the values that we need. 
            If it's a login or card_number, we will find the User by those values.
            warning (bool, optional): If True, will ask for input validation to disable the user. Defaults to True.
        """
        if isinstance(user, str):
            temp_user = self.get_user_by_login(user)
            if not temp_user:
                print("User not found, trying card number")
                temp_user = self.get_user_by_card_number(user)
                if not temp_user:
                    print("Card not found, I give up")
                    raise Exception("Error, User not found")
                else:
                    user = temp_user
            else:
                user = temp_user

        if not user.enabled:
            print(f"Already disable user {user.login}")
            return

        if warning:
            answer = input(f"Are you sure you want to disable user {user.login} ? [y/n] ")
            if answer.lower() in ['n', 'no', 'nao']:
                return 
 
        print(f"Disable user {user.login}")

        credential = user.axis_credential
        credential["Enabled"] = False
        user.enabled = False
        
        credential = str(credential)
        credential = credential.replace('\'', '"')
        credential = credential.replace('False', 'false')
        credential = credential.replace(' ', '')
        
        self.axis_api.set_credential(credential)

    def enable_user(self, user: User | str, warning: bool = True) -> None:
        """Checks if user is enabled on axis, and if it's not, it will enable the user!
        
        Args:
            user (User | str): It can be a User type which already has all the values that we need.
            If it's a login or card_number, it will try to find the User by those values.
            warning (bool, optional): If True, will ask for input validation to enable the user. Defaults to True.
        """
        if isinstance(user, str):
            temp_user = self.get_user_by_login(user)
            if not temp_user:
                temp_user = self.get_user_by_card_number(user)
                if not temp_user:
                    print("Card not found, I give up")
                    raise Exception("Error, User not found")
                else:
                    user: User = temp_user
            else:
                user: User = temp_user
            

        if user.enabled:
            print(f"Already enabled user {user.login}")
            return

        if warning:
            answer = input(f"Are you sure you want to enable user {user.login} ? [y/n] ")
            if answer.lower() in ['n', 'no', 'nao']:
                return 
        print(f"Enable user {user.login}")
        credential = user.axis_credential
        credential["Enabled"] = True
        user.enabled = True

        credential = str(credential)
        credential = credential.replace('\'', '"')
        credential = credential.replace('True', 'true')
        credential = credential.replace(' ', '')
        self.axis_api.set_credential(credential)
    