# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweetipy',
 'tweetipy.handlers',
 'tweetipy.helpers',
 'tweetipy.helpers.QueryBuilder',
 'tweetipy.types']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'segno>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'tweetipy',
    'version': '0.1.7',
    'description': 'A simple "type hinted" Python client for interacting with Twitter\'s API.',
    'long_description': '# Tweetipy\nA simple type hinted Python client for interacting with Twitter\'s API.\n\n```\npip -m install tweetipy\n```\n\nTo use it, setup a developer account under [developer.twitter.com](https://developer.twitter.com/).\n\nAfter that, create an app from the [developer dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the needed tokens ("API Key and Secret").\n\nPlease note that the library does not yet implement the full Twitter API, but rather only some endpoints that are interesting for my projects. Also, although it is already working, please be aware that this library is still in early development phase and thus breaking changes might occur. In other words, don\'t rely on it for production just yet.\n\nIn any case, feel free to use it for your own projects. Do create issues if anything weird pops up. Pull requests and feature requests are welcome!\n\n# Examples\n\n### Posting a tweet\n```python\nfrom tweetipy import Tweetipy\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Post tweet to Twitter\ntweet: Tweet = ttpy.tweets.write("Look mom, I\'m using Twitter API!")\n\n# See the uploaded tweet! :)\nprint(tweet)\n```\n\n### Posting a tweet with media\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.types import Media\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Read some picture and upload the bytes to Twitter\npic_bytes = open(\'path/to/pic.jpeg\', \'rb\').read()\nuploaded_media = ttpy.media.upload(pic_bytes, media_type="image/jpeg")\n\n# Post media tweet to Twitter\ntweet = ttpy.tweets.write(\n    "This tweet contains some media!",\n    media=Media([uploaded_media.media_id_string]))\n\n# See the uploaded media tweet! :)\nprint(tweet)\n```\n\n### Searching tweets\n```python\nfrom tweetipy import Tweetipy\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Find tweets containing some keywords\nsearch_results = ttpy.tweets.search(query=\'space separated keywords\')\n\n# See the results\nprint(search_results)\n```\n\n### Doing advanced searches - Single condition\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.helpers import QueryBuilder\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Initialize the query builder\nt = QueryBuilder()\n\n# Find tweets containing some keywords\nsearch_results = ttpy.tweets.search(\n    query=t.from_user(\'Randogs8\'),\n    sort_order=\'recency\'\n)\n\n# See the results\nprint(search_results)\n```\n\n### Doing advanced searches - Multiple conditions (AND)\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.helpers import QueryBuilder\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Initialize the query builder\nt = QueryBuilder()\n\n# Find tweets containing some keywords\nsearch_results = ttpy.tweets.search(\n    query=t.with_all_keywords([\'dogs\', \'love\']) & t.has.media,\n    sort_order=\'recency\'\n)\n\n# See the results\nprint(search_results)\n```\n\n### Doing advanced searches - Multiple conditions (OR)\n```python\nfrom tweetipy import Tweetipy\nfrom tweetipy.helpers import QueryBuilder\n\n# Initialize client\nttpy = Tweetipy(\n    \'YOUR_TWITTER_API_KEY\',\n    \'YOUR_TWITTER_API_KEY_SECRET\')\n\n# Initialize the query builder\nt = QueryBuilder()\n\n# Find tweets containing some keywords\nsearch_results = ttpy.tweets.search(\n    query=t.from_user(\'Randogs8\') | t.from_user(\'cooldogfacts\'),\n    sort_order=\'recency\'\n)\n\n# See the results\nprint(search_results)\n```\n',
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
