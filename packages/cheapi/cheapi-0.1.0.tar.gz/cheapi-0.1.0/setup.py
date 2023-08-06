# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cheapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cheapi',
    'version': '0.1.0',
    'description': 'Make API usage cheap! Caching wrapper for third party APIs.',
    'long_description': '# Cheapi (cheap API) \n\nLightweight wrapper to cache expensive function results in-memory or on disk.\n\n\n## Installation\n\n```bash\npip install cheapi\n```\n\n## Usage\n\n```python\nfrom cheapi import CachingWrapper\nimport openai\n\n\ndef _ask_chatgpt(prompt):\n    res = openai.ChatCompletion.create(\n        model="gpt-4",\n        messages=[\n            {"role": "system", "content": "You are a helpful assistant for a software engineer."},\n            {"role": "user", "content": prompt}\n        ],\n        temperature=0,\n        timeout=10,\n    )\n    choice, *_ = res["choices"]\n    usage = res["usage"]["total_tokens"]\n    print(f"OpenAI usage: {usage}")\n\n    result = choice["message"]["content"]\n    return result\n\n\nash_chatgpt = CachingWrapper(_ask_chatgpt, cache_backend="memory")\n\nfor i in range(2):\n    print(ash_chatgpt("Write a short joke about caching?") + "\\n")\n```\nor even simpler:\n```python\n\nfrom cheapi import cached\n\n@cached(cache_backend="memory")\ndef ask_chatgpt(prompt):\n    ...\n\nfor i in range(2):\n    print(ask_chatgpt("Write a short joke about caching?") + "\\n")\n```\n\n## Caching backends\n\nUsing memory backend is mostly equivalent to using `functools.lru_cache` but with more configuration.\nSQLite backend is useful for persistent caching, and is similar to `joblib.Memory`.\nCloud backend is being dreamed of, but not implemented yet.\n\n## Why? \n\n[NIH](https://en.wikipedia.org/wiki/Not_invented_here) + so I could [RIIR](https://www.urbandictionary.com/define.php?term=riir) later.',
    'author': 'Arseny Kravchenko',
    'author_email': 'me@arseny.info',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
