# Script slouží pro nastavení obvodu ds3231 aktuálním časem. Pro co nejpřesnější 
# nastavení synchronizujte před spuštěním scriptu systémový čas v počítači s časovým serverem.

# Pokud mělo rtc zastavený oscilátor, je nutné script spustit dvakrát.
# Lze tak dosáhnout přesnosti nastavení času asi 0.3 sec.

import rtc # načtení knihovny rtc
from datetime import datetime # pro získání systémového času z počítače
rtc=rtc.DS3231

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

if rtc.osc_flag()==True:
 print("Někdy dříve došlo k zastavení oscilátoru.")
else:
 print("Oscilátor pracuje správně.")   
#rtc.osc_flag(0) # po odkomentování vymaže příznak zastavení oscilátoru

# Čekání na změnu sekundy pro co nejpřesnější nastavení času
today = datetime.now() # systémový čas z počítače (a datum)
minuly=today.second
while today.second==minuly:
  minuly=today.second
  today = datetime.now() # systémový čas z počítače (a datum)

print (" pc: " + str(today.day) + "." + str(today.month) + "." + str(today.year) + " (" + days[today.weekday()+1] + "), " + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second))
rtc.rtctime(today.hour,today.minute,today.second) # automatické nastavení rtc času: hodina, minuta a sekunda. Zároveň odstartuje oscilátor.
rtc.rtcdate(today.day,today.month,today.year,(today.weekday()+1)) # automatické nastavení rtc datumu: den, měsíc, rok a den v týdnu (1..pondělí, 7..neděle)
#rtc.rtctime(13,1,0) # odkomentujte pro manuální nastavení rtc času: hodina, minuta a sekunda. Zároveň odstartuje oscilátor.
#rtc.rtcdate(31,12,2022,5) # odkomentujte pro manuální nastavení rtc datumu: den, měsíc, rok a den v týdnu (1..pondělí, 7..neděle)

# přečtení po nastavení rtc a zobrazení
cas=rtc.rtctime() # aktuální čas
datum=rtc.rtcdate() # aktuální datum
print("rtc: " + str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + days[datum[3]]+ "), " + str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))
