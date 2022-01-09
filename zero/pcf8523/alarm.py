# Script nastavuje alarm v obvodu

import rtc # načtení knihovny rtc
rtc=rtc.PCF8523

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

# V obvodu lze nastavit alarm na shodu (minut, hodin, dne v měsíci či dne v týdnu) volitelně
# podle toho, zda je u dané položky nastavený příznak pro alarm. Knihovna nastavuje alarm
# pouze na shodu hodin a minut.

alarm=rtc.alarm()
print("Přečtení nastaveného času alarmu: " + str(alarm[0]) + ":" + str(alarm[1]))
#rtc.alarm(11,25) # odkomentováním lze nastavit alarm (hodina,minuta)
print("Zjištění, zda alarm již nastal:", rtc.alarm_flag()) # true..nastal
#rtc.alarm_flag(0) # odkomentováním lze vynulovat příznak alarmu