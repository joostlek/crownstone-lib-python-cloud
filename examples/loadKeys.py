"""
This is an example to get the keys for a sphere, and load them into BLE module.

Created by Ricardo Steijn on 1-5-2020
"""
from cloudLib.lib.cloud import CrownstoneCloud
from BluenetLib.BLE import BluenetBle

cloud = CrownstoneCloud()
bleCore = BluenetBle(hciIndex=0)


############# this function will be executed #############
async def run():
    # login to the cloud using your account (replace with your own credentials)
    await cloud.login('email', 'password')
    # load all the user data from the cloud
    await cloud.sync()

    # get the keys
    await cloud.spheres.get_keys()
    # select a sphere
    bedroom = cloud.spheres.find('Bedroom')
    # load the keys from the sphere into BLE core
    bleCore.setSettings(
        bedroom.keys.admin_key,
        bedroom.keys.member_key,
        bedroom.keys.basic_key,
        bedroom.keys.service_data_key,
        bedroom.keys.localization_key,
        bedroom.keys.mesh_application_key,
        bedroom.keys.mesh_network_key
    )

    # start scanning for crownstones in range
    crownstones_in_range = bleCore.getCrownstonesByScanning()
    for crownstone in crownstones_in_range:
        print(crownstone)

    # close the cloud session and BLE session
    bleCore.shutDown()
    await cloud.cleanup()
##########################################################

# start executing the function
cloud.start(run())