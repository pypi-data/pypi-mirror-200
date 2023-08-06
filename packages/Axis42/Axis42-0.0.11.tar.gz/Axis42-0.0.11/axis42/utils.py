from datetime import datetime, date
from axis42.settings import CAMPUS_ID
import dropi
from enum import Enum
from pprint import pprint as pp

class UserStatusEnum(Enum):
    """ UserStatusEnum class is defined that has several predefined user statuses 
    like ACTIVE, BLACKHOLED, etc.
    """
    ACTIVE = 0,
    BLACKHOLED = 1,
    DESERTER = 2,
    AGU = 3

# https://www.scrapingbee.com/curl-converter/python/ MELHOR WEBSITE DE SEMPRE
max_poolsize: int = 7

api = dropi.Api42()
dropi.config.max_poolsize = max_poolsize

def substring(string, start, end) -> str:
    if end < start or start < 0 or end < 0 or start > len(string): 
        return ""
    return string[start:end]

def is_deserter(user: dict) -> bool:
    """Check if user is deserter, compares blackholed_at with today date and if end_a
    
    Args:
        user (User): User info with key value 'blackholed_at'
    
    Returns:
        True if user is blackholed, False otherwise
    """
    # Convert date from blackholed_at to year-month-day format
    if user['end_at'] == None:
        return False
    blackholedAt = datetime.strptime(user['blackholed_at'][:10], "%Y-%m-%d")
    endAt = datetime.strptime(user['end_at'][:10], "%Y-%m-%d")

    return endAt.date() < blackholedAt.date() and blackholedAt.date() < date.today()


# TODO: Improve this function documentation
def is_blackholed(blackholed_at) -> bool:
    """Check if user is blackholed, compares blackholed_at with today date

    Args:
        blackholed_at: User info with key value 'blackholed_at'
    
    Returns:
        True if user is blackholed, False otherwise
    """
    # Convert date from blackholed_at to year-month-day format
    blackholedAt = datetime.strptime(blackholed_at[:10], "%Y-%m-%d")
    return blackholedAt.date() < date.today()

def is_frozen(user_id: int) -> bool:
    """Check if user is frozen
    
    Args:
        user_id (int): id from user
    
    Returns:
        True if user is Frozen, False otherwise
    """
    # Get all AGU capsules that are not [free'd ?] used from user
    antiGravUsers = api.get(f'anti_grav_units_users?filter[user_id]={user_id}&filter[is_free]=false')
    if antiGravUsers:
        for agu in antiGravUsers:
            # Check's if end_date is None, which means that it's still not finished
            if agu['end_date'] is None:
                return True
    return False

# TODO: Improve this function documentation
def get_user_status(username: str): 
    """
    Returns:
        id: user id -> int,
        status: UserStatusEnum (FROZEN/REGULAR/BLACKHOLED/DESERTER),
    """
    if not username:
        return None, None
    try:
        user = api.get(f'users/{username}/cursus_users')[0]
        begin_at = datetime.strptime(user['begin_at'][:10], '%Y-%m-%d')
        if user['user']['kind'] != 'student' or begin_at.date() > date.today():
            return None
        # Case of student that finished 42 cursus
        if not user['blackholed_at']:
            return user['user']['id'], UserStatusEnum.ACTIVE,

        blackholed_at = datetime.strptime(user['blackholed_at'][:10], '%Y-%m-%d')
        status = UserStatusEnum.ACTIVE
        if is_deserter(user):
            status = UserStatusEnum.DESERTER
        elif is_blackholed(str(blackholed_at)):
            status = UserStatusEnum.BLACKHOLED
        elif is_frozen(user['user']['id']):
            status = UserStatusEnum.AGU
        return user['user']['id'], status
    except Exception as e:
        print(e)
        return None, None