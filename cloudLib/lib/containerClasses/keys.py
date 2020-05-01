from typing import Optional


class Keys:
    """Container class for the keys of a user, for a sphere"""

    def __init__(self, key_set: dict) -> None:
        """Init"""
        self.key_set = key_set

        self.admin_key: Optional[str] = None
        self.member_key: Optional[str] = None
        self.basic_key: Optional[str] = None
        self.localization_key: Optional[str] = None
        self.service_data_key: Optional[str] = None
        self.mesh_application_key: Optional[str] = None
        self.mesh_network_key: Optional[str] = None

        self.load_keys()

    def load_keys(self) -> None:
        """Load keys from dict into string"""

        for key_data in self.key_set["sphereKeys"]:
            if key_data["ttl"] == 0:
                if key_data['keyType'] == 'ADMIN_KEY':
                    self.admin_key = key_data['key']
                elif key_data['keyType'] == 'MEMBER_KEY':
                    self.member_key = key_data['key']
                elif key_data['keyType'] == 'BASIC_KEY':
                    self.basic_key = key_data['key']
                elif key_data['keyType'] == 'LOCALIZATION_KEY':
                    self.localization_key = key_data['key']
                elif key_data['keyType'] == 'SERVICE_DATA_KEY':
                    self.service_data_key = key_data['key']
                elif key_data['keyType'] == 'MESH_APPLICATION_KEY':
                    self.mesh_application_key = key_data['key']
                elif key_data['keyType'] == 'MESH_NETWORK_KEY':
                    self.mesh_network_key = key_data['key']
