# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_fixparser',
 'jetblack_fixparser.fix_message',
 'jetblack_fixparser.loader',
 'jetblack_fixparser.meta_data']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.17,<0.18']

setup_kwargs = {
    'name': 'jetblack-fixparser',
    'version': '2.4.0',
    'description': 'A parser for FIX messages',
    'long_description': '# jetblack-fixparser\n\nA parser for FIX messages.\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\npip install jetblack-fixparser\n```\n\n## Protocol Files\n\nWhile FIX is a standard, the structure of the fields and messages is configurable.\nThis configuration is typically loaded from a file. The source repository\ncontains a number of such files in the `/etc` folder in `YAML` format. There is\nalso a *QuickFix* loader.\n\nThe YAML format makes use of defaults. All message fields default to type `field`,\nso only `group` and `component` fields need to be explicitly specified. Also all\nmessage fields are consider optional, non-optional fields must be marked as\n`required: true`.\n\n## Usage\n\n### Decoding\n\nTo decode a FIX bytes buffer -\n\n```python\nfrom jetblack_fixparser import load_yaml_protocol, FixMessage\n\nbuffer = b\'8=FIX.4.4|9=94|35=3|49=A|56=AB|128=B1|34=214|50=U1|52=20100304-09:42:23.130|45=176|371=15|372=X|373=1|58=txt|10=058|\',\n\nprotocol = load_yaml_protocol(\n    \'FIX44.yaml\',\n    is_millisecond_time=True,\n    is_float_decimal=True\n)\n\nfix_message = FixMessage.decode(\n    protocol,\n    buffer,\n    sep=b\'|\',\n    strict=True,\n    validate=True,\n    convert_sep_for_checksum=True\n)\n\nprint(fix_message.message)\n```\n\nNote that strict validation is enabled. This ensures all required fields are\nspecified. Also the separator is changed from `NULL` to `|` to so they can be\ndisplayed. However the checksum was calculated with the original field separator\nso the `convert_sep_for_checksum` is set to `true`.\n\n### Encoding\n\nTo encode a dictionary describing a FIX message - \n\n```python\nfrom datetime import datetime, timezone\nfrom jetblack_fixparser import load_yaml_protocol, FixMessage\n\nprotocol = load_yaml_protocol(\n    \'FIX44.yaml\',\n    is_millisecond_time=True,\n    is_float_decimal=True,\n    is_type_enum=None\n)\nsending_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=timezone.utc)\n\nfix_message = FixMessage(\n    protocol,\n    {\n        \'MsgType\': \'LOGON\',\n        \'MsgSeqNum\': 42,\n        \'SenderCompID\': "SENDER",\n        \'TargetCompID\': "TARGET",\n        \'SendingTime\': sending_time,\n        \'EncryptMethod\': "NONE",\n        \'HeartBtInt\': 30\n    }\n)\nbuffer = fix_message.encode(regenerate_integrity=True)\n\nprint(buffer)\n```\n\nNote that the `BeginString`, `BodyLength` and `Checksum` fields were automatically\ngenerated.\n\n### Factories\n\nTo encode and decode a message using a factory - \n\n```python\nfrom datetime import datetime, timezone\nfrom jetblack_fixparser import load_yaml_protocol, FixMessage, FixMessageFactory\n\nprotocol = load_yaml_protocol(\n    \'FIX44.yaml\',\n    is_millisecond_time=True,\n    is_float_decimal=True,\n    is_type_enum=None\n)\n\nfactory = FixMessageFactory(protocol, "SENDER", "TARGET")\n\nsending_time = datetime(2020, 1, 1, 12, 30, 0, tzinfo=timezone.utc)\nfix_messages = factory.create(\n        \'LOGON\',\n        42,\n        sending_time,\n        {\n            \'EncryptMethod\': "NONE",\n            \'HeartBtInt\': 30\n        }\n    )\n\nbuffer = fix_message.encode(regenerate_integrity=True)\nroundtrip = FixMessage.decode(protocol, buffer)\nassert fix_message.message == roundtrip.message\n```\n\nBecause the sender and target remain the same, we can simplify message generation\nwith the factory.\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-fixparser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
