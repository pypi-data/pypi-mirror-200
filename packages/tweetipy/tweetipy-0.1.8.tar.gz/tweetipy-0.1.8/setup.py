# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweetipy',
 'tweetipy.enums.expansions',
 'tweetipy.enums.fields',
 'tweetipy.enums.fields._media',
 'tweetipy.enums.fields._place',
 'tweetipy.enums.fields._poll',
 'tweetipy.enums.fields._tweet',
 'tweetipy.enums.fields._user',
 'tweetipy.handlers',
 'tweetipy.helpers',
 'tweetipy.helpers.QueryBuilder',
 'tweetipy.types',
 'tweetipy.types._attachments',
 'tweetipy.types._includes',
 'tweetipy.types._place',
 'tweetipy.types._scope',
 'tweetipy.types.context_annotation',
 'tweetipy.types.media',
 'tweetipy.types.media.metrics',
 'tweetipy.types.poll',
 'tweetipy.types.tweet',
 'tweetipy.types.tweet.metrics',
 'tweetipy.types.user',
 'tweetipy.types.user.metrics']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'segno>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'tweetipy',
    'version': '0.1.8',
    'description': 'A simple "type hinted" Python client for interacting with Twitter\'s API.',
    'long_description': '# Tweetipy\nA simple type hinted Python client for interacting with Twitter\'s API.\n\n```\npip -m install tweetipy\n```\n\nTo use it, setup a developer account under [developer.twitter.com](https://developer.twitter.com/).\n\nAfter that, create an app from the [developer dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the needed tokens ("API Key and Secret").\n\nPlease note that the library does not yet implement the full Twitter API, but rather only some endpoints that are interesting for my projects. Also, although it is already working, please be aware that this library is still in early development phase and thus breaking changes might occur. In other words, don\'t rely on it for production just yet.\n\nIn any case, feel free to use it for your own projects. Do create issues if anything weird pops up. Pull requests and feature requests are welcome!\n\n# Examples\n\n### Posting a tweet\n```python\nfrom tweetipy import Tweetipy\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Post tweet to Twitter\ntweet = ttpy.tweets.write("I\'m using Twitter API!")\n\n# See the uploaded tweet! :)\nprint(tweet)\n```\n\n### Posting a tweet with media\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.types import MediaToUpload\n\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# First upload the media to Twitter.\nwith open(\'dog.jpeg\', \'rb\') as pic:\n    uploaded_media = ttpy.media.upload(\n        media_bytes=pic.read(),\n        media_type="image/jpeg")\n\n# Then post a tweet, adding the media_id as a parameter.\nttpy.tweets.write(\n    "This tweet contains some media.",\n    media=MediaToUpload([uploaded_media.media_id_string]))\n```\n\n### Searching tweets\n```python\nfrom tweetipy import Tweetipy\n\n# Initialize the client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Treat the \'query\' argument as you would a search box.\nsearch_results = ttpy.tweets.search(query=\'space separated keywords\')\n\n\n# See results 🤩\nfor tweet in search_results:\n    print(tweet)\n```\n\n### Doing advanced searches - Single condition\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.helpers import QueryBuilder\n\n# Initialize the client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# The query builder is your friend :)\nt = QueryBuilder()\n\n# Define the search criteria using the query builder.\nsearch_results = ttpy.tweets.search(\n    query=t.from_user(\'Randogs8\'),\n    sort_order=\'recency\'\n)\n\n# See results 🤩\nfor tweet in search_results:\n    print(tweet)\n```\n\n### Doing advanced searches - Multiple conditions (AND)\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.helpers import QueryBuilder\n\n# Initialize the client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# The query builder is your friend :)\nt = QueryBuilder()\n\n# Use the \'and\' operator (&) to define alternative criteria.\n# The query builder will do some background work for you so this works as\n# expected. 😎\nsearch_results = ttpy.tweets.search(\n    query=t.with_all_keywords([\'dogs\', \'love\']) & t.has.media,\n    sort_order=\'relevancy\'\n)\n\n# See the results 🤩\nfor tweet in search_results:\n    print(tweet)\n```\n\n### Doing advanced searches - Multiple conditions (OR)\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.helpers import QueryBuilder\n\n# Initialize the client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# The query builder is your friend :)\nt = QueryBuilder()\n\n# Use the pipe operator (|) to define alternative criteria.\n# The query builder will do some background work for you so this works as\n# expected. 😎\nsearch_results = ttpy.tweets.search(\n    query=t.from_user(\'Randogs8\') | t.from_user(\'cooldogfacts\'),\n    sort_order=\'recency\'\n)\n\n# See the results 🤩\nfor tweet in search_results:\n    print(tweet)\n```\n',
    'author': 'Federico Giancarelli',
    'author_email': 'hello@federicogiancarelli.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/omirete/tweetipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
