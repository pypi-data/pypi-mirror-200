# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vmngclient',
 'vmngclient.api',
 'vmngclient.api.templates',
 'vmngclient.api.templates.device_template',
 'vmngclient.api.templates.models',
 'vmngclient.api.templates.payloads.aaa',
 'vmngclient.api.templates.payloads.cisco_system',
 'vmngclient.api.templates.payloads.cisco_vpn',
 'vmngclient.api.templates.payloads.cisco_vpn_interface_ethernet',
 'vmngclient.api.templates.payloads.tenant',
 'vmngclient.tests',
 'vmngclient.utils']

package_data = \
{'': ['*'],
 'vmngclient.api.templates.payloads.aaa': ['feature/*'],
 'vmngclient.api.templates.payloads.cisco_system': ['feature/*'],
 'vmngclient.api.templates.payloads.cisco_vpn': ['feature/*'],
 'vmngclient.api.templates.payloads.cisco_vpn_interface_ethernet': ['feature/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'attrs>=21.4.0,<22.0.0',
 'cattrs>=22.2.0,<23.0.0',
 'ciscoconfparse>=1.6.40,<2.0.0',
 'clint>=0.5.1,<0.6.0',
 'flake8-quotes>=3.3.1,<4.0.0',
 'parameterized>=0.8.1,<0.9.0',
 'pydantic>=1.10.4,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests-toolbelt>=0.10.1,<0.11.0',
 'requests>=2.27.1,<3.0.0',
 'tenacity>=8.1.0,<9.0.0']

setup_kwargs = {
    'name': 'vmngclient',
    'version': '0.8.1',
    'description': 'Universal vManage API',
    'long_description': '# vManage-client\n[![Python3.8](https://img.shields.io/static/v1?label=Python&logo=Python&color=3776AB&message=3.8)](https://www.python.org/)\n\nvManage client is a package for creating simple and parallel automatic requests via official vManageAPI. It is intended to serve as a multiple session handler (provider, provider as a tenant, tenant). The library is not dependent on environment which is being run in, you just need a connection to any vManage.\n\n## Installation\n```console\npip install vmngclient\n```\n\n## Session usage example\nOur session is an extension to `requests.Session` designed to make it easier to communicate via API calls with vManage. We provide ready to use authenticetion, you have to simply provide the vmanage url, username and password as as if you were doing it through a GUI. \n```python\nfrom vmngclient.session import create_vManageSession\n\nurl = "example.com"\nusername = "admin"\npassword = "password123"\nsession = create_vManageSession(url=url, username=username, password=password)\n\nsession.get("/dataservice/device")\n```\n\n## API usage examples\n\n<details>\n    <summary> <b>Get devices</b> <i>(click to expand)</i></summary>\n\n```python\ndevices = session.api.devices.get()\n```\n\n</details>\n\n<details>\n    <summary> <b>Admin Tech</b> <i>(click to expand)</i></summary>\n\n```Python\nadmin_tech_file = session.api.admin_tech.generate("172.16.255.11")\nadmintech.download(admin_tech_file)\nadmintech.delete(admin_tech_file)\n```\n</details>\n\n<details>\n    <summary> <b>Speed test</b> <i>(click to expand)</i></summary>\n\n```python\ndevices = session.api.devices.get()\nspeedtest = session.api.speedtest.speedtest(devices[0], devices[1])\n```\n\n</details>\n\n<details>\n    <summary> <b>Upgrade device</b> <i>(click to expand)</i></summary>\n\n```python\n# Prepare devices list\nvsmarts = [device for device in DevicesAPI(session).devices\n            if device .personality == Personality.VSMART]\nsoftware_image = "viptela-20.7.2-x86_64.tar.gz"\n\n# Upload image\nsession.api.repository.upload_image(software_image)\n\n# Upgrade\nsoftware_action = SoftwareActionAPI(session, DeviceCategory.VEDGES)\nsoftware_action_id = software_action.upgrade_software(vsmarts,\n    InstallSpecHelper.CEDGE.value, reboot = False, sync = True, software_image=software_image)\n\n# Check action status\nwait_for_completed(session, software_action_id, 3000)\n```\n\n</details>\n\n<details>\n    <summary> <b>Get alarms</b> <i>(click to expand)</i></summary>\n\n```python\nalarms = session.api.alarms.get()\n```\n\n</details>\n\n### Note:\nTo remove `InsecureRequestWarning`, you can include in your scripts:\n```Python\nimport urllib3\nurllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)\n```\n\n## [Contributing, bug reporting and feature requests](https://github.com/CiscoDevNet/vManage-client/blob/main/CONTRIBUTING.md)\n\n## Seeking support\n\nYou can contact us by submitting [issues](https://github.com/CiscoDevNet/vManage-client/issues), or directly via mail on vmngclient@cisco.com.\n',
    'author': 'kagorski',
    'author_email': 'kagorski@cisco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/CiscoDevNet/vManage-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
