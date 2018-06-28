from abc import ABCMeta, abstractmethod
class Intent(object):


	def __init__(self, name, params):
		self.InputContexts = []
		self.OutputContexts = []
		self.name = name
		self.params = []
		for param in params:
			# print param['required']
			self.params += [Parameter(param)]

	def add_inputcontext(self,context):
		self.InputContexts.append(context)
	def add_ouputcontext(self,context):
		self.OutputContexts.append(context)

class Parameter():
    def __init__(self, info):
        self.name = info['name']
        self.placeholder = info['placeholder']
        self.prompts = info['prompts']
        self.required = info['required']
        self.context = info['context']
'''
class FlightBook(Intent):

	RequiredParameters = ['from','to']

	def get_intentname(self):
		return 'FlightBook'

	def prompt(self,para):
		if(para=='from'):
			return 'What is the from'
		if(para=='to'):
			return 'What is the to'

class FlightSearch(Intent):

	RequiredParameters = ['from','to']

	def get_intentname(self):
		return 'FlightSearch'

	def prompt(self,para):
		if(para=='from'):
			return 'What is the from'
		if(para=='to'):
			return 'What is the to'


class FlightTrack(Intent):

	RequiredParameters = ['from','to']    

	def get_intentname(self):
		return 'FlightTrack'

	def prompt(self,para):
		if(para=='from'):
			return 'What is the from'
		if(para=='to'):
			return 'What is the to'
'''
