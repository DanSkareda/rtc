#import machine, utime
#_days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")
_hexs = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F")

def _bcd2dec(_value):
 return (_value>>4)*10 + (_value&0xF)
def _dec2bcd(_value):
 return int((_value//10)*16 + _value%10)
def _dec2hex(_value):
 return str(_hexs[_value//16])+str(_hexs[_value%16])

class RTCC:
 def ram_write(self,_ram=None,_value=None):
  if _ram==None or _value==None:
   raise ValueError("Address parametr missing in ram_write(address,data)")
   return()
  else:
   _data = bytearray(1)
   _data[0]=_value
   self.i2c.writeto_mem(self.addr, _ram, _data, addrsize=8)
   utime.sleep_ms(50)
   return()

 def ram_read(self,_ram=None,_bytes=None):
  if _ram==None and _bytes==None:
   raise ValueError("Any parametr missing in ram_read(address,bytes)")
   return()
  if _bytes==None:
   _bytes=1
  _data = bytearray(_bytes)
  _data = self.i2c.readfrom_mem(self.addr, _ram, _bytes, addrsize=8)
  return (_data)

 def actual(self):
  (pc_year,pc_month,pc_day,pc_hour,pc_minute,pc_second,pc_wday,pc_yday)=utime.localtime(utime.time())
  self.time(pc_hour,pc_minute,pc_second)
  pc_wday=pc_wday+1
  self.date(pc_day,pc_month,pc_year,pc_wday)
  return()

class PCF8523(RTCC):
 def __init__(self, i2c, _address=None):
  self.i2c = i2c
  if _address==None:
   self.addr=0x68 # unchangeable address
  else:
   self.addr=_address
  
 def cap_sel(self,_value=None):
  if _value==None or not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only cap_sel(0) or cap_sel(1)")
   return()
  else:
   _reg = bytearray(1)
   _data = bytearray(1)
   _reg = self.i2c.readfrom_mem(self.addr, 0, 1, addrsize=8)
   if _value==1:
    _data[0]=_reg[0]|0x80
   else:
    _data[0]=_reg[0]&0x7F
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   utime.sleep_ms(50)

 def offset(self,_value=None):
  if _value==None:
   raise ValueError("Parametr missing in offset(value)")
   return()
  else:
   _data = bytearray(1)
   _data[0]=_value
   self.i2c.writeto_mem(self.addr, 14, _data, addrsize=8)
   utime.sleep_ms(50)

 def time(self,_hour=None,_minute=None,_second=None):
  data = bytearray(3)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = self.i2c.readfrom_mem(self.addr, 3, 3, addrsize=8)
    _time_seconds=_bcd2dec(_data[0]&0x7F)
    _time_minutes=_bcd2dec(_data[1]&0x7F)
    _time_hours=_bcd2dec(_data[2]&0x3F)
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in time(hour,minute,second)")
    return()
  else:
   _data[0]=_dec2bcd(_second)
   _data[1]=_dec2bcd(_minute)
   _data[2]=_dec2bcd(_hour)  #pouze pro 24 hod cyklus
   self.i2c.writeto_mem(self.addr, 3, _data, addrsize=8)
   utime.sleep_ms(50)

 def date(self,_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(4)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = self.i2c.readfrom_mem(self.addr, 6, 4, addrsize=8)
    _time_days=_bcd2dec(_data[0]&0x3F)
    _time_weekdays=_bcd2dec(_data[1]&0x7)
    if _time_weekdays==0:
     _time_weekdays=7
    _time_months=_bcd2dec(_data[2]&0x1F)
    _time_years=2000+_bcd2dec(_data[3])
    return (_time_days, _time_months, _time_years, _time_weekdays)
   else:
    raise ValueError("Some parametr missing in date(day,month,year,weekday")
    return()
  else:
   _data[0]=_dec2bcd(_day)
   if _weekday==7:
    _weekday=0
   _data[1]=_weekday
   _data[2]=_dec2bcd(_month)
   _data[3]=_dec2bcd(_year-2000)
   self.i2c.writeto_mem(self.addr, 6, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm_flag(self,_flag=None): # parametr 0 clears flag
  _data = bytearray(1)
  _data = self.i2c.readfrom_mem(self.addr, 1, 1, addrsize=8) # read control_status_2
  _control_status_2=_data[0]
  if _flag==None:
   return bool((_control_status_2&0x8)>>3) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data = bytearray(1)
   _data[0] = _control_status_2&0xF7 # alarm flag is cleared
   self.i2c.writeto_mem(self.addr, 1, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm(self,_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bytearray(1)
    _data = self.i2c.readfrom_mem(self.addr, 1, 1, addrsize=8)
    return bool((_data[0]&0x8)>>3) # alarm flag
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _data = bytearray(4)
   _data[0]=_dec2bcd(_minute)|0x80 # set AE alarm_minute
   _data[1]=_dec2bcd(_hour)|0x80 # set AE alarm_hour
   _data[2]=1 # reset AE alarm_day
   _data[3]=0 # reset AE alarm_weekday
   self.i2c.writeto_mem(self.addr, 10, _data, addrsize=8)
   utime.sleep_ms(50)
   _data = bytearray(2)
   _data = self.i2c.readfrom_mem(self.addr, 0, 2, addrsize=8)
   _register_control_1=_data[0]
   _data[0]=_register_control_1|0x2 # alarm interrupt enabled
   _data[1]=0 # alarm flag is cleared
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   utime.sleep_ms(50)

 def map(self):
  _data = bytearray(20)
  _data = self.i2c.readfrom_mem(self.addr, 0, 20, addrsize=8) #nacte 20 bajtu od adresy 0
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
 
  print("memory map pcf8523:")
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

class PCF8563(RTCC):
 def __init__(self, i2c, _address=None):
  self.i2c = i2c
  if _address==None:
   self.addr=0x51 # unchangeable address
  else:
   self.addr=_address

 def time(self,_hour=None,_minute=None,_second=None):
  _data = bytearray(3)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = self.i2c.readfrom_mem(self.addr, 2, 3, addrsize=8)
    _time_seconds=_bcd2dec(_data[0]&0x7F)
    _time_minutes=_bcd2dec(_data[1]&0x7F)
    _time_hours=_bcd2dec(_data[2]&0x3F)
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in time(hour,minute,second)")
    return()
  else:
   _data[0]=_dec2bcd(_second)
   _data[1]=_dec2bcd(_minute)
   _data[2]=_dec2bcd(_hour)
   self.i2c.writeto_mem(self.addr, 2, _data, addrsize=8)
   utime.sleep_ms(50)

 def date(self,_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(4)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = self.i2c.readfrom_mem(self.addr, 5, 4, addrsize=8)
    _time_days=_bcd2dec(_data[0]&0x3F)
    _time_weekdays=_data[1]&0x7
    if _time_weekdays==0:
     _time_weekdays=7
    _time_months=_bcd2dec(_data[2]&0x1F)
    _time_years=2000+_bcd2dec(_data[3])
    return (_time_days, _time_months, _time_years, _time_weekdays)
   else:
    raise ValueError("Some parametr missing in date(day,month,year,weekday)")
    return()
  else:
   _data[0]=_dec2bcd(_day)
   if _weekday==7:
    _weekday=0
   _data[1]=_weekday
   _data[2]=_dec2bcd(_month)
   _data[3]=_dec2bcd(_year-2000)
   self.i2c.writeto_mem(self.addr, 5, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm_flag(self,_flag=None): # parametr 0 clears flag
  _data = bytearray(1)
  _data = self.i2c.readfrom_mem(self.addr, 1, 1, addrsize=8) # read control_status_2
  _control_status_2=_data[0]
  if _flag==None:
   return bool((_control_status_2&0x8)>>3) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data = bytearray(1)
   _data[0] = _control_status_2&0xF7 # alarm flag is cleared
   self.i2c.writeto_mem(self.addr, 1, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm(self,_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bytearray(1)
    _data = self.i2c.readfrom_mem(self.addr, 1, 1, addrsize=8)
    return bool((_data[0]&0x8)>>3) # alarm flag
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _data = bytearray(4)
   _data[0]=_dec2bcd(_minute)|0x80 # set AE alarm_minute
   _data[1]=_dec2bcd(_hour)|0x80 # set AE alarm_hour
   _data[2]=1 # reset AE alarm_day
   _data[3]=0 # reset AE alarm_weekday
   self.i2c.writeto_mem(self.addr, 9, _data, addrsize=8)
   utime.sleep_ms(50)
   _data = bytearray(1)
   _data[0]=0x2 # alarm flag is cleared, alarm interrupt enabled
   self.i2c.writeto_mem(self.addr, 1, _data, addrsize=8)
   utime.sleep_ms(50)

 def map(self):
  _data = bytearray(16)
  _data = self.i2c.readfrom_mem(self.addr, 0, 16, addrsize=8) #nacte 16 bajtu od adresy 0
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

  print("pcf8563:")
  print("00h (control_status_1) .." + str(_data[0]) + " (test1=" + str(_control_status_1_test1) + ", stop=" + str(_control_status_1_stop) + ", testc=" + str(_control_status_1_testc) + ")")
  print("01h (control_status_2) .." + str(_data[1]) + " (ti_tp=" + str(_control_status_2_ti_tp) + ", af=" + str(_control_status_2_af) + ", tf=" + str(_control_status_2_tf) + ", aie=" + str(_control_status_2_ti_aie) + ", tie=" + str(_control_status_2_tie) + ")")
  print("02h (vl_seconds)       .." + str(_data[2]) + " (vl=" + str(_t_seconds_vl) + ", seconds=" + str(_time_seconds) + ")")
  print("03h (minutes)          .." + str(_data[3]) + " (minutes=" + str(_time_minutes) + ")")
  print("04h (hours)            .." + str(_data[4]) + " (hours=" + str(_time_hours) + ")")
  print("05h (days)             .." + str(_data[5]) + " (days=" + str(_time_days) + ")")
  print("06h (weekdays)         .." + str(_data[6]) + " (weekdays=" + str(_t_weekdays) + ")")
  print("07h (century_months)   .." + str(_data[7]) + " (c=" + str(_t_century) + ", months=" + str(_time_months) + ")")
  print("08h (years)            .." + str(_data[8]) + " (years=" + str(2000+_time_years) + ")")
  print("09h (minute_alarm)     .." + str(_data[9]) + " (ae=" + str(_a_minute_ae) + ", minute=" + str(_alarm_minutes) + ")")
  print("0ah (hour_alarm)       .." + str(_data[10]) + " (ae=" + str(_a_hour_ae) + ", hour=" + str(_alarm_hours) + ")")
  print("0bh (day_alarm)        .." + str(_data[11]) + " (ae=" + str(_a_day_ae) + ", day=" + str(_alarm_days) + ")")
  print("0ch (weekday_alarm)    .." + str(_data[12]) + " (ae=" + str(_a_weekday_ae) + ", weekday=" + str(_alarm_weekdays) + ")")
  print("0dh (clkout_control)   .." + str(_data[13]) + " (fe=" + str(_a_clkout_control_fe) +  ", fd1=" + str(_a_clkout_control_fd1) + ", fd0=" + str(_a_clkout_control_fd0) + ")")
  print("0eh (timer_control)    .." + str(_data[14]) + " (te=" + str(_timer_control_te) +  ", td1=" + str(_timer_control_td1) + ", td0=" + str(_timer_control_td0) + ")")
  print("0fh (timer)            .." + str(_data[15]))
  
class PCF8583(RTCC):
 def __init__(self, i2c, _address=None):
  self.i2c = i2c
  if _address==None:
   self.addr=0x50 # default address 0x50 or 0x51. Only these two.
  if _address==0x50 or _address==0x51:
   self.addr=_address
   return()
  else:
   raise ValueError("Wrong address in pcf8583(i2c,address). Only 0x50 (default for address none) or 0x51.")
   return()   

 def time(self,_hour=None,_minute=None,_second=None):
  _data = bytearray(3)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = self.i2c.readfrom_mem(self.addr, 2, 3, addrsize=8)
    _t_seconds=_data[0]
    _time_seconds=_bcd2dec(_t_seconds)
    _t_minutes=_data[1]
    _time_minutes=_bcd2dec(_t_minutes)
    _t_hours=_data[2] #pouze pro 24 hod cyklus
    _time_hours=_bcd2dec(_t_hours&0x3F)
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in time(hour,minute,second)")
    return()
  else:
   _data[0]=0
   _data[1]=_dec2bcd(_second)
   _data[2]=_dec2bcd(_minute)
   _data[3]=_dec2bcd(_hour)
   self.i2c.writeto_mem(self.addr, 1, _data, addrsize=8)
   utime.sleep_ms(50)

 def date(self,_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(2)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = self.i2c.readfrom_mem(self.addr, 5, 2, addrsize=8)
    _t_year_date=_data[0]
    _time_year=2020+((_t_year_date&0xC0)>>6)
    _time_days=_bcd2dec(_t_year_date&0x3F)
    _t_weekday_month=_data[1]
    _time_weekday=(_t_weekday_month&0xE0)>>5
    if _time_weekday==0:
     _time_weekday=7
    _time_months=_bcd2dec(_t_weekday_month&0x1F)
    return (_time_days, _time_months, _time_year, _time_weekday) 
   else:
    raise ValueError("Some parametr missing in date(day,month,year,weekday")
    return()
  else:
   _data[0]=_dec2bcd(_day)+((_year-2000)<<6)
   if _weekday==7:
    _weekday=0
   _data[1]=(_weekday<<5)+_dec2bcd(_month)
   self.i2c.writeto_mem(self.addr, 5, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm_flag(self,_flag=None): # parametr 0 clears flag
  _data = bytearray(1)
  _data = self.i2c.readfrom_mem(self.addr, 0, 1, addrsize=8) # read control_status_2
  _control_status_1=_data[0]
  if _flag==None:
   return bool((_control_status_2&0x2)>>1) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data = bytearray(1)
   _data[0] = _control_status_1&0xFD # alarm flag is cleared
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm(self,_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bytearray(1)
    _data = self.i2c.readfrom_mem(self.addr, 0, 1, addrsize=8)
    return bool((_control_status_1&0x2)>>1) # alarm flag
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _data = bytearray(7)
   _data[0]=0x90 # alarm flag, interrupt, daily alarm, no timer
   _data[1]=0
   _data[2]=0
   _data[3]=_dec2bcd(_minute)
   _data[4]=_dec2bcd(_hour)
   _data[5]=1
   _data[6]=1
   self.i2c.writeto_mem(self.addr, 8, _data, addrsize=8)
   utime.sleep_ms(50)
   _data[0]=0b10000100 # stop counting, enable alarm control register, clear alarma flag, clear timer flag
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   utime.sleep_ms(50)

 def map(self):
  _data = bytearray(256)
  _data = self.i2c.readfrom_mem(self.addr, 0, 256, addrsize=8) #nacte 20 bajtu od adresy 0
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
  _clock_alarm_function=(_data[8]&0x60)>>4
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
  print("free ram for user:")
  print()
  print("adr     0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F")
  for _radky in range(15):
   _radek=str(_dec2hex(16+(_radky*16)))+"h .. "
   for _sloupce in range(16):
    _radek=_radek+str(_dec2hex(_data[16+((_radky*16)+_sloupce)]))+"h  "
   print(_radek)

class MCP7940x(RTCC):
 def __init__(self, i2c):
  self.i2c = i2c
  self.addr=0x6F # unchangeable address for rtc,sram
  self.id=0x57 # unchangeable address for eeprom,id

#----------------- EEPROM, ID ... address 0x57 --------------------
 def id_write(_value): #zapisuje najednou všech 8 bajtu
  buff=bytearray(1)
  buff[0]=0x55
  i2c.writeto_mem(self.addr, 0x09, buff)
  utime.sleep_ms(50)
  buff=bytearray(1)
  buff[0]=0xAA
  i2c.writeto_mem(self.addr, 0x09, buff)
  utime.sleep_ms(50)
  i2c.writeto_mem(self.id, 0xF0, _value, addrsize=8)
  utime.sleep_ms(50)
  return()

 def eeprom_write(_address,_value):
  _buff=bytearray(1)
  _buff[0]=_value
  i2c.writeto_mem(self.id, _address, _buff, addrsize=8)
  utime.sleep_ms(50)
  return()

#------------------------------------------------------------------

 def calibration(self,_value=None):
  if _value==None:
   _data = bytearray(1)
   _data = self.i2c.readfrom_mem(self.addr, 8, 1, addrsize=8)
   return (_data[0])
  else:
   _data = bytearray(1)
   _data[0]=_value
   self.i2c.writeto_mem(self.addr, 8, _data, addrsize=8)
   utime.sleep_ms(50)

 def oscilator(self,_value=None):
  if _value==None:
   _data = bytearray(1)
   _data = self.i2c.readfrom_mem(self.addr, 3, 1, addrsize=8)
   return bool((_data[0]&0x20)>>5)
  elif not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only oscilator(0) or oscilator(1)")
   return()
  else:
   _reg = bytearray(1)
   _data = bytearray(1)
   _reg = self.i2c.readfrom_mem(self.addr, 0, 1, addrsize=8)
   if _value==1:
    _data[0]=_reg[0]|0x80 # start oscilator
   else:
    _data[0]=_reg[0]&0x7F # stop oscilator
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   utime.sleep_ms(50)

 def time(self,_hour=None,_minute=None,_second=None):
  _data = bytearray(3)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = self.i2c.readfrom_mem(self.addr, 0, 3, addrsize=8)
    _time_seconds=_bcd2dec(_data[0]&0x7F)
    _time_minutes=_bcd2dec(_data[1]&0x7F)
    _time_hours=_bcd2dec(_data[2]&0x3F)
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in time(hour,minute,second)")
    return()
  else:
   _data[0]=_dec2bcd(_second)|0x80 # start oscilator |0x80
   _data[1]=_dec2bcd(_minute)
   _data[2]=_dec2bcd(_hour)
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   utime.sleep_ms(50)

 def date(self,_day=None,_month=None,_year=None,_weekday=None):
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = bytearray(4)
    _data = self.i2c.readfrom_mem(self.addr, 3, 4, addrsize=8)
    _time_weekday=_data[0]&0x7
    if _time_weekday==0:
     _time_weekday=7
    _time_date=_bcd2dec(_data[1]&0x3F)
    _time_month=_bcd2dec(_data[2]&0x1F)
    _time_year=2000+_bcd2dec(_data[3])
    return (_time_date, _time_month, _time_year, _time_weekday)
   else:
    raise ValueError("Some parametr missing in date(day,month,year,weekday")
    return()
  else:
   _data = bytearray(4)
   _data[0] = (self.i2c.readfrom_mem(self.addr, 3, 1, addrsize=8)[0])&0xF8
   if _weekday==7:
    _weekday=0
   _data[0]=_data[0]+_weekday
   _data[1]=_dec2bcd(_day)
   _data[2]=_dec2bcd(_month) # LP set 0
   _data[3]=_dec2bcd(_year-2000)
   self.i2c.writeto_mem(self.addr, 3, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm(self,_hour=None,_minute=None,_second=None,_date=None,_month=None,_day=None):
  if _hour==None or _minute==None or _second==None or _day==None or _month==None or _date==None:
   if _hour==None and _minute==None and _second==None and _day==None and _month==None and _date==None:
    _data = bytearray(1)
    _data = self.i2c.readfrom_mem(self.addr, 13, 1, addrsize=8)
    return bool((_data[0]&0x8)>>3) # alarm flag
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute,second,day,month,date)")
    return()
  else:
   _data = bytearray(6)
   _data[0]=_dec2bcd(_second)
   _data[1]=_dec2bcd(_minute)
   _data[2]=_dec2bcd(_hour)
   if _day==7:
    _day=0   
   _data[3]=_dec2bcd(_day)|0x70
   _data[4]=_dec2bcd(_date)
   _data[5]=_dec2bcd(_month)
   self.i2c.writeto_mem(self.addr, 10, _data, addrsize=8)
   _reg = bytearray(1)
   _data = bytearray(1)
   _reg = self.i2c.readfrom_mem(self.addr, 7, 1, addrsize=8)
   _data[0]=_reg[0]|0x10 # alarm 0 is active
   self.i2c.writeto_mem(self.addr, 7, _data, addrsize=8)
   utime.sleep_ms(50)
  
 def alarm_flag(self,_flag=None): # parametr 0 clears flag
  _data = bytearray(1)
  _data = self.i2c.readfrom_mem(self.addr, 13, 1, addrsize=8) # read control_status_2
  _control_status_2=_data[0]
  if _flag==None:
   return bool((_control_status_2&0x8)>>3) # alarm flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data = bytearray(1)
   _data[0] = _control_status_2&0xF7 # alarm flag is cleared
   self.i2c.writeto_mem(self.addr, 13, _data, addrsize=8)
   utime.sleep_ms(50)
 
 def vbaten(self,_value=None):
  if _value==None:
   _data = bytearray(1)
   _data = self.i2c.readfrom_mem(self.addr, 3, 1, addrsize=8)
   return bool((_data[0]&0x8)>>3)  
  elif not(_value==0 or _value==1):
   raise ValueError("Parameters allowed: only vbaten(0) or vbaten(1)")
   return()
  else:
   _reg = bytearray(1)
   _data = bytearray(1)
   _reg = self.i2c.readfrom_mem(self.addr, 3, 1, addrsize=8)
   if _value==1:
    _data[0]=_reg[0]|0x8
   else:
    _data[0]=_reg[0]&0xF7
   self.i2c.writeto_mem(self.addr, 3, _data, addrsize=8)
   utime.sleep_ms(50)
 
 def vbat(self,_value=None):
  if _value==None:
   _data = bytearray(1)
   _data = self.i2c.readfrom_mem(self.addr, 3, 1, addrsize=8)
   return bool((_data[0]&0x10)>>4)  
  elif not(_value==0):
   raise ValueError("Parameter allowed only vbaten(0)")
   return()
  else:
   _reg = bytearray(1)
   _data = bytearray(1)
   _reg = self.i2c.readfrom_mem(self.addr, 3, 1, addrsize=8)
   _data[0]=_reg[0]&0xEF # reset vbat
   self.i2c.writeto_mem(self.addr, 3, _data, addrsize=8)
   utime.sleep_ms(50)

 def map(self):
  _data = bytearray(32)
  _data = self.i2c.readfrom_mem(self.addr, 0, 32, addrsize=8) #nacte 32 bajtu od adresy 0
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

  print("MCP74902 (s nekterymi chybejicimi registry i MCP7490M):")
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

  _sram = bytearray(64) # pole freesram se musi cist zvlast
  _sram = self.i2c.readfrom_mem(self.addr, 32, 64, addrsize=8)
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
   
class DS3231(RTCC):
 def __init__(self, i2c):
  self.i2c = i2c
  self.addr=0x68 # unchangeable address

 def osc_flag(self,_value=None):
  if _value==None:
   _data = bytearray(1)
   _data = self.i2c.readfrom_mem(self.addr, 15, 1, addrsize=8)
   return bool((_data[0]&0x80)>>7)
  elif not(_value==0):
   raise ValueError("Parameters wrong: only osc_flag(0)")
   return()
  else:
   _reg = bytearray(1)
   _data = bytearray(1)
   _reg = self.i2c.readfrom_mem(self.addr, 15, 1, addrsize=8)
   _data[0]=_reg[0]&0x7F # clear oscilator flag
   self.i2c.writeto_mem(self.addr, 15, _data, addrsize=8)
   utime.sleep_ms(50)

 def time(self,_hour=None,_minute=None,_second=None):
  _data = bytearray(3)
  if _hour==None or _minute==None or _second==None:
   if _hour==None and _minute==None and _second==None:
    _data = self.i2c.readfrom_mem(self.addr, 0, 3, addrsize=8)
    _time_seconds=_bcd2dec(_data[0])
    _time_minutes=_bcd2dec(_data[1])
    _time_hours=_bcd2dec(_data[2]&0x3F) # pouze pro 24 hod cyklus
    return (_time_hours, _time_minutes, _time_seconds)
   else:
    raise ValueError("Some parametr missing in time(hour,minute,second)")
    return()
  else:
   _data[0]=_dec2bcd(_second)
   _data[1]=_dec2bcd(_minute)
   _data[2]=_dec2bcd(_hour)
   self.i2c.writeto_mem(self.addr, 0, _data, addrsize=8)
   _data = bytearray(2)
   _reg = bytearray(2)
   _reg = self.i2c.readfrom_mem(self.addr, 14, 2, addrsize=8)
   _data[0]=_reg[0]&0x7F # start oscilator
   _data[1]=_reg[1]&0x7F # clear oscilator flag
   self.i2c.writeto_mem(self.addr, 14, _data, addrsize=8)
   utime.sleep_ms(50)

 def date(self,_day=None,_month=None,_year=None,_weekday=None):
  _data = bytearray(4)
  if _day==None or _month==None or _year==None or _weekday==None:
   if _day==None and _month==None and _year==None and _weekday==None:
    _data = self.i2c.readfrom_mem(self.addr, 3, 4, addrsize=8)
    _time_weekday=_data[0]
    _time_date=_bcd2dec(_data[1])
    _time_month=_bcd2dec(_data[2]&0x1F) # pouze od roku 2000
    _time_year=2000+_bcd2dec(_data[3])
    return (_time_date, _time_month, _time_year, _time_weekday)
   else:
    raise ValueError("Some parametr missing in date(day,month,year,weekday)")
    return()
  else:
   _data[0]=_weekday
   _data[1]=_dec2bcd(_day)
   _data[2]=_dec2bcd(_month)
   _data[3]=_dec2bcd(_year-2000)
   self.i2c.writeto_mem(self.addr, 3, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm_flag(self,_flag=None): # parametr 0 clears flag
  _data = bytearray(1)
  _data = self.i2c.readfrom_mem(self.addr, 15, 1, addrsize=8) # read status
  _status=_data[0]
  if _flag==None:
   return bool(_status&0x1) # alarm1 flag
  if not(_flag==0):
    raise ValueError("Parameters allowed: only alarm_flag(0)")
    return()
  else:
   _data = bytearray(1)
   _data[0] = _status&0xFE # alarm1 flag cleared
   self.i2c.writeto_mem(self.addr, 15, _data, addrsize=8)
   utime.sleep_ms(50)

 def alarm(self,_hour=None,_minute=None):
  if _hour==None or _minute==None:
   if _hour==None and _minute==None:
    _data = bytearray(1)
    _data = self.i2c.readfrom_mem(self.addr, 15, 1, addrsize=8)
    return bool(_data[0]&0x1) # alarm1 flag
   else:
    raise ValueError("Some parametr missing in alarm(hour,minute)")
    return()
  else:
   _data = bytearray(4)
   _data[0]=0 # seconds
   _data[1]=_dec2bcd(_minute)
   _data[2]=_dec2bcd(_hour)|0x80 # set AE for alarm1 when minute and hour is match
   _data[3]=0x81 # set AE for alarm1 when minute and hour is match
   self.i2c.writeto_mem(self.addr, 7, _data, addrsize=8)
   utime.sleep_ms(50)
   _data = bytearray(2)
   _reg = bytearray(2)
   _reg = self.i2c.readfrom_mem(self.addr, 14, 2, addrsize=8)
   _data[0]=_reg[0]&0xFA # alarm1 interrupt enabled, square wave is output on the INT/SQW pin 
   _data[1]=_reg[1]&0xFE # alarm1 flag cleared
   self.i2c.writeto_mem(self.addr, 14, _data, addrsize=8)
   utime.sleep_ms(50)

 def map(self):
  _data = bytearray(32)
  _data = self.i2c.readfrom_mem(self.addr, 0, 32, addrsize=8) #nacte 32 bajtu od adresy 0
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
    
  print("DS3231:")
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