"""
This is an example how to switch a crownstone using the crownstone python cloud lib.

Last update by Ricardo Steijn on 22-6-2020
"""
from crownstone_cloud.lib.cloud import CrownstoneCloud
import logging
import asyncio

# enable logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


async def main():
    # init cloud
    cloud = CrownstoneCloud('email', 'password')
    await cloud.async_initialize()

    # get a crownstone by name that can dim, and put it on 50% brightness
    crownstone_lamp = cloud.get_crownstone('Lamp')
    await crownstone_lamp.async_set_brightness(0.5)

    # get a crownstone by name and turn it on
    crownstone_tv = cloud.get_crownstone('TV')
    await crownstone_tv.async_turn_on()

    # close the session after we are done
    await cloud.async_close_session()

asyncio.run(main())
