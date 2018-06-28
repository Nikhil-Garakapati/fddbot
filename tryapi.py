import requests
import json 
#Flight Api


def searchflights(attributes,headers):

  data = {
    "promoCode": "PROMO",
    "cabinClass": "economy",
    "searchCriteria": [
      {
        "origin": attributes['From'],
        "dest": attributes['To'],
        "direction": "outBound",
        "date": str(attributes['Date']),
        "isOriginMetro": "true",
        "isDestMetro": "false"
      }
    
    ],
    "paxInfo": {
      "adultCount": 1,
      "infantCount": 0,
      "childCount": 0
    }
  }

  print attributes['From']
  print attributes['To']
  print attributes['Date']
  print headers
  url = "https://devapi.flydubai.com/res/uat2/ibe/v1/api/flights/1"


  response = requests.post(url,json=data,headers=headers)

  f = open('data1',"w")
  json.dump(data,f)

  # print response.content
  headers['securitytoken'] = response.headers['securitytoken']
  return response,headers

  # return len(response.json()['segments'][0]['flights'])

  # print "number of available flights", len(response.json()['segments'][0]['flights'])

# security_token = { 'securitytoken': response.headers['securitytoken'] }
# headers.update(security_token)

# print response

def Prepare1(headers,flightnumber,flights):

  prepare1request = json.load(open('prepare1'))

  data = json.load(open('data1'))

  response = flights.json()

  prepare1request['searchRequest']['searchCriteria'] = data['searchCriteria']
  prepare1request['searchRequest']['paxInfo'] = data['paxInfo']
  # print prepare1request['selectedFlights'][0]
  prepare1request['selectedFlights'][0]['origin'] = response['segments'][0]['flights'][flightnumber]['origin']
  prepare1request['selectedFlights'][0]['dest'] = response['segments'][0]['flights'][flightnumber]['dest']
  prepare1request['selectedFlights'][0]['lfId'] = response['segments'][0]['flights'][flightnumber]['lfId']
  prepare1request['selectedFlights'][0]['departureDate'] = response['segments'][0]['flights'][flightnumber]['departureDate']
  prepare1request['selectedFlights'][0]['isAvailabile'] = response['segments'][0]['flights'][flightnumber]['isAvailabile']
  prepare1request['selectedFlights'][0]['stops'] = response['segments'][0]['flights'][flightnumber]['stops']
  prepare1request['selectedFlights'][0]['totalDuration'] = response['segments'][0]['flights'][flightnumber]['totalDuration']
  prepare1request['selectedFlights'][0]['departureTime'] = response['segments'][0]['flights'][flightnumber]['departureTime']
  prepare1request['selectedFlights'][0]['arrivalTime'] = response['segments'][0]['flights'][flightnumber]['arrivalTime']
  prepare1request['selectedFlights'][0]['selectedFare'] = response['segments'][0]['flights'][flightnumber]['fareTypes'][0]
  prepare1request['selectedFlights'][0]['legs'] = response['segments'][0]['flights'][flightnumber]['legs']


# # print prepare1request

  print headers

  url = 'https://devapi.flydubai.com/res/uat2/ibe/v1/api/itinerary/prepare'
  response = requests.post(url,json=prepare1request,headers=headers)
  json.dump(response.json(),open('prepare1response',"w"))
  # print response
  return response

# # print response.json()


def Prepare2(headers,firstname,lastname):

  response = json.load(open('prepare1response'))
  data = json.load(open('data1'))


  prepare2request = json.load(open('prepare2'))
  url = 'https://devapi.flydubai.com/res/uat2/ibe/v1/api/itinerary/prepare'


# # print response['passengerList']
  prepare2request['searchRequest']['searchCriteria'] = data['searchCriteria']
  prepare2request['searchRequest']['paxInfo'] = data['paxInfo']
  # prepare2request['passengerList'] = response['passengerList']
  prepare2request['selectedFlights'] = response['selectedFlights']
  prepare2request['passengerList'][0]['firstName'] = firstname
  prepare2request['passengerList'][0]['lastName'] = lastname

# # print prepare2request

# f = open('prepare2request.json',"w")

# json.dump(prepare2request,f)


  response = requests.post(url,json=prepare2request,headers=headers)
  json.dump(response.json(),open('prepare2response',"w"))


  return response


def Prepare3(headers,firstname,lastname):
# print response
  response = json.load(open('prepare2response'))
  data = json.load(open('data1'))

  url = 'https://devapi.flydubai.com/res/uat2/ibe/v1/api/itinerary/prepare'

# response = response.json()

  prepare3request = json.load(open('prepare2'))


  prepare3request['searchRequest']['searchCriteria'] = data['searchCriteria']
  prepare3request['searchRequest']['paxInfo'] = data['paxInfo']
  prepare3request['passengerList'][0]['firstName'] = firstname
  prepare3request['passengerList'][0]['lastName'] = lastname



  prepare3request['selectedFlights'] = response['selectedFlights']
  response = requests.post(url,json=prepare3request,headers=headers)

  print response  
  return response


def Paylater(headers):

  url = 'https://devapi.flydubai.com/res/uat2/ibe/v1/api/payment/paylater'
  response =  requests.post(url,headers=headers) 
  # response = requests.post(url,headers=headers)
  return response
# # print response.content


def conformation(headers,firstname,lastname):

  url = 'https://devapi.flydubai.com/res/uat2/ibe/v1/api/itinerary/confirm'
  response = json.load(open('prepare2response'))
  data = json.load(open('data1'))


# response = response.json()

  prepare3request = json.load(open('prepare2'))


  prepare3request['searchRequest']['searchCriteria'] = data['searchCriteria']
  prepare3request['searchRequest']['paxInfo'] = data['paxInfo']
  prepare3request['passengerList'][0]['firstName'] = firstname
  prepare3request['passengerList'][0]['lastName'] = lastname


  prepare3request['selectedFlights'] = response['selectedFlights']
  response = requests.post(url,json=prepare3request,headers=headers)
  return response
