# Script slouží pro nastavení obvodu mcp794xx aktuálním časem. Pro co nejpřesnější 
# nastavení synchronizujte před spuštěním scriptu systémový čas v počítači s časovým serverem.

# Pokud mělo rtc zastavený oscilátor, je nutné script spustit dvakrát.
# Lze tak dosáhnout přesnosti nastavení času asi 0.3 sec.

import rtc # načtení knihovny rtc
from datetime import datetime # pro získání systémového času z počítače
rtc=rtc.MCP794xx

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

print (" pc: " + str(today.day) + "." + str(today.month) + "." + str(today.year) + " (" + days[today.weekday()+1] + "), " + str(today.hour) + ":" + str(today.minute) + ":" + str(today.second))

rtc.rtctime(today.hour,today.minute,today.second) # automatické nastavení rtc času: hodina, minuta a sekunda. Zároveň odstartuje oscilátor.
rtc.rtcdate(today.day,today.month,today.year,(today.weekday()+1)) # automatické nastavení rtc datumu: den, měsíc, rok a den v týdnu (1..pondělí, 7..neděle)
#rtc.rtctime(13,30,0) # odkomentujte pro manuální nastavení rtc času: hodina, minuta a sekunda. Zároveň odstartuje oscilátor.
#rtc.rtcdate(31,12,2021,5) # odkomentujte pro manuální nastavení rtc datumu: den, měsíc, rok a den v týdnu (1..pondělí, 7..neděle)

# přečtení po nastavení rtc a zobrazení
cas=rtc.rtctime() # aktuální čas
datum=rtc.rtcdate() # aktuální datum
print("rtc: " + str(datum[0]) + "." + str(datum[1]) + "." + str(datum[2]) + " (" + days[datum[3]] + "), " + str(cas[0]) + ":" + str(cas[1]) + ":" + str(cas[2]))

rtc.vbaten(1) # nastaveno zálohování obvodu z baterie (nefunkční u MCP7940M, které nemá vstup pro baterii)
if rtc.vbaten()==1:
 print("Podařilo se nastavit zálohování obvodu z baterie.")
else:
 print("Nepodařilo se nastavit zálohování obvodu z baterie.")