
from axis42.utils import get_user_status, UserStatusEnum

class User:
    """User class, saves information about a user in Axis
    
    Properties:
        login (str): username of the user
        tag (str): tag of the user
        fullname (str): full name of the user
        user_token (str): user token of the user, every user has a unique token
        enabled (bool): True if user is enabled in Axis, False otherwise
        credential_token (str): credential token of the user, every credential has a unique token
        card_number (str): card number of the user
        axis_credential (dict): axis credential information of the user, when we make a request to Axis, they expect this format
        axis_user (dict): axis user information, when we make a request to Axis, they expect this format
        id (str): id of the user on 42 intra
        status (UserStatusEnum): status of the user on 42 intra
    """

    # TODO: Improve __init__ method documentation
    def __init__(self, user_info: dict):
        self.__login: str = user_info['login']
        self.__tag: str = user_info['tag']
        self.__fullname: str = user_info['fullname']
        self.__user_token: str = user_info['user_token']
        self.__enabled: bool = user_info['enabled']
        self.__credential_groups: list[str] = user_info['credential_groups']
        self.__credential_token: str = user_info['credential_token']
        self.__card_number: str = user_info['card_number']
        self.__axis_credential: dict = user_info['axis_credential']
        self.__axis_user: dict = user_info['axis_user']
        self.__id: str | None = None
        self.__status: UserStatusEnum | None = None

    @property
    def login(self) -> str:
        return self.__login

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def fullname(self) -> str:
        return self.__fullname

    @property
    def user_token(self) -> str:
        return self.__user_token

    @property
    def enabled(self) -> bool:
        """Returns True if user is enabled in Axis"""
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self.__enabled = enabled

    @property
    def credential_groups(self) -> list[str]:
        return self.__credential_groups

    @property
    def credential_token(self) -> str:
        return self.__credential_token

    @property
    def card_number(self) -> str:
        return self.__card_number

    @property
    def axis_credential(self) -> dict:
        return self.__axis_credential

    @property
    def axis_user(self) -> dict:
        return self.__axis_user

    @property
    def status(self) -> UserStatusEnum | None:
        if not self.__status:
            self.__id, self.__status = get_user_status(self.login)
        return self.__status

    @property
    def id(self) -> str | None:
        if not self.__id:
            self.__id, self.__status = get_user_status(self.login)
        return self.__id

    def is_student(self) -> bool:
        if self.__tag == '[42 Student]':
            return True
        return False
    
    def is_piscine(self) -> bool:
        if self.__tag == '[42 Piscine]':
            return True
        return False

    def __repr__(self):
        if not self.__login:
            return f"User(login={self.tag} {self.__fullname}, card_number={self.__card_number}, enabled={self.__enabled})"
        return f"User(login={self.tag} {self.__login}, card_number={self.__card_number}, enabled={self.__enabled})"

