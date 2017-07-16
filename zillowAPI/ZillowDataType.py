import xml.etree.ElementTree as ET

class address():
    def __init__(self,etree):
        self.street = etree.find('./street').text
        self.zipcode = int(etree.find('./zipcode').text)
        self.city = etree.find('./city').text
        self.state = etree.find('./state').text
        self.latitude = float(etree.find('./latitude').text)
        self.longitude = float(etree.find('./longitude').text)

class links():
    def __init__(self,etree):
        self.home_details = etree.find('./homedetails').text
        self.map_this_home = etree.find('./mapthishome').text
        self.similar_sales = etree.find('./comparables').text

class zestimate():
    def __init__(self,etree):
        self.zestimate = int(etree.find('./amount').text)
        self.last_updated = etree.find('./last-updated').text
        self.value_change = etree.find('./valueChange').text
        self.valuation_low = etree.find('./valuationRange/low').text
        self.valuation_high = etree.find('./valuationRange/high').text
        self.percentile = etree.find('./percentile').text

class rent_zestimate():
    def __init__(self,etree):
        self.zestimate = int(etree.find('./amount').text)
        self.last_updated = etree.find('./last-updated').text
        self.value_change = etree.find('./valueChange').text
        self.valuation_low = etree.find('./valuationRange/low').text
        self.valuation_high = etree.find('./valuationRange/high').text