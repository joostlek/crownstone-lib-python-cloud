"""
This is an example how to switch a crownstone using the crownstone python lib cloud.

Last update by Ricardo Steijn on 17-10-2020
"""
from crownstone_cloud import CrownstoneCloud, run_async
import logging

# Enable logging.
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Initialize cloud.
cloud = CrownstoneCloud()
# Use 'run_async' to run async functions in sync context.
# Login & synchronize all cloud data. Save the user id that the function returns for later use.
my_user_id = run_async(cloud.async_initialize('email', 'password'))

# Get a crownstone by name and turn it on.
crownstone_coffee_machine = cloud.get_crownstone('Coffee machine', my_user_id)
run_async(crownstone_coffee_machine.async_turn_on())

# Close the session after we are done.
run_async(cloud.async_close_session())
