# Script testuje zápis do oblastí SRAM, ID a EEPROM
# Poté přehledně vypíše komentovaný obsah celé paměti rtc

import rtc # načtení knihovny rtc
rtc=rtc.MCP794xx

#64 bajtů uživatelsky přístupné paměti SRAM je v adresním rozsahu 0x20-0x5F.
print("Zapisuji do SRAM na adresu 35 hodnotu 15...")
rtc.ram_write(35,15) # zapisuje do RAM (adresa, bajt)
print("Čtu zapsané...", rtc.ram_read(35)) # čte hodnotu zapsanou do SRAM

id8=[0x55,0x56,0x57,0x58,0x59,0x5A,0x5B,0x5C] # vzorek osmi bajtu ID k zapani
print("Zapisuji ID obvodu", id8, "...")
rtc.id_write(id8) # zapisuje najednou vsech 8 bajtu do 0x57 (ID)
print("Čtu zapsané...", rtc.id_read())

print("Zapisuji do EEPROM na adresu 7 hodnotu 46...")
rtc.eeprom_write(7,46) # zapisuje do EEPROM (adresa, bajt)
print("Čtu zapsané...", rtc.eeprom_read(7))
print()
print("Nyní vypisuji komentovaný obsah celé paměti rtc...")
print()
rtc.rtcmap() # vypíše komentovaný obsah celé paměti rtc