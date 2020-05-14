# crownstone-lib-python-cloud

Asynchronous Python library to get data from the cloud, and switch Crownstones.

## Functionality

* Async: using asyncio and aiohttp, optimized for speed.
* Easy to use: sync all your Crownstone Cloud data with just one command!
* Structurally sound: find your data with ease!
* Complete: set the switch state and brightness of your Crownstones remotely!

## Requirements

* Python 3.7 or higher
* Aiohttp 3.6.2

## Standard installation

cd to the project folder and run:
```console
$ python3.7 setup.py install
```

## Install in a virtual environment

To install the library excute the following command:
```console
$ python3.7 -m venv venv3.7
```
Activate your venv using:
```console
$ source venv3.7/bin/activate
```
Once activated, the venv is used to executed python files, and libraries will be installed in the venv.<br>
To install this library, cd to the project folder and run:
```console
$ python setup.py install
```

## Getting started

### Example

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

## Data structure

The cloud can be displayed with the following structure:
* User
    * Keys
    * Spheres
        * Locations
        * Crownstones
        * Users
        

### User

The user is the to whom the data belongs.<br> 
The user is the one that logs in using email and password.<br>
By getting a user specific access token after login, the data for that specific user can be requested.
```python
await cloud.login('email', 'password')
```

### Keys

The keys are user specific.<br> 
They are required to connect to the crownstone bluetooth mesh.<br>
The most common used keys are the sphere keys. They are located within each individual sphere.<br>
Getting the keys is optional and not included in the general sync.<br>
The keys are returned as a dictionary.
To get the keys for a sphere:
```python
sphere = cloud.spheres.find('MySphere')
keys = await sphere.get_keys()
```

### Spheres

Spheres can be seen as a house, apartement or office. They have rooms (locations), Crownstones and users in them.<br>
Note that the spheres need to be synced **FIRST** before the other data can be synced.<br>
To get spheres for the user without any data (only name and id) use:
```python
await cloud.spheres.sync()
```
To get the spheres and all their data at once use:
```python
await cloud.sync()
```

### Locations

Locations are the rooms in your house or other building.<br>
For example for a house: 
* Livingroom
* Bedroom
* Garage
* Bathroom

To get the locations for your sphere use:
```python
sphere = cloud.spheres.find('MySphere')
await sphere.locations.sync()
```
For the presence tracking, an advanded algorithm detects whenever a user is on a specific location.<br>
The presence is saved for each location in a list. The list contains names of the people who are present.<br>
To print the present people list:
```python
location = sphere.locations.find('MyLocation')
print(location.present_people)
```

### Crownstones

Crownstones are smart plugs that can make every device that isn't smart, way smarter!<br>
Crownstones are located within a sphere.<br>
Example Crownstones:
* Lamp
* Charger
* Television

to get the crownstones for your sphere:
```python
sphere = cloud.spheres.find('MySphere')
await sphere.crownstones.sync()
```
Crownstones can also be turned on/off remotely.<br>
Since this is a command sent to your phone, it is required to have Bluetooth on and to be present in your sphere.<br>
To switch a crownstone on/off:
```python
crownstone = cloud.get_crownstone('MyCrownstone')
await crownstone.turn_on()
await crownstone.turn_off()
```
It is also possible to set the brightness(dimming) of a crownstone.<br>
For this to work, you need to enable dimming in your crownstone app for that specific crownstone. Dimming only works with lights and it is **not** recommended to use it for any other device.<br>
For the brightness use a percentage between 0% and 100%. To set the brightness:
```python
crownstone = cloud.get_crownstone('MyCrownstone')
await crownstone.set_brightness(50)
```

### Users

Users are people who have access to a sphere.<br>
A user can have 3 roles:
* Admin
* Member
* Guest
Each role has different privileges.<br>
Users can have similar names. To view the info of a user's first name in a sphere:
```python
sphere = cloud.spheres.find('MySphere')
users = sphere.users.find_by_first_name('MyUser')
for username in users:
    print(user.role)
    print(user.last_name)
    print(user.email)
```

## Testing
Tests coming soon!
