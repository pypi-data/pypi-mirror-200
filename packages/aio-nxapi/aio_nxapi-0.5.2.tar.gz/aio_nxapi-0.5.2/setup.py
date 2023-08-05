# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aionxapi', 'asyncnxapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'lxml>=4.9.1,<5.0.0']

setup_kwargs = {
    'name': 'aio-nxapi',
    'version': '0.5.2',
    'description': 'Cisco NX-API asyncio client',
    'long_description': '# Cisco NX-API asyncio Client\n\nThis repository contains a Cisco NX-API asyncio based client that uses\nthe [httpx](https://www.python-httpx.org/) as an underlying transport and\n[lxml](https://lxml.de/) as the basis for handling XML.\n\nNote: This client does not support the NETCONF interface.\n\n**WORK IN PROGESS**\n\n### Quick Example\n\nThie following shows how to create a Device instance and run a list of\ncommands.\n\nBy default the Device instance will use HTTPS transport.  The Device instance\nsupports the following settings:\n\n   * `host` - The device hostname or IP address\n   * `username` - The login user-name\n   * `password` - The login password\n   * `proto` - *(Optional)* Choose either "https" or "http", defaults to "https"\n   * `port` - *(Optional)* Chose the protocol port to override proto default\n\nThe result of command execution is a list of CommandResults (namedtuple).\nThe `output` field will be:\n   * lxml.Element when output format is \'xml\'\n   * dict when output format is \'json\'\n   * str when output format is \'text\'\n\n```python\nfrom asyncnxapi import Device\n\nusername = \'dummy-user\'\npassword = \'dummy-password\'\n\nasync def run_test(host):\n    dev = Device(host=host, creds=(username, password))\n    res = await dev.exec([\'show hostname\', \'show version\'], ofmt=\'json\')\n    for cmd in res:\n       if not cmd.ok:\n          print(f"{cmd.command} failed")\n          continue\n\n       # do something with cmd.output as dict since ofmt was \'json\'\n```\n\n# Limitations\n\n  * Chunking is not currently supported.  If anyone has need of this feature\n  please open an issue requesting support.\n\n# References\n\nCisco DevNet NX-API Rerefence:<br/>\n   * https://developer.cisco.com/site/cisco-nexus-nx-api-references/\n\nCisco platform specific NX-API references:\n\n   * N3K systems, requires 7.0(3)I2(2) or later:\n    https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus3000/sw/programmability/7_x/b_Cisco_Nexus_3000_Series_NX-OS_Programmability_Guide_7x/b_Cisco_Nexus_3000_Series_NX-OS_Programmability_Guide_7x_chapter_010010.html\n\n   * N5K system, requires 7.3(0)N1(1) or later:\n    https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus5000/sw/programmability/guide/b_Cisco_Nexus_5K6K_Series_NX-OS_Programmability_Guide/nx_api.html#topic_D110A801F14F43F385A90DE14293BA46\n\n   * N7K systems:\n    https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus7000/sw/programmability/guide/b_Cisco_Nexus_7000_Series_NX-OS_Programmability_Guide/b_Cisco_Nexus_7000_Series_NX-OS_Programmability_Guide_chapter_0101.html\n\n   * N9K systems:\n    https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/6-x/programmability/guide/b_Cisco_Nexus_9000_Series_NX-OS_Programmability_Guide/b_Cisco_Nexus_9000_Series_NX-OS_Programmability_Guide_chapter_011.html\n',
    'author': 'Jeremy Schulman',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
