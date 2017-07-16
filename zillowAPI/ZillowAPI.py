from . import __version__
import requests
from .ZillowError import NetworkRequestFail,ZillowRequestError
from .ZillowDataType import address,links,zestimate,rent_zestimate
import xml.etree.ElementTree as ET
class zillow():

    base_url = 'http://www.zillow.com/webservice/'

    def GetZestimate(self,key,zpid,rentzestimate=False):
        url = "GetZestimate.htm"
        payload = {
            'zws-id':key,
            'zpid':zpid
        }
        if rentzestimate is not False:
            payload['rentzestimate'] = rentzestimate

        content = self.get_data(url,payload)
        etree = ET.fromstring(content)

        if int(etree.find('./message/code').text) is not 0:
            raise ZillowRequestError(int(etree.find('./message/code').text),
                                     etree.find('./message/text').text)

        return ZestimateData(etree.find('./response'),content)

    def GetSearchResults(self,key,address,citystatezip,rentzestimate=False):
        url = 'GetSearchResults.htm'
        payload = {
            'zws-id':key,
            'address':address,
            'citystatezip':citystatezip
        }
        if rentzestimate is not False:
            payload['rentzestimate'] = rentzestimate

        content = self.get_data(url,payload)
        etree = ET.fromstring(content)

        if int(etree.find('./message/code').text) is not 0:
            raise ZillowRequestError(int(etree.find('./message/code').text),
                                     etree.find('./message/text').text)

        result_list = etree.findall('./response/results/result')

        return SearchResultData(result_list,content)

    def GetComps(self,key,zpid,count,rentzestimate=False):
        url = 'GetComps.htm'
        payload = {
            'zws-id':key,
            'zpid':zpid,
            'count':count
        }
        if rentzestimate is not False:
            payload['rentzestimate'] = rentzestimate

        content = self.get_data(url,payload)
        etree = ET.fromstring(content)

        if int(etree.find('./message/code').text) is not 0:
            raise ZillowRequestError(int(etree.find('./message/code').text),
                                     etree.find('./message/text').text)

        principal_etree = etree.find('./response/properties/principal')
        comp_list = etree.findall('./response/properties/comparables/comp')

        return ComparableResult(principal_etree,comp_list,content)

    def GetDeepComps(self,key,zpid,count,rentzestimate=False):
        url = 'GetDeepComps.htm'
        payload = {
            'zws-id':key,
            'zpid':zpid,
            'count':count
        }
        if rentzestimate is not False:
            payload['rentzestimate'] = rentzestimate

        content = self.get_data(url,payload)
        etree = ET.fromstring(content)

        if int(etree.find('./message/code').text) is not 0:
            raise ZillowRequestError(int(etree.find('./message/code').text),
                                     etree.find('./message/text').text)

        principal_etree = etree.find('./response/properties/principal')
        comp_list = etree.findall('./response/properties/comparables/comp')

        return DeepComparableResult(principal_etree,comp_list,content)

    def GetDeepSearch(self,key,address,citystatezip,rentzestimate=False):
        url = 'GetDeepSearchResults.htm'
        payload = {
            'zws-id':key,
            'address':address,
            'citystatezip':citystatezip
        }
        if rentzestimate is not False:
            payload['rentzestimate'] = rentzestimate

        content = self.get_data(url,payload)
        etree = ET.fromstring(content)

        if int(etree.find('./message/code').text) is not 0:
            raise ZillowRequestError(int(etree.find('./message/code').text),
                                     etree.find('./message/text').text)

        result_list = etree.findall('./response/results/result')

        return DeepSearchResultData(result_list,content)

    def GetUpdatedPropertyDetails(self,key,zpid):
        url = 'GetUpdatedPropertyDetails.htm'
        payload = {
            'zws-id':key,
            'zpid':zpid
        }

        content = self.get_data(url,payload)
        etree = ET.fromstring(content)

        if int(etree.find('./message/code').text) is not 0:
            raise ZillowRequestError(int(etree.find('./message/code').text),
                                     etree.find('./message/text').text)

        return UpdatedPropertyDetails(etree.find('./response'),content)

    def get_data(self,url,payload):
        """
        Request a url through requests module
        :param url: 
        :param payload: 
        :return: 
        """
        try:
            response = requests.get(self.base_url + url,params=payload)
        except(
            requests.exceptions.ConnectionError,requests.exceptions.TooManyRedirects,
            requests.exceptions.Timeout
        ) as e:
            raise NetworkRequestFail from e
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise NetworkRequestFail from e

        return response.text



class ZillowData():
    def __init__(self,content):
        """
        
        :param etree: xml.etree.ElementTree
        :param content: str
        """
        if not content:
            pass
        else:
            self.text = content



class ZestimateData(ZillowData):
    def __init__(self,etree,content):
        super(ZestimateData, self).__init__(content)
        self.zpid = etree.find('./zpid').text
        self.address = address(etree.find('./address'))
        self.links = links(etree.find('./links'))
        self.zestimate = zestimate(etree.find('./zestimate'))
        if etree.find('./rentzestimate'):
            self.rent_zestimate = rent_zestimate(etree.find('./rentzestimate'))
        else:
            self.rent_zestimate = None

class SearchResultData(ZillowData):
    def __init__(self,etree_list,content):
        super(SearchResultData, self).__init__(content)
        self.results =[]
        for result in etree_list:
            self.results.append(ZestimateData(result,None))

class DeepSearchResultData(ZillowData):
    def __init__(self,etree_list,content):
        super(DeepSearchResultData, self).__init__(content)
        self.results =[]
        for result in etree_list:
            self.results.append(DeepZestimateData(result,None))

class ComparableData(ZestimateData):
    def __init__(self,etree):
        super(ComparableData, self).__init__(etree,None)
        self.score = float(etree.get('score'))

class DeepComparableData(ComparableData):
    def __init__(self,etree):
        super(DeepComparableData, self).__init__(etree)
        self.tax_assessment_year = etree.find('./taxAssessmentYear').text
        self.tax_assessment = etree.find('./taxAssessment').text
        self.year_built = etree.find('./yearBuilt').text
        self.lot_size = etree.find('./lotSizeSqFt').text
        self.finished_size = etree.find('./finishedSqFt').text
        self.bathrooms = etree.find('./bathrooms').text
        self.bedrooms = etree.find('./bedrooms').text
        self.last_sold_date = etree.find('./lastSoldDate').text
        self.last_sold_price = etree.find('.lastSoldPrice').text

class DeepZestimateData(ZestimateData):
    def __init__(self,etree,content):
        super(DeepZestimateData, self).__init__(etree,content)
        self.tax_assessment_year = etree.find('./taxAssessmentYear').text
        self.tax_assessment = etree.find('./taxAssessment').text
        self.year_built = etree.find('./yearBuilt').text
        self.lot_size = etree.find('./lotSizeSqFt').text
        self.finished_size = etree.find('./finishedSqFt').text
        self.bathrooms = etree.find('./bathrooms').text
        self.bedrooms = etree.find('./bedrooms').text
        self.last_sold_date = etree.find('./lastSoldDate').text
        self.last_sold_price = etree.find('.lastSoldPrice').text

class ComparableResult(ZillowData):
    def __init__(self,etree,comps_list,content):
        super(ComparableResult, self).__init__(content)
        self.principal = ZestimateData(etree,None)
        self.comps = []
        for comps in comps_list:
            self.comps.append(ComparableData(comps))


class DeepComparableResult(ZillowData):
    def __init__(self,etree,comps_list,content):
        super(DeepComparableResult, self).__init__(content)
        self.principal = DeepZestimateData(etree,None)
        self.comps = []
        for comps in comps_list:
            self.comps.append(DeepComparableData(comps))

class UpdatedPropertyDetails(ZillowData):
    def __init__(self,etree,content):
        super(UpdatedPropertyDetails, self).__init__(content)
        self.address = address(etree.find('./address'))
        self.zpid = etree.find('./zpid').text
        self.usecode = etree.find('./editedFacts/useCode').text
        self.bedrooms = etree.find('./editedFacts/bedrooms').text
        self.bathrooms = etree.find('./editedFacts/bathrooms').text
        self.finished_size = etree.find('./editedFacts/finishedSqFt').text
        self.lot_size = etree.find('./editedFacts/lotSizeSqFt').text
        self.year_built = etree.find('./editedFacts/yearBuilt').text
        self.year_updated = etree.find('./editedFacts/yearUpdated').text
        self.num_floor = etree.find('./editedFacts/numFloors').text
        self.basement = etree.find('./editedFacts/basement').text
        self.roof = etree.find('./editedFacts/roof').text
        self.view = etree.find('./editedFacts/view').text
        self.parkingType = etree.find('./editedFacts/parkingType').text
        self.heating_sources = etree.find('./editedFacts/heatingSources').text
        self.heating_system = etree.find('./editedFacts/heatingSystem').text
        self.rooms = etree.find('./editedFacts/rooms').text
