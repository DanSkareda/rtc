# Script přehledně vypíše komentovaný obsah celé paměti rtc

import rtc # načtení knihovny rtc
rtc=rtc.PCF8583

#240 bajtů uživatelsky přístupné paměti SRAM je v adresním rozsahu 0x10-0xFF.
print("Zapisuji do SRAM na adresu 35 hodnotu 15...")
rtc.ram_write(35,15) # zapisuje do RAM (adresa, bajt)
print("Čtu zapsané...", rtc.ram_read(35)) # čte hodnotu zapsanou do SRAM

print()
print("Nyní vypisuji komentovaný obsah celé paměti rtc...")
print()
rtc.rtcmap() # vypíše komentovaný obsah celé paměti rtc