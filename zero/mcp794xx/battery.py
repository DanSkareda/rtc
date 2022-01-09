# Script nastavuje obvod vzhledem k baterii
# Nefunkční u MCP7940M, které nemá vstup pro baterii

import rtc # načtení knihovny rtc
rtc=rtc.MCP794xx

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

print("Pokud je VBATEN true, bude obvod po odpojení napájecího napětí zálohován z baterie.")
print("VBATEN =", rtc.vbaten())
#rtc.vbaten(1) # po odkomentování nastaví VBATEN do true (je povoleno 0 nebo 1)
print()
print("Pokud je VBAT true, byl obvod někdy v minulosti zálohován z baterie.")
print("VBAT = ", rtc.vbat())
if rtc.vbat()==True:
 print("VBAT lze softwarově smazat.")
 #rtc.vbat(0) # po odkomentování lze příznak VBAT smazat (je povolena pouze 0, jakože vynulovat)
 print()
 print("Pokud byl někdy v minulosti zálohován z baterie, lze zjistit od kdy do kdy to bylo.")
 start=rtc.timestamp_down()
 print("Od " + str(start[1]) + ":" + str(start[0]) + " " + str(start[2]) + "." + str(start[3]) + ". (" + days[start[4]] + ")")
 stop = rtc.timestamp_up()
 print("Do " + str(stop[1]) + ":" + str(stop[0]) + " " + str(stop[2]) + "." + str(stop[3]) + ". (" + days[stop[4]] + ")")
