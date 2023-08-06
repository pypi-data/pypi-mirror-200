# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['precilaser']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA>=1.12.0,<2.0.0', 'rich>=13.3.3,<14.0.0']

setup_kwargs = {
    'name': 'precilaser',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Precilaser\n Python interface for precilaser devices\n\nImplements a python interface using pyvisa for 3 Precilaser devices:\n* Precilaser Fiber DFB\n* Precilaser Amplifier\n* Precilaser SHG Amplifier\n\n## Implemented Functionality\n### Precilaser Fiber DFB\n* `status`  \n  retrieve the laser status, in a dataclass (with some of the boilerplate code removed; see `status.py` for more detail):\n  ```Python\n    @dataclass\n    class SeedStatus:\n      status_bytes: bytes\n      endian: str\n      temperature_set: float # grating temperature setpoint [C]\n      temperature_act: float # grating temperature [C]\n      temperature_diode: float # [C]\n      current_set: int # [mA]\n      current_act : int # [mA]\n      wavelength: float # [nm]\n      piezo_voltage: float # [V]\n      emission: bool\n      power: int\n      run_hours: int\n      run_minutes: int\n  ```\n* `temperature_setpoint`  \n  get or set the grating temperature in C\n* `piezo_voltage`  \n  get or set the piezo voltage, from 0 V to 5 V\n* `_get_serial_wavelength_params`  \n  retrieve the parameters required to reconstruct the wavelength from the grating temperature\n* `wavelength`  \n  calculate the wavelength from the retrieved parameters and the grating temperature\n\n### Precilaser Amplifier\n* `status`  \n  retrieve the amplifier status, in a dataclass (with some of the boilerplate code removed; see `status.py` for more detail):\n  ```Python\n  @dataclass\n  class AmplifierStatus:\n    status_bytes: bytes\n    endian: str\n    stable: bool\n    system_status: SystemStatus\n    driver_unlock: DriverUnlock\n    driver_current: Tuple[float, ...]\n    pd_value: Tuple[int, ...] # internal photodiode values in arb. units\n    pd_status: Tuple[PDStatus, ...]\n    temperatures: Tuple[float] # internal temperatures of amplifier stages etc.\n\n  @dataclass\n  class SystemStatus:\n    status: int\n    pd_protection: Tuple[bool, ...]\n    temperature_protection: Tuple[bool, ...]\n    fault: bool\n\n  @dataclass\n  class DriverUnlock:\n    driver_unlock: int\n    driver_enable_control: Tuple[bool, ...]\n    driver_enable_flag: Tuple[bool, ...]\n    interlock: bool # true if the interlock is ok\n\n  @dataclass\n  class PDStatus:\n    status: int\n    sampling_enable: bool\n    hardware_protection: bool\n    upper_limit_enabled: bool\n    lower_limit_enabled: bool\n    hardware_protection_event: bool\n    upper_limit_event: bool\n    lower_limit_event: bool\n    fault: bool\n  ```\n* `current`  \n  get or set the amplifier current [A]\n* `enable()`  \n  enable the amplifier\n* `disable()`  \n  disable the amplifier\n* `save()`\n  save amplifier settings to ROM\n* `enable_power_stabilization()`  \n  enable power stabilization mode; varies the amplifier current to keep the output power constant\n* `disable_power_stabilization()`\n  disable power stabilization mode\n\n### Precilaser Amplifier\nA subclass of the `Amplifier`, includes all `Amplifier` functionality plus additionally:\n* `shg_temperature`\n  get or set the shg crystal temperature [C]\n\n## Example\n```Python\n\nfrom precilaser import SHGAmplifier\n\namp = SHGAmplifier("COM50", address = 0)\n\n# change the SHG crystal temperature\namp.shg_temperature = 73.15',
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
