# Knihovna pro komunikaci s I2C obvodem reálného času

import smbus,time
i2c_channel = 1
bus = smbus.SMBus(i2c_channel)

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")
_hexs = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F")

def _bcd2dec(_value):
 return int(_value>>4)*10 + (_value&0xF)
def _dec2bcd(_value):
 return int((_value//10)*16 + _value%10)
def _dec2hex(_value):
 return str(_hexs[_value//16])+str(_hexs[_value%16])

class DS3231:

 def temperature(): # zkoušeno pouze na kladných teplotách
   _data = bus.read_i2c_block_data(0x68, 0x11, 2)
   _upper = _data[0]
   _lower = ((_data[1]&0xC0)>>6) * 0.25
   return (_upper+_lower)

 def offset(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x68, 0x10, 1)
   return (_data[0])
  else:
   bus.write_byte_data(0x68, 0x10, _value)
   time.sleep(0.05)

 def osc_flag(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x68, 0x0F, 1)
   return bool((_data[0]&0x80)>>7)
  elif not(_value==0):
   raise ValueError("Parameter allowed: only osc_flag(0)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x68, 0x0F, 1)
   _reg[0]=_reg[0]&0x7F # reset flag when oscilator was stopped
   bus.write_byte_data(0x68, 0x0F, _reg[0])
   time.sleep(0.05)

 def rtctime(_hour=None,_minute=None,_second=None):
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = bus.read_i2c_block_data(0x68, 0, 3)
    _time_seconds=_bcd2dec(_data[0])
    _time_minutes=_bcd2dec(_data[1])
    _time_hours=_bcd2dec(_data[2]&0x3F) # AM/PM neošetřeno
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in rtctime(hour,minute,second)")
    return()
  else:
   _data=[_dec2bcd(_second), _dec2bcd(_minute), _dec2bcd(_hour)]
   bus.write_i2c_block_data(0x68, 0, _data)
   time.sleep(0.05)
   _data = bus.read_i2c_block_data(0x68, 14, 2)
   _data[0]=_data[0]&0x7F # start oscilator
   _data[1]=_data[1]&0x7F # clear oscilator flag
   bus.write_i2c_block_data(0x68, 14, _data)   
   time.sleep(0.05)

 def rtcdate(_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(4)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = bus.read_i2c_block_data(0x68, 3, 4)
    _time_weekday=_data[0]
    if _time_weekday==0:
     _time_weekday=7
    _time_date=_bcd2dec(_data[1])
    _time_month=_bcd2dec(_data[2]&0x1F) # pouze od roku 2000
    _time_year=2000+_bcd2dec(_data[3])
    return (_time_date, _time_month, _time_year, _time_weekday)
   else:
    raise ValueError("Some parametr missing in rtcdate(day,month,year,weekday)")
    return()
  else:
   if _weekday==7:
    _weekday=0
   _data=[_weekday, _dec2bcd(_day), _dec2bcd(_month), _dec2bcd(_year-2000)]
   bus.write_i2c_block_data(0x68, 3, _data)
   time.sleep(0.05)

 def alarm_flag(_value=None): # parametr 0 clears alarm1 flag
  if _value==None:
   _data = bus.read_i2c_block_data(0x68, 0x0F, 1)
   return bool(_data[0]&0x1)
  elif not(_value==0):
   raise ValueError("Parameter allowed: only alarm_flag(0)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x68, 0x0F, 1)
   _reg[0]=_reg[0]&0xFE # reset alarm1 flag
   bus.write_byte_data(0x68, 0x0F, _reg[0])
   time.sleep(0.05)

 def alarm(_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bus.read_i2c_block_data(0x68, 8, 2)
    _a_minute=_bcd2dec(_data[0]&0x7F)
    _a_hour=_bcd2dec(_data[1]&0x3F) # AM/PM neošetřeno
    return (_a_hour,_a_minute) # actual alarm
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _buff=[0,_dec2bcd(_minute), _dec2bcd(_hour), 0x81] # nastavení na shodu hodin, minut a sekund (sekundy jsou 0)
   bus.write_i2c_block_data(0x68, 7, _buff)
   time.sleep(0.05)
   _data = bus.read_i2c_block_data(0x68, 0x0F, 1)
   _data[0] = _data[0]&0xFE
   bus.write_byte_data(0x68, 0x0F, _data[0]) # smazani flagu alarmu1
   time.sleep(0.05)

 def rtcmap():
  _data = bus.read_i2c_block_data(0x68, 0, 32) #nacte 32 bajtu od adresy 0
  _time_seconds=_bcd2dec(_data[0])
  _time_minutes=_bcd2dec(_data[1])
  _t_hours_12_24=(_data[2]&0x40)>>6
  if _t_hours_12_24 == 1:
    _time_am_pm=(_data[2]&0x20)>>5
    _time_hours=_bcd2dec(_data[2]&0x1F)
  else:
    _time_hours=_bcd2dec(_data[2])
  _time_day=_data[3]
  _time_date=_bcd2dec(_data[4])
  _time_century=(_data[5]&0x80)>>7
  _time_month=_bcd2dec(_data[5]&0x1F)
  _time_year=_bcd2dec(_data[6])
  _alarm1_a1m1=(_data[7]&0x80)>>7
  _alarm1_seconds=_bcd2dec(_data[7]&0x7F)
  _alarm1_a1m2=(_data[8]&0x80)>>7
  _alarm1_minutes=_bcd2dec(_data[8]&0x7F)
  _alarm1_a1m3=(_data[9]&0x80)>>7
  _alarm1_12_24=(_data[9]&0x40)>>6
  if _alarm1_12_24:
   _alarm1_am_pm=(_data[9]&0x20)>>5
   _alarm1_hours=_bcd2dec(_data[9]&0x1F)
  else:
   _alarm1_hours=_bcd2dec(_data[9]&0x3F)
  _alarm1_a1m4=(_data[10]&0x80)>>7
  _alarm1_dy_dt=(_data[10]&0x40)>>6
  if _alarm1_dy_dt:
   _alarm1_day=_data[10]&0xF
  else:
   _alarm1_date=_bcd2dec(_data[10]&0x3F)
  _alarm2_a2m2=(_data[11]&0x80)>>7
  _alarm2_minutes=_bcd2dec(_data[11]&0x7F)
  _alarm2_a2m3=(_data[12]&0x80)>>7
  _alarm2_12_24=(_data[12]&0x40)>>6
  if _alarm2_12_24:
   _alarm2_am_pm=(_data[12]&0x20)>>5
   _alarm2_hours=_bcd2dec(_data[12]&0x1F)
  else:
   _alarm2_hours=_bcd2dec(_data[12]&0x3F)
  _alarm2_a2m4=(_data[13]&0x80)>>7
  _alarm2_dy_dt=(_data[13]&0x40)>>6
  if _alarm2_dy_dt:
   _alarm2_day=_data[13]&0xF
  else:
   _alarm2_date=_bcd2dec(_data[13]&0x3F)
  _control_eosc=(_data[14]&0x80)>>7
  _control_bbsqw=(_data[14]&0x40)>>6
  _control_conv=(_data[14]&0x20)>>5
  _control_rs2=(_data[14]&0x10)>>4
  _control_rs1=(_data[14]&0x8)>>3
  _control_intcn=(_data[14]&0x4)>>2
  _control_a2ie=(_data[14]&0x2)>>1
  _control_a1ie=(_data[14]&0x1)
  _status_osf=(_data[15]&0x80)>>7
  _status_en32khz=(_data[15]&0x8)>>3
  _status_bsy=(_data[15]&0x4)>>2
  _status_a2f=(_data[15]&0x2)>>1
  _status_a1f=(_data[15]&0x1)
    
  print("00h (Time_Seconds) .." + str(_data[0]) + " (Seconds=" + str(_time_seconds) +  ")")
  print("01h (Time_Minutes) .." + str(_data[1]) + " (Minutes=" + str(_time_minutes) +  ")")
  if _t_hours_12_24 == 1:
   print("02h (Time_Hours) .." + str(_data[2]) + " (AM/PM=" + str(_time_am_pm) + ", Hours=" + str(_time_hours) + ")")   # platí pro 12 hodinový cyklus
  else:
   print("02h (Time_Hours) .." + str(_data[2]) + " (Hours=" + str(_time_hours) + ")")  # platí pro 24 hodinový cyklus
  print("03h (Time_Day) .." + str(_data[3]) + " (Day=" + str(_time_day) + ")")
  print("04h (Time_Date) .." + str(_data[4]) + " (Date=" + str(_time_date) +")")
  print("05h (Time_Month_Century) .." + str(_data[5]) + " (C=" + str(_time_century) + ", Month=" + str(_time_month)  + ")")
  print("06h (Time_Year) .." + str(_data[6]) + " (Year=20" + str(_time_year) + ")")
  print("07h (Alarm1_Seconds) .." + str(_data[7]) + "(A1M1=" + str(_alarm1_a1m1) + ", Seconds=" + str(_alarm1_seconds) + ")")
  print("08h (Alarm1_Minutes) .." + str(_data[8]) + "(A1M2=" + str(_alarm1_a1m2) + ", Minutes=" + str(_alarm1_minutes) + ")")
  if _alarm1_12_24:
   print("09h (Alarm1_Hours) .." + str(_data[9]) + "(A1M3=" + str(_alarm1_a1m3) + ", AM_PM=" + str(_alarm1_am_pm) + ", Hours=" + str(_alarm1_hours) + ")")
  else:
   print("09h (Alarm1_Hours) .." + str(_data[9]) + "(A1M3=" + str(_alarm1_a1m3) + ", Hours=" + str(_alarm1_hours) + ")")
  if _alarm1_dy_dt:
   print("0Ah (Alarm1_Day) .." + str(_data[10]) + " (A1M4" + str(_alarm1_a1m4) + ", Day=" + str(_alarm1_day) + ")")
  else: 
   print("0Ah (Alarm1_Date) .." + str(_data[10]) + " (A1M4" + str(_alarm1_a1m4) + ", Date=" + str(_alarm1_date) + ")")
  print("0Bh (Alarm2_Minutes) .." + str(_data[11]) + "(A2M2=" + str(_alarm2_a2m2) + ", Minutes=" + str(_alarm2_minutes) + ")")
  if _alarm1_12_24:
   print("0Ch (Alarm2_Hours) .." + str(_data[12]) + "(A2M3=" + str(_alarm2_a2m3) + ", AM_PM=" + str(_alarm2_am_pm) + ", Hours=" + str(_alarm2_hours) + ")")
  else:
   print("0Ch (Alarm2_Hours) .." + str(_data[12]) + "(A2M3=" + str(_alarm2_a2m3) + ", Hours=" + str(_alarm2_hours) + ")")
  if _alarm1_dy_dt:
   print("0Dh (Alarm2_Day) .." + str(_data[13]) + " (A2M4" + str(_alarm2_a2m4) + ", Day=" + str(_alarm2_day) + ")")
  else: 
   print("0Dh (Alarm2_Date) .." + str(_data[13]) + " (A2M4" + str(_alarm2_a2m4) + ", Date=" + str(_alarm2_date) + ")")
  print("0Eh (Control) .." + str(_data[14]) + " (EOSC=" + str(_control_eosc) + ", BBSQW=" + str(_control_bbsqw) + ", CONV=" + str(_control_conv) + ", RS2=" + str(_control_rs2) + ", RS1=" + str(_control_rs1) + ", INTCN=" + str(_control_intcn) + ", A2IE=" + str(_control_a2ie) + ", A1IE=" + str(_control_a1ie) + ")")
  print("0Fh (Control_Status) .." + str(_data[15]) + " (OSF=" + str(_status_osf) + ", EN32kHz=" + str(_status_en32khz) + ", BSY=" + str(_status_bsy) + ", A2F=" + str(_status_a2f) + ", A1F=" + str(_status_a1f) + ")")
  print("10h (Aging_Offset) .." + str(_data[16]))
  print("11h (MSB_of_Temp) .." + str(_data[17]))
  print("12h (LSB_of_Temp) .." + str(_data[18]))
