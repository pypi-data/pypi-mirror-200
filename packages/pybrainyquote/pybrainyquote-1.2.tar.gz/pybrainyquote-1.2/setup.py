# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pybrainyquote']
install_requires = \
['bs4', 'furl', 'requests']

entry_points = \
{'console_scripts': ['brainyquote = pybrainyquote:main']}

setup_kwargs = {
    'name': 'pybrainyquote',
    'version': '1.2',
    'description': 'Get quotes from brainyquote. Make you life positive.',
    'long_description': '# PyBrainyquote\n\n\nGet quotes from brainyquote. Make you life positive. :smile:\n\n## Requirements\n\n\n- requests\n- bs4\n- furl\n\n\n## Download\n\n\npip install pybrainyquote\n\n\n## Why\n\nThe original one `brainyquote` is too simple. \n\n\n## Grammar\n\n#### import\n\n```python\nfrom pybrainyquote import *\n\n# or\n# import pybrainyquote as bq\n```\n\n#### get quotes\n```python\nQuote.today(topic=what you like) # get today topic\nget_popular_topics() # have a look at the lists popular topics, if you do not have any idea\nget_topics()\nget_authors()\n\n# just try the following, methods mimicking `bs4`\nQuote.find_all(topic)\nQuote.find(topic)\nQuote.find(topic)\n\nQuote.choice_yaml(yamlfile) # choose a quote in yaml files randomly\nQuote.read_yaml(yamlfile)\n```\n\n## Future\n\nDefine a search engine for quotes, and a method to get one quote randomly. (Completed partly)\n\n\n\nSupport f-string from now on!',
    'author': 'William Song',
    'author_email': '30965609+Freakwill@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Freakwill/pybrainyquote',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
