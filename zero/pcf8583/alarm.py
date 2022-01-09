# Script nastavuje alarm v obvodu

import rtc # načtení knihovny rtc
rtc=rtc.PCF8583

days = ("neděle", "pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle")

# V obvodu lze nastavit alarm na shodu minut a hodin (včetně sekund a setin sekund),
# dne v týdnu, nebo datumu. Knihovna nastavuje alarm pouze na shodu hodin a minut v nula sekund.

alarm=rtc.alarm()
print("Přečtení nastaveného času alarmu: " + str(alarm[0]) + ":" + str(alarm[1]))
#rtc.alarm(14,45) # odkomentováním lze nastavit alarm (hodina,minuta)
print("Zjištění, zda alarm již nastal:", rtc.alarm_flag()) # true..nastal
#rtc.alarm_flag(0) # odkomentováním lze vynulovat příznak alarmu