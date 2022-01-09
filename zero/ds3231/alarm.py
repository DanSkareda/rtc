# Script nastavuje alarm v obvodu

import rtc # načtení knihovny rtc
rtc=rtc.DS3231

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

# V obvodu lze nastavit alarm na postupnou shodu sekund, minut, hodin a dne.
# Knihovna nastavuje alarm pouze na shodu hodin a minut v nula sekund.

alarm=rtc.alarm()
print("Přečtení nastaveného času alarmu: " + str(alarm[0]) + ":" + str(alarm[1]))
#rtc.alarm(5,18) # odkomentováním lze nastavit alarm (hodina,minuta)
print("Zjištění, zda alarm již nastal:", rtc.alarm_flag()) # true..nastal
#rtc.alarm_flag(0) # odkomentováním lze vynulovat příznak alarmu