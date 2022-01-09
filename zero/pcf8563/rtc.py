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

class PCF8563:

 def oscilator(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x51, 0, 1)
   return not bool((_data[0]&0x20)>>5)
  elif not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only oscilator(0) or oscilator(1)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x51, 0, 1)
   if _value==0:
    _reg[0]=_reg[0]|0x20 # stop oscilator
   else:
    _reg[0]=_reg[0]&0xDF # start oscilator
   bus.write_byte_data(0x51, 0, _reg[0])
   time.sleep(0.05)

 def rtctime(_hour=None,_minute=None,_second=None):
  _data = bytearray(3)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = bus.read_i2c_block_data(0x51, 2, 3)
    _time_seconds=_bcd2dec(_data[0]&0x7F)
    _time_minutes=_bcd2dec(_data[1]&0x7F)
    _time_hours=_bcd2dec(_data[2]&0x3F) # AM/PM neošetřeno
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in rtctime(hour,minute,second)")
    return()
  else:
   _data=[_dec2bcd(_second), _dec2bcd(_minute), _dec2bcd(_hour)]
   bus.write_i2c_block_data(0x51, 2, _data)
   time.sleep(0.05)

 def rtcdate(_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(4)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = bus.read_i2c_block_data(0x51, 5, 4)
    _time_days=_bcd2dec(_data[0]&0x3F)
    _time_weekdays=_bcd2dec(_data[1]&0x7)
    _time_months=_bcd2dec(_data[2]&0x1F)
    _time_years=2000+_bcd2dec(_data[3])
    if _time_weekdays==0:
     _time_weekdays=7
    return (_time_days, _time_months, _time_years, _time_weekdays)
   else:
    raise ValueError("Some parametr missing in rtcdate(day,month,year,weekday)")
    return()
  else:
   if _weekday==7:
    _weekday=0
   _data=[_dec2bcd(_day), _dec2bcd(_weekday), _dec2bcd(_month), _dec2bcd(_year-2000)]
   bus.write_i2c_block_data(0x51, 5, _data)
   time.sleep(0.05)

 def alarm_flag(_flag=None): # parametr 0 clears flag
  _data = bus.read_i2c_block_data(0x51, 1, 1) # read control_status_2
  if _flag==None:
   return bool((_data[0]&0x8)>>3) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data[0] = _data[0]&0xF7 # alarm flag is cleared
   bus.write_byte_data(0x51, 1, _data[0])
   time.sleep(0.05)

 def alarm(_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bus.read_i2c_block_data(0x51, 9, 2)
    _a_minute=_bcd2dec(_data[0]&0x7F)
    _a_hour=_bcd2dec(_data[1]&0x3F) # AM/PM neošetřeno
    return (_a_hour,_a_minute) # actual alarm
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _buff=[_dec2bcd(_minute), _dec2bcd(_hour), 0x81, 0x80] # nastavení pouze na shodu hodin a minut
   bus.write_i2c_block_data(0x51, 9, _buff)
   time.sleep(0.05)
   _data = bus.read_i2c_block_data(0x51, 1, 1)
   _data[0] = _data[0]&0xF7 # reset alarm flag
   bus.write_byte_data(0x51, 1, _data[0])
   time.sleep(0.05)

 def rtcmap():
  _data = bytearray(16)
  _data = bus.read_i2c_block_data(0x51, 0, 16) #nacte 16 bajtu od adresy 0
  _control_status_1_test1=(_data[0]&0x80)>>7
  _control_status_1_stop=(_data[0]&0x20)>>5
  _control_status_1_testc=(_data[0]&0x8)>>3
  _control_status_2_ti_tp=(_data[1]&0x10)>>4
  _control_status_2_af=(_data[1]&0x8)>>4
  _control_status_2_tf=(_data[1]&0x4)>>4
  _control_status_2_aie=(_data[1]&0x2)>>4
  _control_status_2_tie=(_data[1]&0x1)
  _t_seconds_vl=(_data[2]&0x80)>>7
  _time_seconds=_bcd2dec(_data[2]&0x7f)
  _time_minutes=_bcd2dec(_data[3]&0x7f)
  _time_hours=_bcd2dec(_data[4]&0x3f)
  _time_days=_bcd2dec(_data[5]&0x3f)
  _time_weekdays=_bcd2dec(_data[6]&0x7)
  _t_century=(_data[7]&0x80)>>7
  _time_months=_bcd2dec(_data[7]&0x1F)
  _time_years=_bcd2dec(_data[8])
  _a_minute_ae=(_data[9]&0x80)>>7
  _alarm_minutes=_bcd2dec(_data[9]&0x7F)
  _a_hour_ae=(_data[10]&0x80)>>7
  _alarm_hours=_bcd2dec(_data[10]&0x3F)
  _a_day_ae=(_data[11]&0x80)>>7
  _alarm_days=_bcd2dec(_data[11]&0x3F)
  _a_weekday_ae=(_data[12]&0x80)>>7
  _alarm_weekday=_bcd2dec(_data[12]&0x7)
  _a_clkout_control_fe=(_data[13]&0x80)>>7
  _a_clkout_control_fd1=(_data[13]&0x2)>>1
  _a_clkout_control_fd0=_data[13]&0x1
  _timer_control_te=(_data[14]&0x80)>>7
  _timer_control_td1=(_data[14]&0x2)>>1
  _timer_control_td0=_data[14]&0x1

  print("00h (control_status_1) .." + str(_data[0]) + " (test1=" + str(_control_status_1_test1) + ", stop=" + str(_control_status_1_stop) + ", testc=" + str(_control_status_1_testc) + ")")
  print("01h (control_status_2) .." + str(_data[1]) + " (ti_tp=" + str(_control_status_2_ti_tp) + ", af=" + str(_control_status_2_af) + ", tf=" + str(_control_status_2_tf) + ", aie=" + str(_control_status_2_aie) + ", tie=" + str(_control_status_2_tie) + ")")
  print("02h (vl_seconds)       .." + str(_data[2]) + " (vl=" + str(_t_seconds_vl) + ", seconds=" + str(_time_seconds) + ")")
  print("03h (minutes)          .." + str(_data[3]) + " (minutes=" + str(_time_minutes) + ")")
  print("04h (hours)            .." + str(_data[4]) + " (hours=" + str(_time_hours) + ")")
  print("05h (days)             .." + str(_data[5]) + " (days=" + str(_time_days) + ")")
  print("06h (weekdays)         .." + str(_data[6]) + " (weekdays=" + str(_time_weekdays) + ")")
  print("07h (century_months)   .." + str(_data[7]) + " (c=" + str(_t_century) + ", months=" + str(_time_months) + ")")
  print("08h (years)            .." + str(_data[8]) + " (years=" + str(2000+_time_years) + ")")
  print("09h (minute_alarm)     .." + str(_data[9]) + " (ae=" + str(_a_minute_ae) + ", minute=" + str(_alarm_minutes) + ")")
  print("0ah (hour_alarm)       .." + str(_data[10]) + " (ae=" + str(_a_hour_ae) + ", hour=" + str(_alarm_hours) + ")")
  print("0bh (day_alarm)        .." + str(_data[11]) + " (ae=" + str(_a_day_ae) + ", day=" + str(_alarm_days) + ")")
  print("0ch (weekday_alarm)    .." + str(_data[12]) + " (ae=" + str(_a_weekday_ae) + ", weekday=" + str(_alarm_weekday) + ")")
  print("0dh (clkout_control)   .." + str(_data[13]) + " (fe=" + str(_a_clkout_control_fe) +  ", fd1=" + str(_a_clkout_control_fd1) + ", fd0=" + str(_a_clkout_control_fd0) + ")")
  print("0eh (timer_control)    .." + str(_data[14]) + " (te=" + str(_timer_control_te) +  ", td1=" + str(_timer_control_td1) + ", td0=" + str(_timer_control_td0) + ")")
  print("0fh (timer)            .." + str(_data[15]))
