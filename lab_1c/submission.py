import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT32,UINT32, STRING, BUFFER, BOOL
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.testing import MockTransportToStorageStream
from playground.network.testing import MockTransportToProtocol
class RequestPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x1.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("Request", STRING)
		]
class QTimeZonePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x2.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("Question", STRING)
	]
class ATimeZonePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x3.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("Answer", STRING)
	]
class DatePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x4.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("month", INT32),
		("day", INT32),
		("year", INT32),
		("hour", INT32),
		("minute", INT32)
	]
class FinalPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x5.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("thx", BUFFER)
	]

class MyProtocolSever(asyncio.Protocol):   
	def __init__(self):
		self.transport = None 
		self.recvnum = 0
		self.deserializer = PacketType.Deserializer()
 
	def connection_made(self, transport):
		self.transport = transport
	
	def dataReceived(self, data): 
		self.deserializer.update(data)
		self.recvnum = self.recvnum + 1
		print('Sever Received {} Packet'.format(self.recvnum))
		#print(self.recvnum)
		for pkt in self.deserializer.nextPackets():
			if(isinstance(pkt,RequestPacket)):
				print('Data received: {!r}'.format(pkt.Request))
				qtimezone=QTimeZonePacket()
				qtimezone.Question = "What's your time zone?"
				packetBytes2 = qtimezone.__serialize__()
				self.transport.write(packetBytes2)
			elif(isinstance(pkt,ATimeZonePacket)):
				print('Data received: {!r}'.format(pkt.Answer))
				date=DatePacket()
				date.month = 9
				date.day = 6
				date.year = 2017
				date.hour = 22
				date.minute = 0
				packetBytes4 = date.__serialize__()
				self.transport.write(packetBytes4)
			elif(isinstance(pkt,FinalPacket)):
				print('Data received: {!r}'.format(pkt.thx))
				print('Mission Complete!Close the client socket')
				#self.connection_lost()
				#self.transport.close()

	def connection_lost(self,exc):
		#self.transport.close()   
		self.transport = None
class MyProtocolClient(asyncio.Protocol):
	def __init__(self):
		self.recvnum = 0
		self.deserializer = PacketType.Deserializer()
	
	def connection_made(self, transport):
		self.transport = transport

	def sendFirstPacket(self):
		request=RequestPacket()
		request.Request = "true"
		packetBytes1 = request.__serialize__()
		self.transport.write(packetBytes1)

	def dataReceived(self, data):
		self.deserializer.update(data)
		self.recvnum = self.recvnum + 1
		print('CLient Received {} Packet!'.format(self.recvnum))
		#print(self.recvnum)
		for pkt in self.deserializer.nextPackets():
			if(isinstance(pkt,QTimeZonePacket)):
				print('Data received: {!r}'.format(pkt.Question))
				atimezone=ATimeZonePacket()
				atimezone.Answer = "UTC-5"
				packetBytes3 = atimezone.__serialize__()
				self.transport.write(packetBytes3)
				#print('Send the time zone to the sever!')
			elif(isinstance(pkt,DatePacket)):
				print('Data received: {}/{}/{} {}:{}'.format(pkt.month,pkt.day,pkt.year,pkt.hour,pkt.minute))
				final=FinalPacket()
				final.thx = b"Thanks!"
				packetBytes5 = final.__serialize__()	
				self.transport.write(packetBytes5)
				print('Mission is completed! Connection closed')
				#self.transport.close()
		
			
	def connection_lost(self, exc):		
		self.transport = None

def basicUnitTest2():
	asyncio.set_event_loop(TestLoopEx())
	client = MyProtocolClient()
	server = MyProtocolSever()
	transportToServer = MockTransportToProtocol(server)
	transportToClient = MockTransportToProtocol(client)
	server.connection_made(transportToClient)
	client.connection_made(transportToServer)
	client.sendFirstPacket()

if __name__=="__main__":
	basicUnitTest2()
