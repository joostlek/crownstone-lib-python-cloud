"""
This is an example how to switch a crownstone using the crownstone python lib cloud.
Using this library in async context is the recommended way.

Last update by Ricardo Steijn on 31-10-2020
"""
from crownstone_cloud import CrownstoneCloud, create_clientsession
import logging
import asyncio

# Enable logging.
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


async def main():
    # Every instance creates it's own websession for easy accessibility, however using 1 websession is recommended.
    # Create your websession like so:
    websession = create_clientsession()
    # Initialize cloud.
    cloud_user_1 = CrownstoneCloud('email_user_1', 'password_user_1', websession)
    # Login to the Crownstone Cloud and synchronize all cloud data.
    await cloud_user_1.async_initialize()

    # Get a crownstone by name that can dim, and put it on 20% brightness for user 1
    crownstone_lamp = cloud_user_1.get_crownstone('Lamp')
    await crownstone_lamp.async_set_brightness(20)

    # Login & synchronize data for an other account.
    cloud_user_2 = CrownstoneCloud('email_user_2', 'password_user_2', websession)
    await cloud_user_2.async_initialize()

    # Get a crownstone by name and turn it on for user 2.
    crownstone_tv = cloud_user_2.get_crownstone('TV')
    await crownstone_tv.async_turn_on()

    # If you want to update specific data you can get the cloud data object for your user.
    # This object has all the cloud data for your user saved in it, which was synced with async_initialize()
    # Parts of the data can also be synced individually without touching the other data.
    # To sync all data at once, use async_synchronize() instead.
    my_sphere = cloud_user_1.cloud_data.find("my_sphere_name")
    # request to sync only the locations with the cloud
    my_sphere.locations.async_update_location_data()
    # get the keys for this sphere so you can use them with the Crownstone BLE python library
    sphere_keys = my_sphere.async_get_keys()

    # Close the aiohttp clientsession after we are done.
    await websession.close()

asyncio.run(main())
