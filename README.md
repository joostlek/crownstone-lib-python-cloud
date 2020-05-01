# crownstone-lib-python-cloud
Asynchronous Python library to get data from the cloud, and switch Crownstones.

## Example

```Python
from cloudLib.lib.cloud import CrownstoneCloud

cloud = CrownstoneCloud()


############# this function will be executed #############
async def run():
    # login to the cloud using your account (replace with your own credentials)
    await cloud.login('email', 'password')
    # load all the user data from the cloud
    await cloud.sync()

    # get a crownstone by name
    lamp = cloud.get_crownstone('Lamp')
    # turn the crownstone on
    await lamp.turn_on()

    # close the session
    await cloud.cleanup()
##########################################################

# start executing the function
cloud.start(run())
```
