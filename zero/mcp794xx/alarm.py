# Script nastavuje alarm0 v obvodu (pouze na kompletní shodu)

import rtc # načtení knihovny rtc
rtc=rtc.MCP794xx

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

# V obvodu MCP794xx lze nastavit alarm0 nebo alarm1 na kompletní (sekunda,minuta,hodina,den,měsíc,den v týdnu)
# nebo jednotlivou shodu (sekund, minut, hodin či datumu). V případě jednotlivé shody
# nelze nastavit alarm0 ani alarm1 při shodě např. pouze hodin a minut (pro naprogramování budíku).
# Dá se to řešit např. tak, že se bude při shodě minut testovat hodina.
# Jednotlivá shoda ani alarm1 nejsou v knihovně naprogramovány.

alarm=rtc.alarm0()
print("Přečtení nastaveného času alarmu0: " + str(alarm[0]) + ":" + str(alarm[1]) + ":" + str(alarm[2]) + " " + str(alarm[3]) + "." + str(alarm[4]) + ". (" + days[alarm[5]] + ")")
#rtc.alarm0(8,31,0,2,1,7) # odkomentováním lze nastavit alarm0 (hodina,minuta,sekunda,den,měsíc,den v týdnu)
print("Zjištění, zda je alarm0 aktivní:", rtc.alarm0_active())
#rtc.alarm0_active(1) # odkomentováním lze alarm0 aktivovat (1) nebo deaktivovat (0)
print("Zjištění, zda alarm0 již nastal:", rtc.alarm0_flag()) # pouze pokud byl alarm0 aktivní
#rtc.alarm0_flag(0) # pokud došlo k alarmu0, lze jej odkomentováním vynulovat