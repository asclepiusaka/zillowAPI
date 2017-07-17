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
>>>from zillowAPI import zillow

>>>z= zillow()
```
all APIs take parameters as required by zillow,for example, to query [GetZestimate](https://www.zillow.com/howto/api/GetZestimate.htm):
```buildoutcfg
>>>apikey = 'zws-id'    #your apikey
>>>ZestimateResult=z.GetZestimate(apikey,zpid=48749425,rentzestimate=true)
```
the response is wrapped into class and all the information can be accessed through attribute, such as:
```buildoutcfg
>>>ZestimateResult.address.street
'2114 Bigelow Ave N'
>>>ZestimateResult.links.home_details_page
'http://www.zillow.com/homedetails/2114-Bigelow-Ave-N-Seattle-WA-98109/48749425_zpid/'
```
when result contains multiple properties, they will be saved in a list, (GetSearchResults also returns list because there is case that multiple properties is returned):
```buildoutcfg
>>>CompsResult = z.GetComps(apikey,48749425,count=5)
>>>type(CompsResut.comps)
<class 'list'>
```
error code in xml is handled properly, when a return code != 0 is found, a ZillowRequestError exception will be raised
```buildoutcfg
>>>z.GetZestimate(self.apikey,214687638711,True)
Zillow Request Error: 500, Error: invalid or missing zpid parameter
```
ZillowRequestError has .code and .message field, check zillow API for more information.

GetZestimate, GetSearchResults support fields:
- address
    - street
    - zipcode
    - city
    - state
    - latitude
    - longitude
- links
    - home_details
    - map_this_home
    - similar_sales
- zestimate
    - zestimate
    - last_updated
    - value_change
    - valuation_low 
    - valuation_high
    - percentile
- rentzestimate
    - zestimate
    - last_updated
    - value_change
    - valuation_low 
    - valuation_high

except for above fields, GetDeepComps, GetDeepSearchResults also support:
- tax_assessment_year
- tax_assessment
- year_built 
- lot_size 
- finished_size
- bathrooms
- bedrooms 
- last_sold_date 
- last_sold_price 

GetUpdatedProertyDetails supports some information provided by property owner or agent:
- address
- zpid 
- usecode 
- bedrooms 
- bathrooms 
- finished_size 
- lot_size
- year_built 
- year_updated 
- num_floor 
- basement 
- roof 
- view 
- parkingType  
- heating_sources
- heating_system
- rooms


# requirement

developed and tested on python 3.6, should work on earlier versions. [requests](http://docs.python-requests.org/en/latest/index.html) library is used.


