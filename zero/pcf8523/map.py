# Script přehledně vypíše komentovaný obsah celé paměti rtc

import rtc # načtení knihovny rtc
rtc=rtc.PCF8523

print("Nyní vypisuji komentovaný obsah celé paměti rtc...")
print()
rtc.rtcmap() # vypíše komentovaný obsah celé paměti rtc