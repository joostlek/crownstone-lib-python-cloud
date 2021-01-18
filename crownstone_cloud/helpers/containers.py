"""Contains classes that only hold data."""


class EnergyData:
    """Data class that holds energy measurements"""

    def __init__(self, accumulated_energy: int, utc_timestamp: int) -> None:
        """Initialize the object."""
        # new value obtained from Crownstone USB Dongle (or other source)
        self.energy_usage = accumulated_energy

        # the new energy usage value (after adding the offset or previous value)
        self.corrected_energy_usage = 0

        # timestamp of the measurement in UTC
        self.timestamp = utc_timestamp
