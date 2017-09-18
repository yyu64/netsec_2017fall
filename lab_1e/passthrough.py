import playground
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
class PassThrough1(StackingProtocol):
	def __init__(self):
		self.transport = None
	def connection_made(self,transport):
		print('passthrough1')
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)
	def data_received(self,data):
		#print(data)
		print('passthrough11')
		self.higherProtocol().data_received(data)
	def connection_lost(self,exc):
		self.higherProtocol().connection_lost(exc)
		self.transport = None

class PassThrough2(StackingProtocol):	
	def __init__(self):
		self.transport = None
	def connection_made(self,transport):
		print('passthrough2')
		self.transport = transport
		higherTransport = StackingTransport(self.transport)
		self.higherProtocol().connection_made(higherTransport)
	def data_received(self,data):
		#print(data)
		print('passthrough22')
		self.higherProtocol().data_received(data)
	def connection_lost(self,exc):
		self.higherProtocol().connection_lost(exc)
		self.transport = None

f = StackingProtocolFactory(lambda:PassThrough1(), lambda:PassThrough2())
ptConnector = playground.Connector(protocolStack = f)
playground.setConnector("passthrough", ptConnector)

