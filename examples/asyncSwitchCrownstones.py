"""
This is an example how to switch a crownstone using the crownstone python lib cloud.
Using this library in async context is the recommended way.

Last update by Ricardo Steijn on 17-10-2020
"""
from crownstone_cloud import CrownstoneCloud
import logging
import asyncio

# Enable logging.
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


async def main():
    # Initialize cloud.
    cloud = CrownstoneCloud()
    # Login to the Crownstone Cloud and synchronize all cloud data.
    # Important is to save your user id which is returned from the function!
    user_id_1 = await cloud.async_initialize('email_user_1', 'password_user_1')

    # Get a crownstone by name that can dim, and put it on 20% brightness for user 1.
    crownstone_lamp = cloud.get_crownstone('Lamp', user_id_1)
    await crownstone_lamp.async_set_brightness(20)

    # Login & synchronize data for an other account.
    user_id_2 = await cloud.async_initialize("email_user_2", "password_user_2")

    # Get a crownstone by name and turn it on for user 2.
    crownstone_tv = cloud.get_crownstone('TV', user_id_2)
    await crownstone_tv.async_turn_on()

    # If you want to update specific data you can get the cloud data object for your user.
    # This object has all the cloud data for your user saved in it, which was synced with async_initialize()
    # Parts of the data can also be synced individually without touching the other data.
    # To sync all data at once, use async_synchronize() instead.
    my_cloud_data = cloud.get_cloud_data(user_id_1)
    # Now find the specific sphere object
    my_sphere = my_cloud_data.find("my_sphere_name")
    # request to sync only the locations with the cloud
    my_sphere.locations.async_update_location_data()
    # get the keys for this sphere so you can use them with the Crownstone BLE python library
    sphere_keys = my_sphere.async_get_keys()

    # Close the aiohttp clientsession after we are done.
    await cloud.async_close_session()

asyncio.run(main())
