# Script slouží pro přesné nastavení kalibrace postupnou změnou parametru kalibrace. Porovnává 
# systémový čas v počítači s aktuálním časem v obvodu ds3231 a zobrazuje rozdíl. Pro co nejpřesnější 
# výsledek synchronizujte před spuštěním scriptu systémový čas v počítači s časovým serverem.

import rtc # načtení knihovny rtc
from datetime import datetime # pro získání systémového času z počítače
rtc=rtc.DS3231

#rtc.offset(0) # odkomentujte pro nastavení offsetu, rozsah nastavení -127 až +127, případně 0-255
print("offset: " + str(rtc.offset())) # zobrazuje 0-255

# Čekání na změnu sekundy pro zjištění přesného rozdílu časů
# Pokud je oscilátor zastavený, script se zacyklí ve stavu čekání
cas=rtc.rtctime() # aktuální čas
minuly=cas[2] 
while cas[2]==minuly:
  minuly=cas[2]
  cas=rtc.rtctime() # aktuální čas

datum=rtc.rtcdate() # aktuální datum
today = datetime.now() # systémový čas z počítače (a datum)
dtrtc = datetime(datum[2], datum[1], datum[0], cas[0], cas[1], cas[2]) # složení dat z rtc do formátu systémového času
if dtrtc>today :
  print("rozdíl +", dtrtc-today, "(rtc jde napřed)")
if today>dtrtc :
  print("rozdíl -", today-dtrtc, "(rtc jde pozadu)")
dt = today.strftime("%H:%M:%S")
print("rtc:", str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]) + ", pc:", dt)
