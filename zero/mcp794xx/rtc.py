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

class MCP794xx:

 def calibration(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x6F, 8, 1)
   return (_data[0])
  else:
   bus.write_byte_data(0x6F, 8, _value)
   time.sleep(0.05)

 def oscilator(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x6F, 3, 1)
   return bool((_data[0]&0x20)>>5)
  elif not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only oscilator(0) or oscilator(1)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x6F, 3, 1)
   if _value==1:
    _reg[0]=_reg[0]|0x80 # start oscilator
   else:
    _reg[0]=_reg[0]&0x7F # stop oscilator
   bus.write_byte_data(0x6F, 0, _reg[0])
   time.sleep(0.05)

 def rtctime(_hour=None,_minute=None,_second=None):
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = bus.read_i2c_block_data(0x6F, 0, 3)
    _time_seconds=_bcd2dec(_data[0]&0x7F)
    _time_minutes=_bcd2dec(_data[1]&0x7F)
    _time_hours=_bcd2dec(_data[2]&0x3F) # AM/PM neošetřeno
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in rtctime(hour,minute,second)")
    return()
  else:
   _data=[_dec2bcd(_second)|0x80, _dec2bcd(_minute), _dec2bcd(_hour)] # start oscilator |0x80
   bus.write_i2c_block_data(0x6F, 0, _data)
   time.sleep(0.05)

 def rtcdate(_day=None,_month=None,_year=None,_weekday=None):
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = bus.read_i2c_block_data(0x6F, 3, 4)
    _time_weekday=_data[0]&0x7
    if _time_weekday==0:
     _time_weekday=7
    _time_date=_bcd2dec(_data[1]&0x3F)
    _time_month=_bcd2dec(_data[2]&0x1F)
    _time_year=2000+_bcd2dec(_data[3])
    return (_time_date, _time_month, _time_year, _time_weekday)
   else:
    raise ValueError("Some parametr missing in rtcdate(day,month,year,weekday")
    return()
  else:
   _data = bytearray(1) # deklarace musi byt   
   _data[0] = (bus.read_i2c_block_data(0x6F, 3, 1)[0])&0xF8
   if _weekday==7:
    _weekday=0
   _data=[_data[0]+_weekday, _dec2bcd(_day), _dec2bcd(_month), _dec2bcd(_year-2000)]
   bus.write_i2c_block_data(0x6F, 3, _data)
   time.sleep(0.05)

 def timestamp_down():
  _data = bus.read_i2c_block_data(0x6F, 0x18, 4)
  _ts_minutes=_bcd2dec(_data[0]&0x7F)
  _ts_hours=_bcd2dec(_data[1]&0x3F) # AM/PM neošetřeno
  _ts_date=_bcd2dec(_data[2]&0x3F)
  _ts_month=_bcd2dec(_data[3]&0x1F)
  _ts_weekday=(_data[3]&0xE0)>>5
  if _ts_weekday==0:
   _ts_weekday=7
  return (_ts_minutes, _ts_hours, _ts_date, _ts_month, _ts_weekday)

 def timestamp_up():
  _data = bus.read_i2c_block_data(0x6F, 0x1C, 4)
  _ts_minutes=_bcd2dec(_data[0]&0x7F)
  _ts_hours=_bcd2dec(_data[1]&0x3F) # AM/PM neošetřeno
  _ts_date=_bcd2dec(_data[2]&0x3F)
  _ts_month=_bcd2dec(_data[3]&0x1F)
  _ts_weekday=(_data[3]&0xE0)>>5
  if _ts_weekday==0:
   _ts_weekday=7
  return (_ts_minutes, _ts_hours, _ts_date, _ts_month, _ts_weekday)

 def id_write(_value=None): #zapisuje najednou všech 8 bajtu do ID oblasti s adresou 0x57
  if _value==None:
   raise ValueError("Parametr missing in id_write(data)")
   return()
  if not(len(_value)==8):
   raise ValueError("Parameter does not contain 8 bytes in id_wite(data)")
   return()
  _buff=0x55
  bus.write_byte_data(0x6F, 0x09, _buff)
  time.sleep(0.05)
  _buff=0xAA
  bus.write_byte_data(0x6F, 0x09, _buff)
  time.sleep(0.05)
  bus.write_i2c_block_data(0x57, 0xF0, _value)
  time.sleep(0.05)
  return()

 def id_read(): # čte ID obvodu
  _data= bus.read_i2c_block_data(0x57, 0xF0, 8)
  return(_data)

 def eeprom_write(_address=None,_value=None):  # zapisuje do oblasti EEPROM s adresou 0x57
  if _address==None or _value==None:
   raise ValueError("Some parametr missing in eeprom_write(address,data)")
   return()
  bus.write_byte_data(0x57, _address, _value)
  time.sleep(0.05)
  return()

 def eeprom_read(_address=None,_bytes=None): # čte z oblasti EEPROM s adresou 0x57
  if _address==None and _bytes==None:
   raise ValueError("Address parametr missing in eeprom_read(address,bytes)")
   return()
  if _bytes==None:
   _bytes=1 
  _data = bus.read_i2c_block_data(0x57, _address, _bytes)
  return(_data)

 def ram_write(_ram=None,_value=None):
  if _ram==None and _value==None:
   raise ValueError("Address parametr missing in ram_write(address,data)")
   return()
  bus.write_byte_data(0x6F, _ram, _value)
  time.sleep(0.05)
  return()

 def ram_read(_ram=None,_bytes=None):
  if _ram==None and _bytes==None:
   raise ValueError("Address parametr missing in ram_read(address,bytes)")
   return()
  if _bytes==None:
   _bytes=1
  _data = bus.read_i2c_block_data(0x6F, _ram, _bytes)
  return (_data)

 def rtcmap():
  _data = bus.read_i2c_block_data(0x6F, 0, 32) #nacte 32 bajtu od adresy 0
  _t_seconds_st=(_data[0]&0x80)>>7
  _time_seconds=_bcd2dec(_data[0]&0x7F)
  _t_minutes_st=(_data[1]&0x80)>>7
  _time_minutes=_bcd2dec(_data[1]&0x7F)
  _t_hours_12_24=(_data[2]&0x40)>>6
  if _t_hours_12_24==1:
   _t_hours_am_pm=(_data[2]&0x20)>>5
   _time_hours=_bcd2dec(_data[2]&0x1F)
  else:
   _time_hours=_bcd2dec(_data[2]&0x3F)
  _t_day_oscon=(_data[3]&0x20)>>5
  _t_day_vbat=(_data[3]&0x10)>>4
  _t_day_vbaten=(_data[3]&0x8)>>3
  _time_day=_data[3]&0x7
  _time_date=_bcd2dec(_data[4]&0x3F)
  _t_month_lp=(_data[5]&0x20)>>5
  _time_month=_bcd2dec(_data[5]&0x1F)
  _time_year=_bcd2dec(_data[6])
  _control_out=(_data[7]&0x80)>>7
  _control_sqwe=(_data[7]&0x40)>>6
  _control_alm1=(_data[7]&0x20)>>5
  _control_alm0=(_data[7]&0x10)>>4
  _control_extosc=(_data[7]&0x8)>>3
  _control_rs2=(_data[7]&0x4)>>2
  _control_rs1=(_data[7]&0x2)>>1
  _control_rs0=(_data[7]&0x1)
  _alarm0_seconds=_bcd2dec(_data[10]&0x7F)
  _alarm0_minutes=_bcd2dec(_data[11]&0x7F)
  _a0_hours_12_24=(_data[12]&0x40)>>6
  if _a0_hours_12_24==1:
   _a0_hours_am_pm=(_data[12]&0x20)>>5
   _alarm0_hours=_bcd2dec(_data[12]&0x1F)
  else:
   _alarm0_hours=_bcd2dec(_data[12]&0x3F)
  _a0_day_alm0pol=(_data[13]&0x80)>>7
  _a0_day_alm0c2=(_data[13]&0x40)>>6
  _a0_day_alm0c1=(_data[13]&0x20)>>5
  _a0_day_alm0c0=(_data[13]&0x10)>>4
  _a0_day_alm0if=(_data[13]&0x8)>>3
  _alarm0_day=_data[13]&0x7
  _alarm0_date=_bcd2dec(_data[14]&0x3F)
  _alarm0_month=_bcd2dec(_data[15]&0x1F)
  _alarm1_seconds=_bcd2dec(_data[17]&0x7F)
  _alarm1_minutes=_bcd2dec(_data[18]&0x7F)
  _a1_hours_12_24=(_data[19]&0x40)>>6
  if _a1_hours_12_24==1:
   _a1_hours_am_pm=(_data[19]&0x20)>>5
   _alarm1_hours=_bcd2dec(_data[19]&0x1F)
  else:
   _alarm1_hours=_bcd2dec(_data[19]&0x3F)
  _a1_day_alm1pol=(_data[20]&0x80)>>7
  _a1_day_alm1c2=(_data[20]&0x40)>>6
  _a1_day_alm1c1=(_data[20]&0x20)>>5
  _a1_day_alm1c0=(_data[20]&0x10)>>4
  _a1_day_alm1if=(_data[20]&0x8)>>3
  _alarm1_day=_data[20]&0x7
  _alarm1_date=_bcd2dec(_data[21]&0x3F)
  _alarm1_month=_bcd2dec(_data[22]&0x1F)
  _timesaver0_minutes=_bcd2dec(_data[24]&0x7F)
  _t0_hours_12_24=(_data[25]&0x40)>>6
  if _t0_hours_12_24==1: 
   _t0_hours_am_pm=(_data[25]&0x20)>>5
   _timesaver0_hours=_bcd2dec(_data[25]&0x1F)
  else:
   _timesaver0_hours=_bcd2dec(_data[25]&0x3F)
  _timesaver0_date=_bcd2dec(_data[26]&0x3F)
  _timesaver0_day=(_data[27]&0xE0)>>5
  _timesaver0_month=_bcd2dec(_data[27]&0x1F)
  _timesaver1_minutes=_bcd2dec(_data[28]&0x7F)
  _t1_hours_12_24=(_data[29]&0x40)>>6
  if _t1_hours_12_24==1: 
   _t1_hours_am_pm=(_data[29]&0x20)>>5
   _timesaver1_hours=_bcd2dec(_data[29]&0x1F)
  else:
   _timesaver1_hours=_bcd2dec(_data[29]&0x3F)
  _timesaver1_date=_bcd2dec(_data[30]&0x3F)
  _timesaver1_day=(_data[31]&0xE0)>>5
  _timesaver1_month=_bcd2dec(_data[31]&0x1F)

  # full memory map from MCP749xx (with some missing registers also MCP7490M)
  print("00h (Time_Seconds) .." + str(_data[0]) + " (ST=" + str(_t_seconds_st) + ", Seconds=" + str(_time_seconds) + ")")
  print("01h (Time_Minutes) .." + str(_data[1]) + " (Minutes=" + str(_time_minutes) + ")")
  if _t_hours_12_24 == 1:
   print("02h (Time_Hours) .." + str(_data[2]) + " (AM/PM=" + str(_t_hours_am_pm) + ", Hour=" + str(_time_hours) +")")   # platí pro 12 hodinový cyklus
  else:
   print("02h (Time_Hours) .." + str(_data[2]) + " (Hour=" + str(_time_hours) + ")")  # platí pro 24 hodinový cyklus
  print("03h (Time_Day) .." + str(_data[3]) + " (OSCON=" + str(_t_day_oscon) + ", Vbat=" + str(_t_day_vbat) + ", VBATEN=" + str(_t_day_vbaten) + ", Day=" + str(_time_day) + ")")
  print("04h (Time_Date) .." + str(_data[4]) + " (Date=" + str(_time_date) +")")
  print("05h (Time_Month) .." + str(_data[5]) + " (LP=" + str(_t_month_lp) + ", Month=" + str(_time_month)  + ")")
  print("06h (Time_Year) .." + str(_data[6]) + " (Year=20" + str(_time_year) + ")")
  print("07h (Control Reg.) .." + str(_data[7]) + " (OUT=" + str(_control_out) + ", SQWE=" + str(_control_sqwe) + ", ALM1=" + str(_control_alm1) + ", ALM0=" + str(_control_alm0) + ", EXTOSC=" + str(_control_extosc) + ", RS2=" + str(_control_rs2) + ", RS1=" + str(_control_rs1) + ", RS0=" + str(_control_rs0) +")")
  print("08h (Calibration) .." + str(_data[8]))
  print("09h (Unlock ID) .." + str(_data[9]))
  print("0Ah (Alarm0_Seconds) .." + str(_data[10]) + " (Seconds=" + str(_alarm0_seconds) +")")
  print("0Bh (Alarm0_Minutes) .." + str(_data[11]) + " (Minutes=" + str(_alarm0_minutes) +")" )
  if _a0_hours_12_24 == 1:
   print("0Ch (Alarm0_Hours) .." + str(_data[12]) + " (AM/PM=" + str(_a0_hours_am_pm) + " (Hour=" + str(_alarm0_hours) +")")   # platí pro 12 hodinový cyklus
  else:
   print("0Ch (Alarm0_Hours) .." + str(_data[12]) + " (Hour=" + str(_alarm0_hours) + ")")   # platí pro 24 hodinový cyklus
  print("0Dh (Alarm0_Day) .." + str(_data[13]) + " (ALM0POL=" + str(_a0_day_alm0pol) + ", ALM0C2=" + str(_a0_day_alm0c2) + ", ALM0C1=" + str(_a0_day_alm0c1) + ", ALM0C0=" + str(_a0_day_alm0c0) + ", ALM0IF=" + str(_a0_day_alm0if) + ", Day=" + str(_alarm0_day) + ")")
  print("0Eh (Alarm0_Date) .." + str(_data[14]) + " (Date=" + str(_alarm0_date) + ")")
  print("0Fh (Alarm0_Month) .." + str(_data[15]) + " (Month=" + str(_alarm0_month) + ")")
  print("10h (Reserved) .." + str(_data[16]))
  print("11h (Alarm1_Seconds) .." + str(_data[17]) + " (Seconds=" + str(_alarm1_seconds) +")")
  print("12h (Alarm1_Minutes) .." + str(_data[18]) + " (Minutes=" + str(_alarm1_minutes) +")" )
  if _a1_hours_12_24 == 1:
   print("13h (Alarm1_Hours) .." + str(_data[19]) + " (AM/PM=" + str(_a1_hours_am_pm) + " (Hour=" + str(_alarm1_hours) +")")   # platí pro 12 hodinový cyklus
  else:
   print("13h (Alarm1_Hours) .." + str(_data[19]) + " (Hour=" + str(_alarm1_hours) + ")")   # platí pro 24 hodinový cyklus
  print("14h (Alarm1_Day) .." + str(_data[20]) + " (ALM1POL=" + str(_a1_day_alm1pol) + ", ALM1C2=" + str(_a1_day_alm1c2) + ", ALM1C1=" + str(_a1_day_alm1c1) + ", ALM1C0=" + str(_a1_day_alm1c0) + ", ALM1IF=" + str(_a1_day_alm1if) + ", Day=" + str(_alarm1_day) + ")")
  print("15h (Alarm1_Date) .." + str(_data[21]) + " (Date=" + str(_alarm1_date) + ")")
  print("16h (Alarm1_Month) .." + str(_data[22]) + " (Month=" + str(_alarm1_month) + ")")
  print("17h (Reserved) .." + str(_data[23]))
  print("18h (Timesaver0_Minutes) .." + str(_data[24]) + " (Minutes=" + str(_timesaver0_minutes) + ")")
  if _t0_hours_12_24 == 1:
   print("19h (Timesaver0_Hours) .." + str(_data[25]) + ", AM/PM=" + str(_t0_hours_am_pm) + " (Hour=" + str(_timesaver0_hours) + ")")   # platí pro 12 hodinový cyklus
  else:
   print("19h (Timesaver0_Hours) .." + str(_data[25]) + " (Hour=" + str(_timesaver0_hours) + ")")   # platí pro 24 hodinový cyklus
  print("1Ah (Timesaver0_Date) .." + str(_data[26]) + " (Date=" + str(_timesaver0_date) + ")")
  print("1Bh (Timesaver0_Day_Month) .." + str(_data[27]) + " (Day=" + str(_timesaver0_day) + " (Month=" + str(_timesaver0_month) + ")")
  print("1Ch (Timesaver1_Minutes) .." + str(_data[28]) + " (Minutes=" + str(_timesaver1_minutes) + ")")
  if _t1_hours_12_24 == 1:
   print("1Dh (Timesaver1_Hours) .." + str(_data[29]) + " (AM/PM=" + str(_t1_hours_am_pm) +", Hour=" + str(_timesaver1_hours) + ")")   # platí pro 12 hodinový cyklus
  else:
   print("1Dh (Timesaver1_Hours) .." + str(_data[29]) + " (Hour=" + str(_timesaver1_hours) + ")")   # platí pro 24 hodinový cyklus
  print("1Eh (Timesaver1_Date) .." + str(_data[30]) + " (Date=" + str(_timesaver1_date) + ")")
  print("1Fh (Timesaver1_Day_Month) .." + str(_data[31]) + " (Day=" + str(_timesaver1_day) + " (Month=" + str(_timesaver1_month) + ")")

  #_sram = bytearray(64) # pole freesram se musi cist zvlast
  _sram1 = bus.read_i2c_block_data(0x6F, 32, 32) # najednou nelze načíst víc, než 32 bajtů
  _sram2 = bus.read_i2c_block_data(0x6F, 64, 32)
  _sram = _sram1 + _sram2
  #64 bajtů uživatelsky přístupné paměti SRAM je v adresním rozsahu 0x20-0x5f.
  
  print()
  print("free RAM for user:")
  print()
  print("adr     0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F")
  for _radky in range(4):
   _radek=str(_dec2hex(32+(_radky*16)))+"h .. "
   for _sloupce in range(16):
    _radek=_radek+str(_dec2hex(_sram[(_radky*16)+_sloupce]))+"h  "
   print(_radek)
 
  print()
  # id
  data= bus.read_i2c_block_data(0x57, 0xF0, 8)
  _radek="id: "
  for i in range(8):
   _radek=_radek+_dec2hex(data[i])+"h "
  print(_radek)

  #eeprom
  data1= bus.read_i2c_block_data(0x57, 0, 32)
  data2= bus.read_i2c_block_data(0x57, 32, 32)
  data3= bus.read_i2c_block_data(0x57, 64, 32)
  data4= bus.read_i2c_block_data(0x57, 96, 32)
  data=data1+data2+data3+data4
  print()
  print("eeprom:")
  print()
  print("adr     0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F")
  for _radky in range(8):
   _radek=str(_dec2hex(_radky*16))+"h .. "
   for _sloupce in range(16):
    _radek=_radek+str(_dec2hex(data[(_radky*16)+_sloupce]))+"h  "
   print(_radek)
  print()

 def vbaten(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x6F, 3, 1)
   return bool((_data[0]&0x8)>>3)  
  elif not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only vbaten(0) or vbaten(1)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x6F, 3, 1)
   if _value==1:
    _reg[0]=_reg[0]|0x8
   else:
    _reg[0]=_reg[0]&0xF7
   bus.write_byte_data(0x6F, 3, _reg[0])
   time.sleep(0.05)
 
 def vbat(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x6F, 3, 1)
   return bool((_data[0]&0x10)>>4)  
  elif not(_value==0):
   raise ValueError("Parameter allowed only vbat(0)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x6F, 3, 1)
   _reg[0]=_reg[0]&0xEF # reset vbat
   bus.write_byte_data(0x6F, 3, _reg[0])
   time.sleep(0.05)

# předpokládá kompletní shodu a tak jí i nastavuje - netestuje se jednotlivá shoda
# alarm1 není naprogramován

 def alarm0(_a_hour=None,_a_minute=None,_a_second=None,_a_date=None,_a_month=None,_a_wday=None):
  if _a_hour==None or _a_minute==None or _a_second==None or _a_wday==None or _a_month==None or _a_date==None:
   if _a_hour==None and _a_minute==None and _a_second==None and _a_wday==None and _a_month==None and _a_date==None:
    _data = bus.read_i2c_block_data(0x6F, 0x0A, 6)
    _a_second=_bcd2dec(_data[0]&0x7F)
    _a_minute=_bcd2dec(_data[1]&0x7F)
    _a_hour=_bcd2dec(_data[2]&0x3F) # AM/PM neošetřeno
    _a_wday=_data[3]&0x7
    if _a_wday==0:
     _a_wday=7
    _a_date=_bcd2dec(_data[4]&0x3F)
    _a_month=_bcd2dec(_data[5]&0x1F)
    return (_a_hour,_a_minute,_a_second,_a_date,_a_month,_a_wday) # actual alarm
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute,second,wday,month,date)")
    return()
  else:
   if _a_wday==7:
     _a_wday=0
   # _a_wday se níže nastavuje na alarm při kompletní shodě, nenastavuje se ale hardwarový výstup MFP 
   _buff=[_dec2bcd(_a_second), _dec2bcd(_a_minute), _dec2bcd(_a_hour), _dec2bcd(_a_wday)|0x70, _dec2bcd(_a_date), _dec2bcd(_a_month)]
   bus.write_i2c_block_data(0x6F, 0x0A, _buff)
   time.sleep(0.05)
   _buff = bus.read_i2c_block_data(0x6F, 7, 1)
   _buff[0]=_buff[0]|0x10 # alarm 0 is active
   bus.write_byte_data(0x6F, 7, _buff[0])
   time.sleep(0.05)
  
 def alarm0_flag(_flag=None): # parametr 0 clears flag
  _data = bus.read_i2c_block_data(0x6F, 13, 1) # read control_reg
  if _flag==None:
   return bool((_data[0]&0x8)>>3) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data[0] = _data[0]&0xF7 # alarm flag is cleared
   bus.write_byte_data(0x6F, 13, _data[0])
   time.sleep(0.05)
 
 def alarm0_active(_flag=None): # parametr 0 active flag
  _data = bus.read_i2c_block_data(0x6F, 7, 1) # read control_reg
  if _flag==None:
   return bool((_data[0]&0x10)>>4) # alarm flag
  if not(_flag==0 or _flag==1):
    raise ValueError("Parameters allowed: only alarm_active(0) or alarm_active(1)")
    return()
  if (_flag==1):
   _data[0]=_data[0]|0x10 # alarm 0 is active
  else:
   _data[0]=_data[0]&0xEF # alarm 0 is deactive
  bus.write_byte_data(0x6F, 7, _data[0])
  time.sleep(0.05)
 