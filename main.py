from Intents import Intent
from Contexts import Context,FirstGreeting,IntentComplete,SpellConformation
import os
import json
from Entities import *
import random
from attributegetter import *
from generatengrams import ngrammatch
from spell import *
from api import *
from attributegetter import *
from tryapi import *

def loadEntities(path):
    entities = []
    for fil in os.listdir(path):
        if fil.endswith('json.new'):
            with open(path+'/'+fil) as f:
                dat = json.load(f)
                category = Named(dat['name'])
                entries = []
                for i in dat['entries']:
                    entries += [Entry(i['value'], i['synonyms'])]
                category.entries = entries
                entities += [category]
    return entities

def loadIntent(path, intent):
    with open(path) as fil:
        dat = json.load(fil)
        intent = dat[intent]
        return Intent(intent['intentname'],intent['Parameters'])
        #exec('intent = ' + dat[intent]['intentname'] + '('


def greet():
    return 'Welcome to the flydubai chat assistant\n\
    Here you can talk to us about\n\
    * Search flights\n\
    * Book flights\n\
    * Track flights\n'

def attributeGetter(uinput, context,attributes):
    words = uinput.split()
    if('from' in words):
        attributes['From'] = words[words.index('from') +1]
    if('to' in words):
        attributes['To'] = words[words.index('to') + 1]
    return attributes, uinput

def intentIdentifier(clean_input, context,current_intent):
    clean_input = clean_input.lower()
    scores = ngrammatch(clean_input)
    scores = sorted_by_second = sorted(scores, key=lambda tup: tup[1])
    # print clean_input
    # print 'scores', scores

    return loadIntent('data/params/params.cfg','FlightSearch')
    if(current_intent=="None"):
        if(clean_input=="search"):
            return loadIntent('data/params/params.cfg', 'FlightSearch')
        if(clean_input=='book'):
            return loadIntent('data/params/params.cfg','FlightBook')
        if(clean_input=='track'):
            return loadIntent('data/params/params.cfg','FlightTrack')
        else:
            if scores[-1][0].startswith('book'):
                return loadIntent('data/params/params.cfg','FlightBook')
            elif scores[-1][0].startswith('search'):
                return loadIntent('data/params/params.cfg','FlightSearch')
            else:
                return loadIntent('data/params/params.cfg','FlightSearch')
    else:
        return current_intent


def checkrequiredparams(intent,attributes):
    for para in intent.params:
        if para.required=='True':
            if para.name not in attributes.keys():
                return random.choice(para.prompts), Context(para.context)
    print attributes
    return 'Searching the best fares from %s to %s for %s :)' %(attributes['From'], attributes['To'], attributes['Date']),  IntentComplete()

def inputProcessor(uinput, context,attributes, current_intent):
    
	if uinput.startswith('exit'):
		exit()

        attributes, cleaned_input = getattributes(uinput, context,attributes)
        return attributes, intentIdentifier(cleaned_input, context, current_intent)

class chat():
    def __init__(self):
        self.active_contexts = []
        self.attributes = {}
        # entities = loadEntities('data/entities')
        self.context  = FirstGreeting()
        self.current_intent = "None"
        self.flights = {}
        self.flag=0
        #return greet()
        self.headers = {
            "client_id": "2b1c38949f544a2baa914588d9098c69",
            "client_secret": "f0114c91C6ea41F19d3255f76E930031"
        }

    def bolo(self, user_input):
        #user_input = raw_input('>>')
        

        #print 'blabalbalb'
        if((self.context.name=='SpellConformation')&(self.context.name!='Prepare1Called')):
            print self.context.name
            if(user_input.lower()=='yes'):
                self.context.tobecorrected[self.context.index] = self.context.correct
                user_input = ' '.join(self.context.tobecorrected)
                self.context  = self.context.contexttobestored
            else:
                self.context = self.context.contexttobestored
                print self.context
                print self.attributes
                return "then what did you mean?"

        user_input = user_input.split()

        if(self.context.name!='Prepare1Called'):
            for i in range(len(user_input)):
                word = user_input[i].lower()
                potentialwords = list(spellcorrection('./data/big.txt',word))
                if(potentialwords[0]!=word):
                    potentialwords = list(spellcorrection('./data/date.txt',word))
                    print potentialwords

                    if(potentialwords[0]!=word):
                        self.context = SpellConformation(i,potentialwords[0],user_input,self.context) 
                        return "did you mean " +     potentialwords[0] +  "?"
                        break
            
        user_input = ' '.join(user_input)
   

        if(self.context.name!='SpellConformation'):
            self.attributes,new_intent  = inputProcessor(user_input,self.context,self.attributes,self.current_intent)
            print user_input,self.attributes
            self.current_intent = new_intent
            print self.current_intent
            if((self.context.name!='FlightsSearched')&(self.context.name!='Prepare1Called')):
                print self.attributes
                prompt, self.context = checkrequiredparams(self.current_intent,self.attributes)
                return prompt

    def Search(self,user_input):


        if(self.context.name=='IntentComplete'):

            self.flights,self.headers = searchflights(self.attributes,self.headers)


            if(len(self.flights.json()['segments'][0]['flights'])==0):
                self.context = Context('FlightSearch_dialog_Date')
                del self.attributes['Date']
                return "There are no flights available on the given date please give alternative date"
            else:
                response = 'number of available flights are:' + str(len(self.flights.json()['segments'][0]['flights'])) + '\n\n' + "details are given below:" + '\n\n'
                for i in range(len(self.flights.json()['segments'][0]['flights'])):
                    response += str(i) + ":" + '\n\n'
                    response += "Departure Time: " + str(self.flights.json()['segments'][0]['flights'][i]['departureTime'].split('T')[1]) + '\n\n'
                    response += "Arrival Time: "  + str(self.flights.json()['segments'][0]['flights'][i]['arrivalTime'].split('T')[1]) + '\n\n'
                    response += "Fare: " + str(self.flights.json()['segments'][0]['flights'][i]['fareTypes'][0]['fare']['totalFare']) + '\n\n'

                response += "Please select the flight number"

                self.context = Context('FlightsSearched')

                return response
        
        if(self.context.name=='FlightsSearched'):
            flightnumber = int(user_input)
            response = Prepare1(self.headers,flightnumber,self.flights)
            print response.content

            self.context = Context('Prepare1Called')
            return "Please Provide Passenge Name"


        if(self.context.name=='Prepare1Called'):

            self.context = Context('InformationConformation')
            names,matches = getNames(user_input, Context('FlightSearch_dialog_PassengerName'),{'Name':[]})   
            if names!=[]:
                self.attributes['PassengerName'] = names[0]
                print self.attributes
            return "Please conform the infromation provided" +  '\n\n'  + "Origin: " + self.attributes['From'] + '\n\n' + "Destination: " + self.attributes['To'] + '\n\n' + "Departure Date: " + str(self.attributes['Date']) + '\n\n' + "Passenger Name: " + self.attributes['PassengerName'] + '\n\n' 

        if(self.context.name=='InformationConformation'):
            if(user_input=='yes'):
                self.context.name='InformationCorrect'

        if(self.context.name=='InformationCorrect'):

            
            firstname = self.attributes['PassengerName'].split(' ')[0]
            lastname = self.attributes['PassengerName'].split(' ')[1]
            response = Prepare2(self.headers,firstname,lastname)
            print response
            response = Prepare3(self.headers,firstname,lastname)
            response = Paylater(self.headers)
            print response
            response = conformation(self.headers,firstname,lastname)
            json.dump(response.json(),open('conformation',"w"))
            print response.json()['pnrInformation']['bookingReference']
            return 'booking done!. Booking Reference is ' + response.json()['pnrInformation']['bookingReference']

            '''
            if(context.name=='IntentComplete'):
                security_token = RetrieveSecurityToken()
                LoginTravelAgent(security_token)
                RetrieveFareQuote(attributes,security_token)
                return "here are the available flights"
            '''

            #print 'intent', current_intent.name
            #print context.name
            #print attributes        


