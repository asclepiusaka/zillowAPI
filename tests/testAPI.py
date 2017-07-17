from zillowAPI import zillow
from zillowAPI import ZillowDataType
from zillowAPI import ZillowAPI
from zillowAPI import ZillowError

import unittest
import xml.etree.ElementTree as ET

class ZillowTest(unittest.TestCase):
    def setUp(self):
        with open('tests/apiKeys','r') as f:
            self.apikey = f.readline()
        self.apikey = self.apikey.strip('\n')

    def test_get_data_through_get_zestimate(self):
        url = 'GetZestimate.htm'
        payload = {'zws-id':self.apikey,'zpid':2146876387}
        z = zillow()
        r = z.get_data(url, payload)
        self.assertIsInstance(r,str,"return message is not string")
        self.assertTrue(r.startswith('<?xml'))

        with open('tests/temp','w') as f:
            f.write(r)

    def test_GetZestimate(self):
        a = zillow().GetZestimate(self.apikey,zpid=2146876387,rentzestimate=True)
        self.assertIsInstance(a,ZillowAPI.ZestimateData)
        self.assertIsInstance(a.address,ZillowDataType.address)
        self.assertIsInstance(a.zestimate,ZillowDataType.zestimate)
        self.assertIsInstance(a.rent_zestimate,ZillowDataType.rent_zestimate)
        self.assertIsInstance(a.links,ZillowDataType.links)
        #make sure the raw response text is saved
        self.assertIsInstance(a.text,str)
        self.assertTrue(int(a.zpid)==2146876387)
        self.assertTrue(a.text.startswith('<?xml'))
        with self.assertRaises(ZillowError.ZillowRequestError) as cm:
            zillow().GetZestimate(self.apikey,214687638711,True)

        RE = cm.exception
        self.assertTrue(RE.code == 500)


    def test_GetSearchResults(self):
        a = zillow().GetSearchResults(self.apikey,'2114 Bigelow Ave','Seattle, WA',True)
        self.assertIsInstance(a,ZillowAPI.SearchResultData)
        self.assertIsInstance(a.results,list)
        ins = a.results[0]
        self.assertIsInstance(ins.address,ZillowDataType.address)
        self.assertIsInstance(ins.zestimate,ZillowDataType.zestimate)
        self.assertIsInstance(ins.rent_zestimate,ZillowDataType.rent_zestimate)
        self.assertIsInstance(ins.links,ZillowDataType.links)
        with self.assertRaises(AttributeError):
            getattr(ins,'text')
        self.assertIsInstance(a.text,str)
        self.assertTrue(a.text.startswith('<?xml'))

    def test_GetComps(self):
        a = zillow().GetComps(self.apikey,48749425,5,True)
        self.assertIsInstance(a,ZillowAPI.ComparableResult)
        self.assertIsInstance(a.text,str)
        self.assertIsInstance(a.principal,ZillowAPI.ZestimateData)
        self.assertIsInstance(a.comps,list)
        self.assertTrue(len(a.comps)==5)
        self.assertIsInstance(a.comps[0],ZillowAPI.ComparableData)
        comp_instance = a.comps[0]
        self.assertIsInstance(comp_instance.score,float)

    def test_GetDeepComps(self):
        a = zillow().GetDeepComps(self.apikey,48749425,5,True)
        self.assertIsInstance(a,ZillowAPI.DeepComparableResult)
        principal = a.principal
        self.assertIsInstance(principal,ZillowAPI.DeepZestimateData)
        comps = a.comps
        self.assertIsInstance(comps,list)
        self.assertIsInstance(comps[0],ZillowAPI.DeepComparableData)
        self.assertIsInstance(comps[0].score,float)

    def test_GetDeepSearch(self):
        a = zillow().GetDeepSearch(self.apikey,'2114 Bigelow Ave','Seattle, WA')
        self.assertIsInstance(a,ZillowAPI.DeepSearchResultData)
        self.assertIsInstance(a.results,list)
        self.assertIsInstance(a.results[0],ZillowAPI.DeepZestimateData)

    def test_GetUpdatedPropertyDetails(self):
        a = zillow().GetUpdatedPropertyDetails(self.apikey,48749425)
        self.assertIsInstance(a,ZillowAPI.UpdatedPropertyDetails)


class DataTypeTest(unittest.TestCase):
    def setUp(self):
        self.etree = ET.parse('tests/getZestimate.xml')

    def test_class_address(self):
        address = ZillowDataType.address(self.etree.find('./response/address'))
        self.assertIsInstance(address.longitude,float)
        self.assertIsInstance(address.latitude,float)
        self.assertIsInstance(address.zipcode,int)
        self.assertIsInstance(address.street,str)
        self.assertIsInstance(address.street,str)

    def test_class_links(self):
        links = ZillowDataType.links(self.etree.find('./response/links'))
        self.assertIsInstance(links.home_details,str)
        self.assertTrue(links.home_details.startswith('http://'))
        self.assertIsInstance(links.map_this_home,str)
        self.assertIsInstance(links.similar_sales,str)

    def test_class_zestimate(self):
        zestimate = ZillowDataType.zestimate(self.etree.find('./response/zestimate'))
        self.assertIsInstance(zestimate.zestimate,int)
        self.assertIsInstance(zestimate.last_updated,str)
        self.assertIsInstance(zestimate.percentile,str)
        self.assertIsInstance(zestimate.valuation_high,str)
        self.assertIsInstance(zestimate.valuation_low,str)

    def test_class_rent_zestimate(self):
        with self.assertRaises(AttributeError):
            rent_zestimate = ZillowDataType.rent_zestimate(self.etree.find('./response/rentzestimate'))
