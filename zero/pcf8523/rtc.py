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

class PCF8523:

 def vbaten(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x68, 2, 1)
   return ((_data[0]&0xE0)>>5) # vraci mód PM funkce (0...VBAT enable, 7..VBAT disable)
  elif not(_value>=0 and _value<=7):
   raise ValueError("Parameters allowed: only vbaten(0) to vbaten(7)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x68, 2, 1)
   _reg[0]=(_reg[0]&0x1F)|(_value<<5)
   bus.write_byte_data(0x68, 2, _reg[0])
   time.sleep(0.05)
 
 def vbat(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x68, 2, 1)
   return bool((_data[0]&0x8)>>3)  
  elif not(_value==0):
   raise ValueError("Parameter allowed only vbat(0)")
   return()
  else:
   _reg = bus.read_i2c_block_data(0x68, 2, 1)
   _reg[0]=_reg[0]&0xF7 # reset vbat
   bus.write_byte_data(0x68, 2, _reg[0])
   time.sleep(0.05)

 def batt():
  _data = bus.read_i2c_block_data(0x68, 2, 1)
  return bool((_data[0]&0x4)>>2)  

 def cap_sel(_value=None):
  if _value==None:
   _reg = bus.read_i2c_block_data(0x68, 0, 1)
   return((_reg[0]&0x80)>>7)
  if not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only cap_sel(0) or cap_sel(1)")
   return()
  _reg = bus.read_i2c_block_data(0x68, 0, 1)
  if _value==1:
   _reg[0]=_reg[0]|0x80
  else:
   _reg[0]=_reg[0]&0x7F
  bus.write_byte_data(0x68, 0, _reg[0])
  time.sleep(0.05)

 def oscilator():
  _reg = bus.read_i2c_block_data(0x68, 0, 1)
  return (_reg[0]&0x20)>>5

 def offset(_value=None):
  if _value==None:
   _data = bus.read_i2c_block_data(0x68, 14, 1)
   return (_data[0])
  else:
   bus.write_byte_data(0x68, 14, _value)
   time.sleep(0.05)

 def rtctime(_hour=None,_minute=None,_second=None):
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = bus.read_i2c_block_data(0x68, 3, 3)
    _time_seconds=_bcd2dec(_data[0]&0x7F)
    _time_minutes=_bcd2dec(_data[1]&0x7F)
    _time_hours=_bcd2dec(_data[2]&0x3F) # AM/PM neošetřeno
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in rtctime(hour,minute,second)")
    return()
  else:
   _data=[_dec2bcd(_second)&0x7F, _dec2bcd(_minute), _dec2bcd(_hour)] # start oscilator &0x7F
   bus.write_i2c_block_data(0x68, 3, _data)
   time.sleep(0.05)

 def rtcdate(_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(4)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = bus.read_i2c_block_data(0x68, 6, 4)
    _time_days=_bcd2dec(_data[0]&0x3F)
    _time_weekdays=_bcd2dec(_data[1]&0x7)
    if _time_weekdays==0:
     _time_weekdays=7
    _time_months=_bcd2dec(_data[2]&0x1F)
    _time_years=2000+_bcd2dec(_data[3])
    return (_time_days, _time_months, _time_years, _time_weekdays)
   else:
    raise ValueError("Some parametr missing in rtcdate(day,month,year,weekday")
    return()
  else:
   if _weekday==7:
    _weekday=0
   _data=[_dec2bcd(_day), _weekday, _dec2bcd(_month), _dec2bcd(_year-2000)]
   bus.write_i2c_block_data(0x68, 6, _data)
   time.sleep(0.05)

 def alarm_flag(_flag=None): # parametr 0 clears flag
  _data = bus.read_i2c_block_data(0x68, 1, 1) # read control_status_2
  if _flag==None:
   return bool((_data[0]&0x8)>>3) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data[0] = _data[0]&0xF7 # alarm flag is cleared
   bus.write_byte_data(0x68, 1, _data[0])
   time.sleep(0.05)
 
 def alarm(_a_hour=None,_a_minute=None):
  if _a_hour==None or _a_minute==None:
   if _a_hour==None and _a_minute==None:
    _data = bus.read_i2c_block_data(0x68, 0x0A, 4)
    _a_minute=_bcd2dec(_data[0]&0x7F)
    _a_hour=_bcd2dec(_data[1]&0x3F) # AM/PM neošetřeno
    return (_a_hour,_a_minute) # actual alarm
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _buff=[_dec2bcd(_a_minute), _dec2bcd(_a_hour), 0x81, 0x80] # nastavení pouze na shodu hodin a minut
   bus.write_i2c_block_data(0x68, 0x0A, _buff)
   time.sleep(0.05)
   _data = bus.read_i2c_block_data(0x68, 1, 1)
   _data[0] = _data[0]&0xF7
   bus.write_byte_data(0x68, 1, _data[0]) # smazani flagu alarmu
   time.sleep(0.05)
   
 def rtcmap():
  _data = bus.read_i2c_block_data(0x68, 0, 20) #nacte 20 bajtu od adresy 0
  _control_1_cap_sel=(_data[0]&0x80)>>7
  _control_1_t=(_data[0]&0x40)>>6
  _control_1_stop=(_data[0]&0x20)>>5
  _control_1_sr=(_data[0]&0x10)>>4
  _control_1_12_24=(_data[0]&0x8)>>3
  _control_1_sie=(_data[0]&0x4)>>2
  _control_1_aie=(_data[0]&0x2)>>1
  _control_1_cie=_data[0]&0x1
  _control_2_wtaf=(_data[1]&0x80)>>7
  _control_2_ctaf=(_data[1]&0x40)>>6
  _control_2_ctbf=(_data[1]&0x20)>>5
  _control_2_sf=(_data[1]&0x10)>>4
  _control_2_af=(_data[1]&0x8)>>3
  _control_2_wtaie=(_data[1]&0x4)>>2
  _control_2_ctaie=(_data[1]&0x2)>>1
  _control_2_ctbie=_data[1]&0x1
  _control_3_pm=(_data[2]&0xe0)>>5
  _control_3_bsf=(_data[2]&0x8)>>3
  _control_3_blf=(_data[2]&0x4)>>2
  _control_3_bsie=(_data[2]&0x2)>>1
  _control_3_blie=_data[2]&0x1
  _t_seconds_os=(_data[3]&0x80)>>7
  _time_seconds=_bcd2dec(_data[3]&0x7f)
  _time_minutes=_bcd2dec(_data[4]&0x7f)
  if _control_1_12_24==1 : #12
   _t_hours_ampm=(_data[5]&0x20)>>5
   _time_hours=_bcd2dec(_data[5]&0x1f)
  else: #24
   _time_hours=_bcd2dec(_data[5]&0x3f)
  _time_days=_bcd2dec(_data[6]&0x3f)
  _time_weekdays=_bcd2dec(_data[7]&0x7)
  _time_months=_bcd2dec(_data[8]&0x1f)
  _time_years=_bcd2dec(_data[9])
  _a_minute_aen_m=(_data[10]&0x80)>>7
  _alarm_minute=_bcd2dec(_data[10]&0x7f)
  if _control_1_12_24==1: #12
   _a_hour_aen_h=(_data[11]&0x80)>>7
   _a_hour_ampm=(_data[11]&0x20)>>5
   _alarm_hour=_bcd2dec(_data[11]&0x1f)
  else: #24
   _a_hour_aen_h=(_data[11]&0x80)>>7
   _alarm_hour=_bcd2dec(_data[11]&0x3f)
  _a_day_aen_d=(_data[12]&0x80)>>7
  _alarm_day=_bcd2dec(_data[12]&0x3f)
  _a_weekday_aen_w=(_data[13]&0x80)>>7
  _alarm_weekday=_bcd2dec(_data[13]&0x7)
  _tmr_clkout_ctrl_tam=(_data[15]&0x80)>>7
  _tmr_clkout_ctrl_tbm=(_data[15]&0x40)>>6
  _tmr_clkout_ctrl_cof=(_data[15]&0x38)>>3
  _tmr_clkout_ctrl_tac=(_data[15]&0x6)>>1
  _tmr_clkout_ctrl_tbc=_data[15]&0x1
  _tmr_a_freq_ctrl_taq=_data[16]&0x7
  _tmr_b_freq_ctrl_tbw=(_data[18]&0x70)>>4
  _tmr_b_freq_ctrl_tbq=_data[18]&0x7
 
  # full memory map
  print("00h (control_1)       .. "+ str(_data[0]) + " (cap_sel=" + str(_control_1_cap_sel) + ", t=" + str(_control_1_t) + ", stop=" + str(_control_1_stop) + ", sr=" + str(_control_1_sr)+ ", 12_24=" + str(_control_1_12_24) + ", sie=" + str(_control_1_sie) + ", aie=" + str(_control_1_aie) + ", cie=" + str(_control_1_cie) + ")")
  print("01h (control_2)       .. "+ str(_data[1]) + " (wtaf=" + str(_control_2_wtaf) + ", ctaf=" + str(_control_2_ctaf) + ", ctbr=" + str(_control_2_ctbf) + ", sf=" + str(_control_2_sf)+ ", af=" + str(_control_2_af) + ", wtaie=" + str(_control_2_wtaie) + ", ctaie=" + str(_control_2_ctaie) + ", ctbie=" + str(_control_2_ctbie) + ")")
  print("02h (control_3)       .. "+ str(_data[2]) + " (pm=" + str(_control_3_pm) + ", bsf=" + str(_control_3_bsf) + ", blf=" + str(_control_3_blf) + ", bsie=" + str(_control_3_bsie) + ", blie=" + str(_control_3_blie) + ")")
  print("03h (seconds)         .. "+ str(_data[3]) + " (os=" + str(_t_seconds_os) + ", seconds=" + str(_time_seconds) + ")")
  print("04h (minutes)         .. "+ str(_data[4]) + " (minutes=" + str(_time_minutes) + ")")
  if _control_1_12_24==1: #12
   print("05h (hours)           .. "+ str(_data[5]) + " (ampm=" + str(_t_hours_ampm) + ", hours=" + str(_time_hours) + ")")
  else: #24
   print("05h (hours)           .. "+ str(_data[5]) + " (hours=" + str(_time_hours) + ")")
  print("06h (days)            .. "+ str(_data[6]) + " (days=" + str(_time_days) + ")")
  print("07h (weekdays)        .. "+ str(_data[7]) + " (weekdays=" + str(_time_weekdays) + ", " + days[_time_weekdays] +")")
  print("08h (months)          .. "+ str(_data[8]) + " (month=" + str(_time_months) + ")")
  print("09h (years)           .. "+ str(_data[9]) + " (years=20" + str(_time_years) +")")
  print("0ah (minute_alarm)    .. "+ str(_data[10]) + " (aen_m=" + str(_a_minute_aen_m) + ", minute_alarm=" + str(_alarm_minute) + ")")
  if _control_1_12_24==1: #12
   print("0bh (hour_alarm)      .. "+ str(_data[11]) + " (aen_h=" + str(_a_hour_aen_h) + ", ampm=" + str(a_hour_ampm) + ", hour_alarm=" + str(_alarm_hour) + ")")
  else: #24
   print("0bh (hour_alarm)      .. "+ str(_data[11]) + " (aen_h=" + str(_a_hour_aen_h) + ", hour_alarm=" + str(_alarm_hour) + ")")
  print("0ch (day_alarm)       .. "+ str(_data[12]) + " (aen_d=" + str(_a_day_aen_d) + ", day_alarm=" + str(_alarm_day) + ")")
  print("0dh (weekday_alarm)   .. "+ str(_data[13]) + " (aen_w=" + str(_a_weekday_aen_w) + ", weekday_alarm=" + str(_alarm_weekday) + ")")
  print("0eh (offset)          .. "+ str(_data[14]))
  print("0fh (tmr_clkout_ctrl) .. "+ str(_data[15]) + " (tam=" + str(_tmr_clkout_ctrl_tam) + ", tbm=" + str(_tmr_clkout_ctrl_tbm) + ", cof=" + str(_tmr_clkout_ctrl_cof) + ", tac=" + str(_tmr_clkout_ctrl_tac) + ", tbc=" + str(_tmr_clkout_ctrl_tbc) +")")
  print("10h (tmr_a_freq_ctrl) .. "+ str(_data[16]) + " (" + "taq=" + str(_tmr_a_freq_ctrl_taq) + ")")
  print("11h (tmr_a_reg)       .. "+ str(_data[17]))
  print("12h (tmr_b_freq_ctrl) .. "+ str(_data[18]) + " (" + "tbw=" + str(_tmr_b_freq_ctrl_tbw) + ", tbq=" + str(_tmr_b_freq_ctrl_tbq) + ")")
  print("13h (tmr_b_reg)       .. "+ str(_data[19]))
