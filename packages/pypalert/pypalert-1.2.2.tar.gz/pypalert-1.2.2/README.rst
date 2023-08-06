pip install pypalert

from pypalert import pypalert

#connect to S303 
pypalert.connect(IP,port)

#disconnect with S303
pypalert.connect_exit()

#get now Unixtime
pypalert.get_Now_UnixTime()

#get Channel1 datas in this second
pypalert.get_Now_Channel1()

#get Channel2 datas in this second
pypalert.get_Now_Channel2()

#get Channel3 datas in this second
pypalert.get_Now_Channel3()

#get Channel4 datas in this second
pypalert.get_Now_Channel4()

#get SPS in this second
pypalert.get_SPS()

#get Scale in this second
pypalert.get_Scale()

#get data in this N second
pypalert.get_NsecondData(N)
