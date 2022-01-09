# Script slouží pro zobrazení teploty obvodu

import rtc # načtení knihovny rtc
rtc=rtc.DS3231

# obvod si aktualizuje teplotu každých 64 sekund
# záporné stupně (nejvyšší, znaménkový bit) neřeším
print("Teplota obvodu: " + str(rtc.temperature()) + " °C") 