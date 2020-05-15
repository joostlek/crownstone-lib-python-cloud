"""
API to update the data in the cloud models.
The main purpose is to use these callbacks in combination with crownstone-lib-python-sse.
It can however be manually used if so pleased.
"""


def update_switch_state(switch_state_event, **kwargs):
    """Update the switch state of a crownstone"""
    pass


def update_presence(presence_event, **kwargs):
    """Update the presence on a location"""
    pass


def update_sphere_data(data_event, **kwargs):
    """Update/add/remove sphere data"""
    pass


def update_crownstone_data(data_event, **kwargs):
    """Update/add/remove crownstone data"""
    pass


def update_user_data(data_event, **kwargs):
    """Update/add/remove user data"""
    pass


def update_location_data(data_event, **kwargs):
    """Update/add/remove location data"""
    pass