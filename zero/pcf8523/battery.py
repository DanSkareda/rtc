# Script nastavuje obvod vzhledem k baterii

import rtc # načtení knihovny rtc
rtc=rtc.PCF8523

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

rtc.cap_sel(1) # po odkomentování nastaví kapacitu oscilátoru: 1 .. 12.5 pF, 0 .. 7 pF
if (rtc.cap_sel() == 1):
 print("Kapacita oscilátoru je nastavená na 12.5 pF.")
else:
 print("Kapacita oscilátoru je nastavená na 7 pF.")
print()

print("Pokud je oscilátor 0, rtc běží (1 je stop stav).")
print("Oscilátor = ", rtc.oscilator())
print()

print("Pokud je VBATEN 0, bude obvod po odpojení napájecího napětí zálohován z baterie.")
print("VBATEN =", rtc.vbaten())
#rtc.vbaten(0) # po odkomentování nastaví mód PM funkce (0...zálohování z baterie povoleno, 7..zálohování z baterie nepovoleno)

print()
print("Pokud je VBAT true, byl obvod někdy v minulosti zálohován z baterie.")
print("VBAT = ", rtc.vbat())
if rtc.vbat()==True:
 print("VBAT lze softwarově smazat.")
 #rtc.vbat(0) # po odkomentování lze příznak VBAT smazat (je povolena pouze 0, jakože vynulovat)

print()
print("Pokud je BATT true, je baterie vybitá a je nutno jí vyměnit (nebo chybí úplně).")
print("BATT = ", rtc.batt())
