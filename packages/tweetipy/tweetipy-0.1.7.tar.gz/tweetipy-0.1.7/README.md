# Tweetipy
A simple type hinted Python client for interacting with Twitter's API.

```
pip -m install tweetipy
```

To use it, setup a developer account under [developer.twitter.com](https://developer.twitter.com/).

After that, create an app from the [developer dashboard](https://developer.twitter.com/en/portal/dashboard) and generate the needed tokens ("API Key and Secret").

Please note that the library does not yet implement the full Twitter API, but rather only some endpoints that are interesting for my projects. Also, although it is already working, please be aware that this library is still in early development phase and thus breaking changes might occur. In other words, don't rely on it for production just yet.

In any case, feel free to use it for your own projects. Do create issues if anything weird pops up. Pull requests and feature requests are welcome!

# Examples

### Posting a tweet
```python
from tweetipy import Tweetipy

# Initialize client
ttpy = Tweetipy(
    'YOUR_TWITTER_API_KEY',
    'YOUR_TWITTER_API_KEY_SECRET')

# Post tweet to Twitter
tweet: Tweet = ttpy.tweets.write("Look mom, I'm using Twitter API!")

# See the uploaded tweet! :)
print(tweet)
```

### Posting a tweet with media
```python
from tweetipy import Tweetipy
from tweetipy.types import Media

# Initialize client
ttpy = Tweetipy(
    'YOUR_TWITTER_API_KEY',
    'YOUR_TWITTER_API_KEY_SECRET')

# Read some picture and upload the bytes to Twitter
pic_bytes = open('path/to/pic.jpeg', 'rb').read()
uploaded_media = ttpy.media.upload(pic_bytes, media_type="image/jpeg")

# Post media tweet to Twitter
tweet = ttpy.tweets.write(
    "This tweet contains some media!",
    media=Media([uploaded_media.media_id_string]))

# See the uploaded media tweet! :)
print(tweet)
```

### Searching tweets
```python
from tweetipy import Tweetipy

# Initialize client
ttpy = Tweetipy(
    'YOUR_TWITTER_API_KEY',
    'YOUR_TWITTER_API_KEY_SECRET')

# Find tweets containing some keywords
search_results = ttpy.tweets.search(query='space separated keywords')

# See the results
print(search_results)
```

### Doing advanced searches - Single condition
```python
from tweetipy import Tweetipy
from tweetipy.helpers import QueryBuilder

# Initialize client
ttpy = Tweetipy(
    'YOUR_TWITTER_API_KEY',
    'YOUR_TWITTER_API_KEY_SECRET')

# Initialize the query builder
t = QueryBuilder()

# Find tweets containing some keywords
search_results = ttpy.tweets.search(
    query=t.from_user('Randogs8'),
    sort_order='recency'
)

# See the results
print(search_results)
```

### Doing advanced searches - Multiple conditions (AND)
```python
from tweetipy import Tweetipy
from tweetipy.helpers import QueryBuilder

# Initialize client
ttpy = Tweetipy(
    'YOUR_TWITTER_API_KEY',
    'YOUR_TWITTER_API_KEY_SECRET')

# Initialize the query builder
t = QueryBuilder()

# Find tweets containing some keywords
search_results = ttpy.tweets.search(
    query=t.with_all_keywords(['dogs', 'love']) & t.has.media,
    sort_order='recency'
)

# See the results
print(search_results)
```

### Doing advanced searches - Multiple conditions (OR)
```python
from tweetipy import Tweetipy
from tweetipy.helpers import QueryBuilder

# Initialize client
ttpy = Tweetipy(
    'YOUR_TWITTER_API_KEY',
    'YOUR_TWITTER_API_KEY_SECRET')

# Initialize the query builder
t = QueryBuilder()

# Find tweets containing some keywords
search_results = ttpy.tweets.search(
    query=t.from_user('Randogs8') | t.from_user('cooldogfacts'),
    sort_order='recency'
)

# See the results
print(search_results)
```
