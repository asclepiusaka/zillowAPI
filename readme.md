# zillowAPI

zillowAPI is a zillow.com API wrapper written in python, check [here](https://www.zillow.com/howto/api/APIOverview.htm) for API information.

# Overview

a python practice project, two old implementations are referenced. following API is supported:
- GetZestimate
- GetSearchResult
- GetComps
- GetDeepComps
- GetDeepSearch
- GetUpdatedPropertyDetails


# Usage:
to use this library,import zillow class and create an instance first;
```buildoutcfg
from zillowAPI import zillow

zillow = zillow()
```
all APIs take parameters as required by zillow,for example, to query [GetZestimate](https://www.zillow.com/howto/api/GetZestimate.htm):
```buildoutcfg

```


# requirement

developed and tested on python 3.6, should work on earlier versions. [requests](http://docs.python-requests.org/en/latest/index.html) library is used.

#usage

