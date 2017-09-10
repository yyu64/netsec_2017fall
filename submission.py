from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
import request
import qtimezone
import atimezone
import date
import final

if __name__=="__main__":

	request = RequestPacket()
	request.Request = true

	qtimezone = QTimeZonePacket()
	qtimezone.Question = "What's your time zone?"

	atimezone  = ATimeZonePacket()
	atimezone.Answer = "UTC-5"

	date = DatePacket()
	date.month = 9
	date.day = 6
	date.year = 2017
	date.hour = 22
	date.minute = 0

	final = FinalPacket()
	final.thx = b"Thanks!"

	packetBytes1 = request.__serialize__()
	packetBytes2 = qtimezone.__serialize__()
	packetBytes3 = atimezone.__serialize__()
	packetBytes4 = date.__serialize__()
	packetBytes5 = final.__serialize__()

	requestRecv = PacketType.Deserialize(packetBytes1)
	qtimezoneRecv = PacketType.Deserialize(packetBytes2)
	atimezoneRecv = PacketType.Deserialize(packetBytes3)
	dateRecv = PacketType.Deserialize(packetBytes4)
	finalRecv = PacketType.Deserialize(packetBytes5)
	if request == requestRecv:
		print("1. These two packets are the same!")
	if qtimezone == qtimezoneRecv:
		print("2. These two packets are the same!")
	if atimezone == atimezoneRecv:
		print("3. These two packets are the same!")
	if date == dateRecv:
		print("4. These two packets are the same!")
	if final == finalRecv:
		print("5. These two packets are the same!")

