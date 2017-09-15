import playground
import sys, time, os, logging, asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT32,UINT32, STRING, BUFFER, BOOL
from playground.network.common import PlaygroundAddress
class EchoPacket(PacketType):
    DEFINITION_IDENTIFIER = "test.EchoPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
              ("original", BOOL),
              ("message", STRING)
             ]


class RequestPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x1.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		#("OrginalC",BOOL),
		("Request", STRING)
		]
class QTimeZonePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x2.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		#("OrginalS",BOOL),
		("Question", STRING)
	]
class ATimeZonePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x3.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		#("OrginalC",BOOL),
		("Answer", STRING)
	]
class DatePacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x4.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		#("OrginalS",BOOL),
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
		#("OrginalC",BOOL),
		("thx", BUFFER)
	]
class helloPacket(PacketType):
	DEFINITION_IDENTIFIER = "lab2b.student_x6.MyPacket"
	DEFINITION_VERSION = "1.0"
	FIELDS = [
		("")
	]
class MyProtocolSever(asyncio.Protocol):   
	def __init__(self):
		self.transport = None 
		self.recvnum = 0
		self.deserializer = PacketType.Deserializer()
 
	def connection_made(self, transport):
		print('Connection made')
		self.transport = transport
	
	def data_received(self, data): 
		self.deserializer.update(data)
		self.recvnum = self.recvnum + 1
		print('Sever Received Packet')
		print(self.recvnum)
		for pkt in self.deserializer.nextPackets():
			#print(pkt.Request)
			#if not pkt.OriginalS:
			if(isinstance(pkt,RequestPacket)):
				print('Packet type:RequestPacket')
				qtimezone=QTimeZonePacket()
				qtimezone.Question = "What's your time zone?"
				qtimezone.OriginalS = True
				packetBytes2 = qtimezone.__serialize__()
				self.transport.write(packetBytes2)
			elif(isinstance(pkt,ATimeZonePacket)):
				print('Packet type:ATimeZonePacket')
				date=DatePacket()
				date.month = 9
				date.day = 6
				date.year = 2017
				date.hour = 22
				date.minute = 0
				date.OriginalS = True
				packetBytes4 = date.__serialize__()
				self.transport.write(packetBytes4)
			elif(isinstance(pkt,FinalPacket)):
				print('Packet type:FinalPacket')
				print('Mission Complete!Close the client socket')
				self.transport.close()
			else:
				print('Other Packets! Drop it!')

	def connection_lost(self,exc):
		self.transport = None


class MyProtocolClient(asyncio.Protocol):
	def __init__(self):
		self.recvnum = 0
		self.deserializer = PacketType.Deserializer()
	
	def connection_made(self, transport):
		print('Connection made')
		self.transport = transport

	def data_received(self, data):
		self.deserializer.update(data)
		self.recvnum = self.recvnum + 1
		#print('Client Received Packet!')
		#print(self.recvnum)
		for pkt in self.deserializer.nextPackets():
			if(isinstance(pkt,QTimeZonePacket)):
				atimezone=ATimeZonePacket()
				atimezone.Answer = "UTC-5"
				packetBytes3 = atimezone.__serialize__()
				self.transport.write(packetBytes3)
			elif(isinstance(pkt,DatePacket)):
				#print("Final Packet")
				final=FinalPacket()
				final.thx = b"Thanks!"
				packetBytes5 = final.__serialize__()	
				self.transport.write(packetBytes5)
				self.transport.close()
	def connection_lost(self,exc):
		self.transport = None
		print('Connection Complete!')

class RequestConnection:
	def __init__(self,transp):
		self.transp = transp
		self.sendFirstPacket()

	def sendFirstPacket(self):
		request=RequestPacket()
		request.Request = "true"
		packetBytes1 = request.__serialize__()
		self.transp.write(packetBytes1)
				

if __name__=="__main__":
	mode = sys.argv[1]
	loop = asyncio.get_event_loop()
	loop.set_debug(enabled=True)
	if mode.lower() == "server":
       		coro = playground.getConnector().create_playground_server(lambda: MyProtocolSever(), 101)
        	server = loop.run_until_complete(coro)
        	print("My Server Started at {}".format(server.sockets[0].gethostname()))
        	loop.run_forever()
        	loop.close()
        
        
	else:
		remoteAddress = mode
		#control = MyControl()
		coro = playground.getConnector().create_playground_connection(MyProtocolClient, remoteAddress, 101)
		transport, protocol = loop.run_until_complete(coro)
		RequestConnection(transport)
		#print("Client Connected. Starting UI t:{}. p:{}".format(transport, protocol))
		#loop.add_reader(sys.stdin, control.stdinAlert)
		#control.connect(protocol)
		#control.Alert()
		#loop.run_forever()
		loop.close()
