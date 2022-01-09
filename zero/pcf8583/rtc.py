# Knihovna pro komunikaci s I2C obvodem reálného času

import smbus,time
i2c_channel = 1
bus = smbus.SMBus(i2c_channel)
addr = 0x50 # obvod může mít adresu 0x50 nebo 0x51

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")
_hexs = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F")

def _bcd2dec(_value):
 return int(_value>>4)*10 + (_value&0xF)
def _dec2bcd(_value):
 return int((_value//10)*16 + _value%10)
def _dec2hex(_value):
 return str(_hexs[_value//16])+str(_hexs[_value%16])

class PCF8583:

 def oscilator(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(addr, 0, 1)
   return not bool((_data[0]&0x80)>>7)
  elif not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only oscilator(0) or oscilator(1)")
   return()
  else:
   _reg = bus.read_i2c_block_data(addr, 0, 1)
   if _value==0:
    _reg[0]=_reg[0]|0x80 # stop oscilator
   else:
    _reg[0]=_reg[0]&0x7F # start oscilator
   bus.write_byte_data(addr, 0, _reg[0])
   time.sleep(0.05)

 def rtctime(_hour=None,_minute=None,_second=None):
  _data = bytearray(4)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = bus.read_i2c_block_data(addr, 2, 3)
    _time_seconds=_bcd2dec(_data[0])
    _time_minutes=_bcd2dec(_data[1])
    _time_hours=_bcd2dec(_data[2]) # AM/PM neošetřeno
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in rtctime(hour,minute,second)")
    return()
  else:
   _data=[0, _dec2bcd(_second), _dec2bcd(_minute), _dec2bcd(_hour)]
   bus.write_i2c_block_data(addr, 1, _data)
   time.sleep(0.05)
   _data = bus.read_i2c_block_data(addr, 0, 1)
   _data[0] = _data[0]&0x7F
   bus.write_byte_data(addr, 0, _data[0])
   time.sleep(0.05)


 def rtcdate(_day=None,_month=None,_weekday=None): # rok je nepoužitelný
  _data = bytearray(3)
  if _day==None or _month==None or _weekday==None:
   if _day==None and _month==None and _weekday==None:
    _data = bus.read_i2c_block_data(addr, 5, 2)
    _time_days=_bcd2dec(_data[0]&0x3F)
    _time_months=_bcd2dec(_data[1]&0x1F)
    _time_weekdays=(_data[1]&0xE0)>>5
    if _time_weekdays==0:
     _time_weekdays=7
    return (_time_days, _time_months, _time_weekdays)
   else:
    raise ValueError("Some parametr missing in rtcdate(day,month,weekday)")
    return()
  else:
   _data=[_dec2bcd(_day), (_weekday<<5)+_dec2bcd(_month)]
   bus.write_i2c_block_data(addr, 5, _data)
   time.sleep(0.05)

 def alarm_flag(_flag=None): # parametr 0 clears flag
  _data = bus.read_i2c_block_data(addr, 0, 1) # read control_status_2
  if _flag==None:
   return bool((_data[0]&0x2)>>1) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data[0] = _data[0]&0xFD # alarm flag is cleared
   bus.write_byte_data(addr, 0, _data[0])
   time.sleep(0.05)

 def alarm(_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bus.read_i2c_block_data(addr, 0x0B, 2)
    _a_minute=_bcd2dec(_data[0])
    _a_hour=_bcd2dec(_data[1]) # AM/PM neošetřeno
    return (_a_hour,_a_minute) # actual alarm
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _buff=[0x10, 0, 0, _dec2bcd(_minute), _dec2bcd(_hour), 0, 0] # nastavení pouze na shodu hodin a minut
   bus.write_i2c_block_data(addr, 8, _buff)
   time.sleep(0.05)
   _data = bus.read_i2c_block_data(addr, 0, 1)
   _data[0] = _data[0]|0x4
   bus.write_byte_data(addr, 0, _data[0])
   time.sleep(0.05)

 def ram_write(_ram=None,_value=None):
  if _ram==None and _value==None:
   raise ValueError("Address parametr missing in ram_write(address,data)")
   return()
  bus.write_byte_data(addr, _ram, _value)
  time.sleep(0.05)
  return()

 def ram_read(_ram=None,_bytes=None):
  if _ram==None and _bytes==None:
   raise ValueError("Address parametr missing in ram_read(address,bytes)")
   return()
  if _bytes==None:
   _bytes=1
  _data = bus.read_i2c_block_data(addr, _ram, _bytes)
  return (_data)

 def rtcmap():
  _data = bytearray(16)
  _data = bus.read_i2c_block_data(addr, 0, 16) #nacte 16 bajtu od adresy 0
  _stop_counting_flag=(_data[0]&0x80)>>7
  _hold_last_count_flag=(_data[0]&0x40)>>6
  _function_mode=(_data[0]&0x30)>>4
  _mask_flag=(_data[0]&0x8)>>3
  _alarm_enable_bit=(_data[0]&0x4)>>2
  _alarm_flag=(_data[0]&0x2)>>1
  _timer_flag=_data[0]&0x1
  _time_hundredth_of_a_second=_bcd2dec(_data[1])
  _time_seconds=_bcd2dec(_data[2])
  _time_minutes=_bcd2dec(_data[3])
  _format_hours=(_data[4]&0x80)>>7
  _am_pm_flag=(_data[4]&0x40)>>6
  _time_hours=_bcd2dec(_data[4]&0x3f)
  _time_year=2000+((_data[5]&0xc0)>>6)
  _time_days=_bcd2dec(_data[5]&0x3f)
  _time_weekday=(_data[6]&0xe0)>>5
  _time_months=_bcd2dec(_data[6]&0x1f)
  _alarm_interrupt_enable=(_data[8]&0x80)>>7
  _timer_alarm_enable=(_data[8]&0x40)>>6
  _clock_alarm_function=(_data[8]&0x30)>>4
  _timer_interrupt_enable=(_data[8]&0x8)>>3
  _timer_function=_data[8]&0x7
  _alarm_hundredth_of_a_second=_bcd2dec(_data[9])
  _alarm_seconds=_bcd2dec(_data[10])
  _alarm_minutes=_bcd2dec(_data[11])
  _alarm_hours=_bcd2dec(_data[12])
  _alarm_date=_bcd2dec(_data[13])
  _weekday_6_enable=(_data[14]&0x40)>>6
  _weekday_5_enable=(_data[14]&0x20)>>5
  _weekday_4_enable=(_data[14]&0x10)>>4
  _weekday_3_enable=(_data[14]&0x8)>>3
  _weekday_2_enable=(_data[14]&0x4)>>2
  _weekday_1_enable=(_data[14]&0x2)>>1
  _weekday_0_enable=_data[14]&0x1
  
  print("00h (control/status) .." + str(_data[0]) + " (stop counting flag=" +  str(_stop_counting_flag) + ", hold last count flag=" + str(_hold_last_count_flag) + ", function mode=" + str(_function_mode) + ", mask flag=" + str(_mask_flag) + ", alarm enable bit=" + str(_alarm_enable_bit) + ", alarm flag=" + str(_alarm_flag) + ", timer flag=" + str(_timer_flag)  + ")")
  # dale pouze pro rezim clock modes
  print("01h (hundredth of a second) .." + str(_data[1]) + " (" + str(_time_hundredth_of_a_second) + ")")
  print("02h (seconds) .." + str(_data[2]) + " (second=" + str(_time_seconds) + ")")
  print("03h (minutes) .." + str(_data[3]) + " (minute=" + str(_time_minutes) + ")")
  print("04h (hours) .." + str(_data[4]) + " (format=" + str(_format_hours) + ", am/pm flag=" + str(_am_pm_flag) + ", hour=" + str(_time_hours) + ")")
  print("05h (year/date) .." + str(_data[5]) + " (year=" + str(_time_year) + ", day=" + str(_time_days) + ")")
  print("06h (weekday/month) .." + str(_data[6]) + " (weekday=" + str(_time_weekday) + ", month=" + str(_time_months) + ")")
  print("07h (timer) .." + str(_data[7]))
  print("08h (alarm control) .." + str(_data[8]) + " (alarm interrupt enable=" + str(_alarm_interrupt_enable) + ", timer alarm enable=" + str(_timer_alarm_enable) + ", clock alarm function=" + str(_clock_alarm_function) + ", timer interrupt enable=" + str(_timer_interrupt_enable) + ", timer function=" + str(_timer_function) + ")")
  print("09h (hundredth of a second) .." + str(_data[9]) + " (" + str(_alarm_hundredth_of_a_second) + ")")
  print("0ah (alarm seconds) .." + str(_data[10]) + " (" + str(_alarm_seconds) + ")")
  print("0bh (alarm minutes) .." + str(_data[11]) + " (" + str(_alarm_minutes) + ")")
  print("0ch (alarm hours) .." + str(_data[12]) + " (" + str(_alarm_hours) + ")")
  print("0dh (alarm date) .." + str(_data[13]) + " (" + str(_alarm_date) + ")")
  print("0eh (alarm weekdays) .." + str(_data[14]) + " (weekday6 enable=" + str(_weekday_6_enable) + ", weekday5 enable=" + str(_weekday_5_enable) + ", weekday4 enable=" + str(_weekday_4_enable) + ", weekday3 enable=" + str(_weekday_3_enable) + ", weekday2 enable=" + str(_weekday_2_enable) + ", weekday1 enable=" + str(_weekday_1_enable) + ", weekday0 enable=" + str(_weekday_0_enable) + ")")
  print("0fh (alarm timer) .." + str(_data[15]))
  print()
  
  #_sram = bytearray(240) # pole freesram se musi cist zvlast
  _sram1 = bus.read_i2c_block_data(addr, 16, 32) # najednou nelze načíst víc, než 32 bajtů
  _sram2 = bus.read_i2c_block_data(addr, 48, 32)
  _sram3 = bus.read_i2c_block_data(addr, 80, 32)
  _sram4 = bus.read_i2c_block_data(addr, 112, 32)
  _sram5 = bus.read_i2c_block_data(addr, 144, 32)
  _sram6 = bus.read_i2c_block_data(addr, 176, 32)
  _sram7 = bus.read_i2c_block_data(addr, 208, 32)
  _sram8 = bus.read_i2c_block_data(addr, 240, 16)
  _sram=_sram1+_sram2+_sram3+_sram4+_sram5+_sram6+_sram7+_sram8
  
  #240 bajtů uživatelsky přístupné paměti SRAM je v adresním rozsahu 0x10-0xFF.
  print("free ram for user:")
  print()
  print("adr     0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F")
  for _radky in range(15):
   _radek=str(_dec2hex(16+_radky*16))+"h .. "
   for _sloupce in range(16):
    _radek=_radek+str(_dec2hex(_sram[(_radky*16)+_sloupce]))+"h  "
   print(_radek)
