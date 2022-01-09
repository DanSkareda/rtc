# Script slouží pro nastavení obvodu pcf8583 aktuálním časem. Pro co nejpřesnější 
# nastavení synchronizujte před spuštěním scriptu systémový čas v počítači s časovým serverem.

# Pokud mělo rtc zastavený oscilátor, je nutné script spustit dvakrát.
# Lze tak dosáhnout přesnosti nastavení času asi 0.3 sec.

import rtc # načtení knihovny rtc
from datetime import datetime # pro získání systémového času z počítače
rtc=rtc.PCF8583 # defaultní adresa je 0x50 (změnu na 0x51 lze provést ruční editací addr v rtc.py)

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

print("Pokud je oscilátor ve stavu true, obvod pracuje.")
print("Oscilátor = ", rtc.oscilator())
print()
#rtc.oscilator(1) # po odkomentování spustí (1) nebo zastaví (0) oscilátor

# Čekání na změnu sekundy pro co nejpřesnější nastavení času
today = datetime.now() # systémový čas z počítače (a datum)
minuly=today.second
while today.second==minuly:
  minuly=today.second
  today = datetime.now() # systémový čas z počítače (a datum)

print (" pc: " + str(today.day) + "." + str(today.month) + " (" + days[today.weekday()+1] + "), " + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second))
rtc.rtctime(today.hour,today.minute,today.second) # automatické nastavení rtc času: hodina, minuta a sekunda. Zároveň odstartuje oscilátor.
rtc.rtcdate(today.day,today.month,(today.weekday()+1)) # automatické nastavení rtc datumu: den, měsíc (rok je nepoužitelný) a den v týdnu (1..pondělí, 7..neděle)
#rtc.rtctime(13,1,0) # odkomentujte pro manuální nastavení rtc času: hodina, minuta a sekunda. Zároveň odstartuje oscilátor.
#rtc.rtcdate(31,12,5) # odkomentujte pro manuální nastavení rtc datumu: den, měsíc a den v týdnu (1..pondělí, 7..neděle)

# přečtení po nastavení rtc a zobrazení
cas=rtc.rtctime() # aktuální čas
datum=rtc.rtcdate() # aktuální datum
print("rtc: " + str(datum[0]) + "." + str(datum[1]) + " (" + days[datum[2]]+ "), " + str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))

