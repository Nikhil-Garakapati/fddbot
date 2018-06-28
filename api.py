from zeep import Client
from lxml import etree
import datetime
import xml.etree.ElementTree as ET
import json



def RetrieveSecurityToken():
    client = Client(wsdl='./api/wsdls/Security/security.wsdl')

    request = json.load(open('./data/apirequests/RetrieveSecurityToken'))
    response = client.service.RetrieveSecurityToken(request)

    security_token = response['SecurityToken']
    print security_token
    return security_token


def LoginTravelAgent(security_token):
    client = Client('./api/wsdls/TravelAgent/TravelAgents.wsdl')
    request = json.load(open('./data/apirequests/LoginTravelAgent'))
    request['SecurityGUID'] = security_token
    response = client.service.LoginTravelAgent(request)


def RetrieveFareQuote(attributes,security_token):
    client = Client('./api/wsdls/FareQuote/Fare.wsdl',strict=False)
    request = json.load(open('./data/apirequests/RetrieveFareQuote'))
    request['SecurityGUID'] = security_token
    request['FareQuoteDetails'][0]['FareQuoteDetail']['DateOfDeparture'] = attributes['Date']
    request['FareQuoteDetails'][0]['FareQuoteDetail']['Origin'] = attributes['From']
    request['FareQuoteDetails'][0]['FareQuoteDetail']['Destination'] = attributes['To']
    rep = client.service.RetrieveFareQuote(request)


    flights =  rep['_raw_elements'][2]

    tree = ET.ElementTree(flights)
    tree.write('output.xml')

    root = tree.getroot()

    print "first flight is "

    for flightsegment in root:
        for child in flightsegment:
            if "DepartureDate" in child.tag:
                print "Departure Date is ", child.text.split("T")[0]
                print "Departure Time is ", child.text.split("T")[1]
            if "ArrivalDate" in child.tag:
                print "Arrival Date is ", child.text.split("T")[0]
                print "Arrival Time is ", child.text.split("T")[1]

        print "next flight"

    

    