# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mr', 'mr.config', 'mr.states', 'mr.states.implementations']

package_data = \
{'': ['*']}

install_requires = \
['meeseeks-singleton>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'my-mimic',
    'version': '0.1.0',
    'description': 'Cache/Memoization package',
    'long_description': '# My Mimic\n```\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⢠⢊⢽⣝⡆⣫⣷⣌⣦⣤⡐⠾⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣾⣯⣿⣯⣷⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⡠⢤⣜⠺⢟⡩⡇⢹⣉⡟⣰⠻⣯⢇⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠷⠄⠀⠀⠀⠀⠀⠀⠀\n⢸⢰⣻⡟⣄⢈⣖⠹⢺⠰⠷⣏⢱⣾⣿⣿⣿⣿⣾⣿⣷⣶⣶⣤⣤⠠⠐⠂⠀⠀⠐⠒⠠⣄⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠁⠋⠳⣄⠫⡐⣉⠆⡓⢌⢂⢿⢹⣿⡛⢿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⢀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠻⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠈⡔⣡⠒⣸⠞⡌⢂⢎⣥⣷⣿⢨⣿⣿⣿⣿⡟⠁⡀⠀⠠⠀⡐⠀⠡⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠸⣦⣳⡆⣞⣴⡿⠃⠀⠘⠛⠛⣿⣿⣿⡿⢀⡞⢣⡇⠀⡀⠰⡴⠟⡄⠆⢃⠘⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢠⢛⢻⠏⠉⠀⠀⠀⠀⠀⠀⠙⠛⡫⢁⠸⡀⠸⠅⢀⠡⢸⡇⠘⡿⠀⠈⠘⡌⠛⠿⢿⡟⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⡜⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣟⡆⢠⠈⠁⢀⠂⠀⡀⠉⢒⠇⠠⢀⣭⣔⡩⢐⠂⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢇⢀⡦⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⣯⡇⢀⡘⢷⣶⢶⠶⣶⣚⡟⡄⣴⠻⣭⣟⣷⡈⢒⣃⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⢸⡈⠐⠣⠄⣀⡀⠀⣠⡾⣩⢏⡼⣹⢏⣧⡂⠌⡌⠻⣉⠎⡑⢎⢧⡐⢯⣷⢳⡾⡝⣠⠿⣏⡟⣿⣟⣦⡄⠀⠀⣀⣀⡀⠤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠙⠦⠄⣐⡀⢀⠠⠉⠉⠘⡷⣎⢷⡹⣎⢷⡻⣖⢨⣑⣨⠘⢩⠘⠌⣃⠢⢉⣋⣵⠾⣍⢳⣬⣛⢶⣻⡮⡑⠆⠀⢀⣀⣠⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢱⣧⣥⣾⢿⡜⣯⢳⣝⢮⣳⡇⠁⠒⠤⢋⢏⢩⡙⢭⢉⠧⡈⣿⡝⣮⢳⢮⡝⣮⢷⣻⢾⡏⠉⠀⠀⠘⡦⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡽⣯⠿⣽⣞⡷⣞⡷⣯⠛⠀⠀⣠⣤⠾⡶⣞⣤⣅⠂⠀⢻⣽⣎⣟⣮⡽⣯⢿⣹⡿⠀⠀⠀⠀⠀⠸⢄⣈⡇⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣽⣻⠷⣾⡽⣯⠟⠃⠀⢠⣾⢻⣬⢛⡵⢫⡞⣭⢻⡄⠀⠙⠾⣽⢾⣽⣳⡯⠛⠀⠀⠀⠀⠀⡠⠊⠉⠀⠈⠑⠢⡀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⣩⠁⠀⠀⠀⠀⣼⣇⡳⣌⠳⣜⢣⡞⣵⣫⢽⠀⠀⢀⠤⡉⠽⠀⠀⠀⠀⡠⠖⠂⠒⠁⠀⡀⠀⡀⠀⠀⣠⠭⡁⠉⡀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡅⡄⠀⠀⠀⢿⡲⣝⡬⣓⢮⡳⣝⢮⣳⢻⠀⡌⢃⢚⢰⠃⠀⠀⠀⠀⢧⢀⡰⠊⠙⣼⠁⡬⡄⢰⠦⢄⡁⠘⢫⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⣻⢟⣿⣴⠠⢌⠻⣧⣻⣝⣮⣳⣏⡷⡽⣣⡵⣞⠿⣯⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⡠⠃⠀⡇⢸⠀⠑⢤⠐⠴⠞⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣱⣟⣾⣳⣟⣷⡨⠒⣌⠱⡛⢚⠓⣛⢙⣰⣿⡹⣞⡽⣎⢷⣻⡄⠀⠀⠀⠀⠀⠀⠐⢧⣀⣠⠇⠘⠶⠀⠞⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠽⢷⣻⣞⣧⣟⡾⣽⠧⠣⢄⠣⡘⠤⡉⢤⠃⣼⣷⣻⢾⣵⣻⠞⠉⠓⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡄⠊⠁⠀⢀⣿⣞⣷⣫⣽⡞⠐⢣⣬⣆⣁⣢⣑⣢⣵⡞⣷⣯⣟⣾⣽⠂⣤⣀⠀⠀⢉⡔⠒⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠞⠉⠀⢠⣴⠞⠋⠉⠙⠛⠛⠉⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠀⠈⠘⠛⠉⠁⠀⠀⠉⠛⠶⡏⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⣎⠈⠐⠒⡖⣾⡉⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⣫⢭⠶⣋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠶⠹⢜⡱⡸⢌⡳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣈⢦⠓⡼⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣄⡀⠈⠑⣇⡝⣌⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣣⡛⡔⡻⣄⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠛⢻⣷⣤⣾⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣷⣌⣱⣿⣷⣄⡀⣠⣾⣿⢿⣧⡀⠀\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣻⣷⡀\n⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⢿⣿⣿⣿⣟⣿⣻⣽⣳⣯⣿⠇\n⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠻⠷⠿⠷⠟⠋⠀\n                                                                            By CenturyBoys\n```\n\n\nMy Mimic is a function decorator for cache/memoization. They use the args and kwargs to create a hash to storage the function call result after the first call all function invoke will use already storage result.  \n\n### Configuration\n\nUsing `mr.Mime` from Mimic allowed you to use the default config or create a self one. By default, an in-memory state are used you can implement your own state resolver using the interface IState.\n\nBelow you can see the interface contract\n```python\nfrom abc import ABC, abstractmethod\n\nclass IState(ABC):\n    """\n    State interface\n    """\n\n    @abstractmethod\n    def sync_get(self, key: str):\n        """\n        Sync get implementation\n        :param key: Str\n        :return:\n        """\n\n    @abstractmethod\n    def sync_set(self, key: str, value: any, ttl: int = None):\n        """\n        Sync set implementation\n        :param key: Str\n        :param value: Any\n        :param ttl: int. Seconds that the cache will have to live. Set None to never die\n        :return:\n        """\n\n    @abstractmethod\n    async def async_get(self, key: str):\n        """\n        Async get implementation\n        :param key: Str\n        :return:\n        """\n\n    @abstractmethod\n    async def async_set(self, key: str, value: any, ttl: int = None):\n        """\n        Async set implementation\n        :param key: Str\n        :param value: Any\n        :param ttl: int. Seconds that the cache will have to live. Set None to never die\n        :return:\n        """\n\n```\n\nTo configure a new state you need to use `mr.Mime.set_config` function passing a config instance.\n\n```python\nimport mr\n\nclass MyState(mr.IState):\n    def sync_get(self, key: str):\n        pass\n\n    def sync_set(self, key: str, value: any, ttl: int = None):\n        pass\n\n    async def async_get(self, key: str):\n        pass\n\n    async def async_set(self, key: str, value: any, ttl: int = None):\n        pass\n\nmr.Mime.set_config(config=mr.Config(state=MyState))\n```\n\n### How to use\n\nFor that we use `mr.Mime` as decorator that receive a ttl as argument. That means the ttl is the seconds that the cache will have to live. Set None to never die.\n\nMime works fine with sync and async functions too.\n\n```python\nimport time\nimport mr\n\n@mr.Mime(ttl=1)\ndef cached_callback(param_a: int, param_b: int):\n    print("Function was called")\n    return param_a + param_b\n\nresult = cached_callback(1, 2)\nprint(result)\nresult = cached_callback(1, 2)\nprint(result)\ntime.sleep(2)\nprint("Await 2 seconds")\nresult = cached_callback(1, 2)\nprint(result)\n```\nThe output will be\n\n```bash\nFunction was called\n3\n3\nAwait 2 seconds\nFunction was called\n3\n```',
    'author': 'Marco Sievers de Almeida Ximit Gaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
