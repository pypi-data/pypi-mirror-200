# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cohpy', 'cohpy.tests']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=7.2.2,<8.0.0', 'flake8>=6.0.0,<7.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'cohpy',
    'version': '1.0',
    'description': '',
    'long_description': '<h1 style="text-align: center">COHPY</h1>\n<div style="text-align: center">\n<i>An unofficial API Wrapper for Company Of Heroes API</i>\n\n</div>\n\n[![Lint and Tests](https://github.com/AndresGL01/cohpy/actions/workflows/ci.yml/badge.svg)](https://github.com/AndresGL01/cohpy/actions/workflows/ci.yml)\n<a href="https://github.com/AndresGL01/cohpy/stargazers"><img src="https://img.shields.io/github/stars/AndresGL01/cohpy" alt="Stars Badge"/></a>\n\n\n### Tutorial\n- [How to install](#How-to-install)\n- [Functionalities](#Functionalities)\n- [Examples](#Examples)\n\n## Current API Coverage\n- List all leaderboards ✔️\n- Show players from a leaderboard ️✔️\n- Show match historial from a player ✔️\n- Show personal player stats ✔️\n\n## Functionalities\n\napi_client:\n: Interface between wrapper and Company of Heroes API \n\n````python\nimport cohpy\n\napi_client = cohpy.get_api_client()\n````\n\napi_client.leaderboards():\n: Get all leaderboards available from the COH API\n\n- Parameters:\n  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).\nYou can show it setting this param to **False**\n\n````python\nimport cohpy\n\napi_client = cohpy.get_api_client()\n\napi_client.leaderboards()\n````\n\napi_client.leaderboards():\n: Get all leaderboards available from the COH API\n\n- Parameters:\n  - leaderboard_id (mandatory): Leaderboard identifier extracted from leaderboards() function. You can use raw ints like 2130329 or\nCode class that wraps more used leaderboards\n  - count (optional): **Default=200** How many players will be showed in the response. From 1 to 200.\n  - sort_type (optional): **Default=ELO** Set the order of the leaderboard based on wins or elo. You can use ints like 0 (ELO) or 1 (WINS). Also you can use SortType wrapper\n  - start (optional): **Default=1** Sets the position of the first player obtained from the request.\n  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).\nYou can show it setting this param to **False**\n````python\nimport cohpy\n\napi_client = cohpy.get_api_client()\n\napi_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3, sort_type=cohpy.SortType.ELO)\n````\n\napi_client.match_history():\n: Get all leaderboards available from the COH API\n\n- Parameters:\n  - profile_params (mandatory): Player id. Can be steam profile id or relic id (Don\'t forget to set the mode). Can be a list of ints or strings. Steam queries must follow /steam/[0-9]+\n  - mode (optional): **Default=relic** Set the query mode. Options are [relic, steam].\n  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).\nYou can show it setting this param to **False**\n````python\nimport cohpy\n\napi_client = cohpy.get_api_client()\n\napi_client.match_history(profile_params=[1, 2])\napi_client.match_history(profile_params=1)\napi_client.match_history(profile_params=\'/steam/123456789\', mode=\'steam\')\napi_client.match_history(profile_params=[\'/steam/123456789\', \'/steam/123456789\'], mode=\'steam\')\n\n````\n\napi_client.personal_stats():\n: Get all leaderboards available from the COH API\n\n- Parameters:\n  - profile_params (mandatory): Player id. Can be steam profile id, relic id or alias (Don\'t forget to set the mode). Can be a list of ints or strings. Steam queries must follow /steam/[0-9]+\n  - mode (optional): **Default=relic** Set the query mode. Options are [relic, steam].\n  - remove_server_status (optional): **Default=True** Remove from the response the server status (redundant).\nYou can show it setting this param to **False**\n````python\nimport cohpy\n\napi_client = cohpy.get_api_client()\n\napi_client.personal_stats(profile_params=[1, 2])\napi_client.personal_stats(profile_params=1)\napi_client.personal_stats(profile_params=\'/steam/123456789\', mode=\'steam\')\napi_client.personal_stats(profile_params=[\'/steam/123456789\', \'/steam/123456789\'], mode=\'steam\')\napi_client.personal_stats(profile_params=\'yoursuperalias\', mode=\'alias\')\napi_client.personal_stats(profile_params=[\'yoursuperalias\', \'awesomealias\'], mode=\'alias\')\n\n````\n\n# Examples\nFirst of all, you\'ll need an APIClient instance to retrieve the api data: \n````python\nimport cohpy\n\napi_client = cohpy.get_api_client()\n````\nThen you could use the API interface to retrieve the data you want:\n\n````python\nimport cohpy\n\nall_leaderboards = api_client.leaderboards() # Returns all leaderboards info\namerican_3v3_leaderboard = api_client.leaderboard(leaderboard_id=cohpy.Codes.USF3v3) # Returns info from specific leaderboard\n````\nNote that ````leaderboard_id```` can be a int or a cohpy.Codes instance.\n',
    'author': 'Andres Garrido',
    'author_email': 'andreslp0001@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
