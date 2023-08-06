# PyBrainyquote


Get quotes from brainyquote. Make you life positive. :smile:

## Requirements


- requests
- bs4
- furl


## Download


pip install pybrainyquote


## Why

The original one `brainyquote` is too simple. 


## Grammar

#### import

```python
from pybrainyquote import *

# or
# import pybrainyquote as bq
```

#### get quotes
```python
Quote.today(topic=what you like) # get today topic
get_popular_topics() # have a look at the lists popular topics, if you do not have any idea
get_topics()
get_authors()

# just try the following, methods mimicking `bs4`
Quote.find_all(topic)
Quote.find(topic)
Quote.find(topic)

Quote.choice_yaml(yamlfile) # choose a quote in yaml files randomly
Quote.read_yaml(yamlfile)
```

## Future

Define a search engine for quotes, and a method to get one quote randomly. (Completed partly)



Support f-string from now on!