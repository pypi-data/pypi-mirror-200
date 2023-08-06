pip install pypalert

from pypalert import pypalert

#connect to S303 
a = ModbusData(IP,port)


#get now get_IP
a.get_IP()

#get now port
a.get_Port()

#get now Unixtime
a.get_Now_UnixTime()

#get Channel1 datas in this second
a.get_Now_Channel1()

#get Channel2 datas in this second
a.get_Now_Channel2()

#get Channel3 datas in this second
a.get_Now_Channel3()

#get Channel4 datas in this second
a.get_Now_Channel4()

#get SPS in this second
a.get_SPS()

#get Scale in this second
a.get_Scale()

#get data in this N second
a.get_NsecondData(N)
