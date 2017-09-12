from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT32,UINT32, STRING, BUFFER, BOOL
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
	
def basicUnitTest():
	request=RequestPacket()	
	request.Request = "true"
	#print("The orginal request data is : {}".format(request.Request))
	packetBytes1 = request.__serialize__()
	requestRecv = PacketType.Deserialize(packetBytes1)
	print(requestRecv.Request)
	if request == requestRecv:
		print("The request packet is the same!")
	else:
		print("Error!")

	qtimezone=QTimeZonePacket()
	qtimezone.Question = "What's your time zone?"
	packetBytes2 = qtimezone.__serialize__()
	qtimezoneRecv = PacketType.Deserialize(packetBytes2)
	if qtimezone == qtimezoneRecv:
		print("The qtimezone packet is the same!")
	else:
		print("Error!")

	atimezone=ATimeZonePacket()
	atimezone.Answer = "UTC-5"
	packetBytes3 = atimezone.__serialize__()
	atimezoneRecv = PacketType.Deserialize(packetBytes3)
	if atimezone == atimezoneRecv:
		print("The atimezone packet is the same!")
	else:
		print("Error!")

	date=DatePacket()
	date.month = 9
	date.day = 6
	date.year = 2017
	date.hour = 22
	date.minute = 0
	packetBytes4 = date.__serialize__()
	dateRecv = PacketType.Deserialize(packetBytes4)
	if date == dateRecv:
		print("The date packet is the same!")
	else:
		print("Error!")

	final=FinalPacket()
	final.thx = b"Thanks!"
	packetBytes5 = final.__serialize__()
	finalRecv = PacketType.Deserialize(packetBytes5)
	if final == finalRecv:
		print("The final packet is the same!")
	else:
		print("Error!")
if __name__=="__main__":
	basicUnitTest()
