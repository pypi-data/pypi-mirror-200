# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyassorted', 'pyassorted.asyncio', 'pyassorted.cache', 'pyassorted.lock']

package_data = \
{'': ['*']}

install_requires = \
['pytz', 'rich']

setup_kwargs = {
    'name': 'pyassorted',
    'version': '0.4.0',
    'description': 'A library has light-weight assorted utils in Prue-Python.',
    'long_description': '# pyassorted #\n\nA library has assorted utils in Pure-Python. There are 3 principles:\n\n1. Light-weight\n2. No dependencies\n3. Pythonic usage.\n\n\n* Documentation: https://dockhardman.github.io/pyassorted/\n* PYPI: https://pypi.org/project/pyassorted/\n\n## Installation ##\n```shell\npip install pyassorted\n```\n\n## Modules ##\n- pyassorted.asyncio.executor\n- pyassorted.asyncio.utils\n- pyassorted.cache.cache\n- pyassorted.lock.filelock\n\n\n## Examples ##\n\n### pyassorted.asyncio ###\n\n```python\nimport asyncio\nfrom pyassorted.asyncio import run_func\n\ndef normal_func() -> bool:\n    return True\n\nasync def async_func() -> bool:\n    await asyncio.sleep(0.0)\n    return True\n\nasync main():\n    assert await run_func(normal_func) is True\n    assert await run_func(async_func) is True\n\nasyncio.run(main())\n```\n\n### pyassorted.cache ###\n\n```python\nimport asyncio\nfrom pyassorted.cache import LRU, cached\n\nlru_cache = LRU()\n\n# Cache function\n@cached(lru_cache)\ndef add(a: int, b: int) -> int:\n    return a + b\n\nassert add(1, 2) == 3\nassert lru_cache.hits == 0\nassert lru_cache.misses == 1\n\nassert add(1, 2) == 3\nassert lru_cache.hits == 1\nassert lru_cache.misses == 1\n\n# Cache coroutine\n@cached(lru_cache)\nasync def async_add(a: int, b: int) -> int:\n    await asyncio.sleep(0)\n    return a + b\n\nassert add(1, 2) == 3\nassert lru_cache.hits == 2\nassert lru_cache.misses == 1\n```\n\n### pyassorted.lock ###\n\n```python\nfrom concurrent.futures import ThreadPoolExecutor\nfrom pyassorted.lock import FileLock\n\nnumber = 0\ntasks_num = 100\nlock = FileLock()\n\ndef add_one():\n    global number\n    with lock:\n        number += 1\n\nwith ThreadPoolExecutor(max_workers=40) as executor:\n    futures = [executor.submit(add_one) for _ in range(tasks_num)]\n    for future in futures:\n        future.result()\n\nassert number == tasks_num\n```\n',
    'author': 'Allen Chou',
    'author_email': 'f1470891079@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
