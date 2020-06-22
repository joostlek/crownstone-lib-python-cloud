"""
This is an example how to switch a crownstone using the crownstone python cloud lib.

Last update by Ricardo Steijn on 22-6-2020
"""
from crownstone_cloud.lib.cloud import CrownstoneCloud
import logging

# enable logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# init cloud
cloud = CrownstoneCloud('email', 'password')
cloud.initialize()

# get a crownstone by name and turn it on
crownstone_coffee_machine = cloud.get_crownstone('Coffee machine')
crownstone_coffee_machine.turn_on()

cloud.close_session()
