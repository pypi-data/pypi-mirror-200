# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_recorder']

package_data = \
{'': ['*']}

install_requires = \
['time-machine>=2.9.0,<3.0.0', 'vcrpy>=4.2.1,<5.0.0']

entry_points = \
{'pytest11': ['pytest_recorder_plugin = pytest_recorder.plugin',
              'pytest_recorder_record_http = pytest_recorder.record_http',
              'pytest_recorder_record_time = pytest_recorder.record_time',
              'pytest_recorder_record_verify_object = '
              'pytest_recorder.record_verify_object',
              'pytest_recorder_record_verify_screen = '
              'pytest_recorder.record_verify_screen']}

setup_kwargs = {
    'name': 'pytest-recorder',
    'version': '0.2.3',
    'description': 'Pytest plugin, meant to facilitate unit tests writing for tools consumming Web APIs.',
    'long_description': '# 1. TL;DR example\nSTEP 1\n\nWrite this code:\n\n\n# File tests/some_module.py\n\n```python\n@pytest.mark.record_http\n@pytest.mark.record_time\n@pytest.mark.record_verify_screen\ndef test_some_test(record):\n    some_python_object = ...\n\n    record.add_verify(object=some_python_object)\n```\n\nSTEP 2\n\nRun:\n\npytest tests/some_module.py --record\n\nIt will:\n\nSave all the  HTTP requests\n\nSave the execution datetime\n\nSave the screen output\n\nSave the data you provide to recorder object\n\nSTEP 3\n\nRun:\n\npytest tests/some_module.py\n\nIt will:\n\nReuse the stored HTTP requests\n\nReuse the same datetime to execute the test\n\nCompare the current screen output to the previous one and raise and exception if different\n\nCompare the current recorder object data to the previous one and raise and exception if different\n\n# 2. Detailed example\nCODE\n\n```python\n@pytest.mark.record_http\n@pytest.mark.record_time(date=datetime(2023, 3, 1, 12, 0, 0), tic=False)\n@pytest.mark.record_verify_screen(hash=True)\ndef test_some_test(record):\n    ...\n    record.hash_only = True\n    record.add_verify(object=df)\n    record.add_verify(object=[df])\n\n    recorder.add_verify(\n        object=df,\n    )\n```\n\nUSAGE\n\npytest [FILE] [--record[=none,all,http,object,screen,time]] [--record-no-overwrite] [--record-no-hash]\n\nFILES\n\nFor a given test_function from test_module, we will have the following files:\n\n/tests/test_module.py:test_function\n\n/tests/record/http/test_module/test_function.yaml\n\n/tests/record/object/test_module/test_function.json\n\n/tests/record/object_hash/test_module/test_function.txt/json?\n\n/tests/record/screen/test_module/test_function.txt/json?\n\n/tests/record/screen_hash/test_module/test_function.txt/json?\n\n/tests/record/time/test_module/test_function.txt/json?\n\n',
    'author': 'Chavithra PARANA',
    'author_email': 'chavithra@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
