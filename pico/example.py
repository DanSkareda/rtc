import machine,utime,rtc
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

# příklad pro PCF8563 - vypisuje aktuální čas v cyklu 1 sekunda

myrtc=PCF8563(i2c)
while True:
 cas=myrtc.time() # aktualni cas
 print(str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]) + "  .. " + str(myrtc.alarm()))
 utime.sleep(1)

# níže odkomentuj z odpovídajícího bloku metody myrtc dle potřeby

#myrtc=rtc.PCF8523(i2c)
#myrtc.ram_write(0x10, 0x33) # zapis do ram: adresa, data. Pouze jeden bajt
#print(hex(myrtc.ram_read(0x10, 1))) # nebo print(_dec2hex(myrtc.ram_read(0x10,1))) # cteni z ram: adresa, kolik bajtu
#myrtc.cap_sel(1) #nastavuje kapacitu krystalu 12.5 pF
#myrtc.offset(1) # offset zpresnuje chod hodin - nutno zmerit kus od kusu
#myrtc.time(12,42,0) # nastaveni: hodina, minuta, sekunda
#myrtc.date(6,8,2021,5) # nastaveni: den v mesici, mesic, rok, den v tydnu (1..pondeli, 7..nedele)
#myrtc.actual() #nastaveni aktualniho datetime
#myrtc.alarm(19,02) # alarm pri shode: hodina, minuta
#myrtc.alarm_flag(0) #  none..read bit where set in hardware if the alarm was triggered (bool), 0..reset bit
#myrtc.map() # vypise kompletni mapu pameti rtc
#cas=myrtc.time() # precteni: hodina, minuta, sekunda
#print(str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))
#datum=myrtc.date() #precteni: den v mesici, mesic, rok, den v tydnu (1..pondeli, 7..nedele)
#print(str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + str(days[datum[3]]) + ")")

#myrtc=rtc.PCF8563(i2c)
#myrtc.ram_write(0x10, 0x33) # zapis do ram: adresa, data. Pouze jeden bajt
#print(hex(myrtc.ram_read(0x10, 1))) # nebo print(_dec2hex(myrtc.ram_read(0x10,1))) # cteni z ram: adresa, kolik bajtu
#myrtc.time(15,45,0) # nastaveni: hodina, minuta a sekunda
#myrtc.date(6,8,2021,5) # nastaveni: den, mesic, rok a den v tydnu (1..pondeli, 7..nedele)
#myrtc.actual() #nastaveni aktualniho datetime
#myrtc.alarm(19,02) # alarm pri shode: hodina, minuta
#myrtc.alarm_flag(0) #  none..read bit where set in hardware if the alarm was triggered (bool), 0..reset bit
#myrtc.map() # vypise celou pamet rtc
#cas=myrtc.time() # aktualni cas
#print(str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))
#datum=myrtc.date() # aktualni datum
#print(str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + str(days[datum[3]]) + ")")

#myrtc=rtc.PCF8583(i2c,address) # adresy 0x50 nebo 0x51. Pouze tyto dve.
#myrtc.ram_write(0x10, 0x33) # zapis do ram: adresa, data. Pouze jeden bajt
#print(hex(myrtc.ram_read(0x10, 1))) # nebo print(_dec2hex(myrtc.ram_read(0x10,1))) # cteni z ram: adresa, kolik bajtu
#myrtc.time(14,20,0) # nastaveni: hodina, minuta a sekunda
#myrtc.date(6,8,2021,5) # nastaveni: den, mesic, rok a den v tydnu (1..pondeli, 7..nedele)
#myrtc.actual() #nastaveni aktualniho datetime  
#myrtc.alarm(19,02) # alarm pri shode: hodina, minuta
#myrtc.alarm_flag(0) #  none..read bit where set in hardware if the alarm was triggered (bool), 0..reset bit
#myrtc.map() # vypise celou pamet rtc
#cas=myrtc.time() # aktualni cas
#print(str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))
#datum=myrtc.date() # aktualni datum
#print(str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + str(days[datum[3]]) + ")")

#myrtc=rtc.MCP7940x(i2c)
#myrtc.ram_write(0x20, 0x33) # zapis do ram: adresa, data. Pouze jeden bajt
#print(hex(myrtc.ram_read(0x20, 1))) # nebo print(_dec2hex(myrtc.ram_read(0x20,1))) # cteni z ram: adresa, kolik bajtu
#for freeram in range(32,128):
# myrtc.ram_write(freeram,0) #vynuluje freeram, chvili to trva!
#myrtc.calibration(-50) # none..read calibration, value..set calibration # offset zpresnuje chod hodin - nutno zmerit kus od kusu
#print(_dec2hex(myrtc.calibration()))
#myrtc.oscilator() # 1..start oscilator, 0..stop oscilator, none..read oscilator (bool)
#myrtc.vbat(0) # 0..reset indication, none..read "Vcc fails" (power from bat) (bool)
#myrtc.vbaten(1) # 0..disable power from bat, 1..enable, none..read "power of" (bool)

"""
# id
buff=bytearray([0x55,0x56,0x57,0x58,0x59,0x5A,0x5B,0x5C])
id_write(buff) # zapisuje najednou vsech 8 bajtu do 0x57 (ID)
data=bytearray(8)
data= i2c.readfrom_mem(self.id, 0xF0, 8, addrsize=8)
_radek="id: "
for i in range(8):
 _radek=_radek+_dec2hex(data[i])+"h "
print(_radek)
print("id: "+str(int.from_bytes(data, "out of range")))

#eeprom
eeprom_write(5,0x55)
data=bytearray(128)
data= i2c.readfrom_mem(self.id, 0, 128, addrsize=8)
print()
print("eeprom:")
print()
print("adr     0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F")
for _radky in range(8):
 _radek=str(_dec2hex(_radky*16))+"h .. "
 for _sloupce in range(16):
  _radek=_radek+str(_dec2hex(data[(_radky*16)+_sloupce]))+"h  "
 print(_radek)
"""

#myrtc.time(19,51,00) # nastaveni: hodina, minuta a sekunda. Zaroven odstartuje oscilator
#myrtc.date(24,8,2021,3) # nastaveni: den, mesic, rok a den v tydnu (1..pondeli, 7..nedele)
#myrtc.actual() #nastaveni aktualniho datetime
#myrtc.alarm(16,46,00,22,8,7) # alarm0 pri shode: hodina, minuta, sekunda, den, mesic a den v tydnu (1..pondeli, 7..nedele)
#myrtc.alarm_flag(0) #  none..read bit where set in hardware if the alarm was triggered (bool), 0..reset bit
#myrtc.map() # vypise celou pamet rtc
#cas=myrtc.time() # aktualni cas
#print(str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]) + "  .. " + str(myrtc.alarm()))
#datum=myrtc.date() # aktualni datum
#print(str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + str(days[datum[3]]) + ")")

#myrtc=rtc.DS3231(i2c)
#myrtc.ram_write(0x10, 0x33) # zapis do ram: adresa, data. Pouze jeden bajt
#print(hex(myrtc.ram_read(0x10, 1))) # nebo print(_dec2hex(myrtc.ram_read(0x10,1))) # cteni z ram: adresa, kolik bajtu
#myrtc.osc_flag(0) # none..read oscilator flag (1..wrong time), 0..clear oscilator flag
#myrtc.time(9,17,00) # nastaveni: hodina, minuta a sekunda. Zaroven smaze oscilator flag a zapne oscilator i pri Vbat
#myrtc.date(14,8,2021,6) # nastaveni: den, mesic, rok a den v tydnu (1..pondeli, 7..nedele)
#myrtc.actual() #nastaveni aktualniho datetime
#myrtc.alarm(9,56) # alarm pri shode: hodina, minuta
#myrtc.alarm_flag(0) #  none..read bit where set in hardware if the alarm was triggered (bool), 0..reset bit
#myrtc.map() # vypise celou pamet rtc
#cas=myrtc.time() # aktualni cas
#print(str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))
#datum=myrtc.date() # aktualni datum
#print(str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + str(days[datum[3]]) + ")")
