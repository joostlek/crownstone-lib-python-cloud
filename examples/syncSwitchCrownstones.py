"""
This is an example how to switch a crownstone using the crownstone python cloud lib.

Last update by Ricardo Steijn on 15-5-2020
"""
from crownstone_cloud.lib.cloud import CrownstoneCloud

# init cloud
cloud = CrownstoneCloud('email', 'password')
cloud.initialize_sync()

# get a crownstone and turn it on
crownstone = cloud.get_crownstone('awesomeCrownstone')
crownstone.turn_on_sync()