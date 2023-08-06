# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ligo', 'ligo.rrt_chat', 'ligo.rrt_chat.tests']

package_data = \
{'': ['*'], 'ligo.rrt_chat': ['data/*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'safe-netrc>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'ligo-rrt-chat',
    'version': '0.1.0.dev3',
    'description': '',
    'long_description': '# Chat\n\nCreate a mattermost chat for discussing superevents.\n\n## Usage\n\nThis current version uses a simple superevent_dictionary \ncontaining superevent_id to make mattermost channels.\nIt only works if the .netrc file has a "mattermost-bot" \nlogin with appropiate token as password. \n\nA `response` object gets the response form the mattermost api\nIf there is no response, the channel creation succeeded \nThe new channel name will be `RRT {superevent_id}`\nA post will be made in this channel with a corresponding \ngrace_db playground url.\n\n```\nfrom ligo.rrt_chat import channel_creation\nimport json\n\nres = channel_creation.rrt_channel_creation(superevent_dict)\n\nif res is not None:\n    print("channel creation failed {}".format(json.loads(res.text)))    \nelse:\n    print("channel creation succeded")\n```\n',
    'author': 'Sushant Sharma-Chaudhary',
    'author_email': 'sushant.sharma-chaudhary@git.ligo.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
