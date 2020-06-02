"""
This is an example how to switch a crownstone using the crownstone python cloud lib.

Last update by Ricardo Steijn on 2-6-2020
"""
from crownstone_cloud.lib.cloud import CrownstoneCloud
import asyncio


async def main():
    # init cloud
    cloud = CrownstoneCloud('email', 'password')
    await cloud.initialize()

    # get a crownstone by name and switch it on
    crownstone = cloud.get_crownstone('awesomeCrownstone')
    await crownstone.turn_on()

    # switch all crownstones in a sphere to on:
    sphere = cloud.spheres.find('awesomeSphere')
    for crownstone in sphere.crownstones:
        await crownstone.turn_on()

    await cloud.close_session()

asyncio.run(main())