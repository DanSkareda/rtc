I2C komunikace Raspberry Pi (Zero, 4B) s obvody reálného času (rtc) řady MCP794xx. 

Pro komunikaci s rtc je nutné v systému povolit I2C. Poté pro kontrolu správného připojení napište v terminálu "i2cdetect -y 1". Mělo by to vypsat tabulku a v ní adresu rtc 0x6F, případně ještě i adresu eepromu 0x57.

Odzkoušeno na obvodech:

- MCP7940M (částečně funkční)
- MCP79402
- MCP79411
- MCP79412

Předpokládám čas v 24h formátu (AM/PM neřeším).

Napsáno v Python3.

Seznam souborů:

* rtc.py ... knihovna pro komunikaci s obvody řady MCP794xx
* setup.py ... automatické (podle systému, případně manuální) nastavení datumu a času v obvodu
* difference.py ... přesné změření rozdílu časů mezi obvodem a pc
* alarm.py ... nastavuje alarm0 v obvodu
* battery.py ... nastavuje obvod vzhledem k baterii
* map.py ... vypíše komentovaný obsah celé paměti obvodu (včetně testu sram, id a eeprom)
* schematic.pdf ... schéma připojení rtc k Raspberry

Uvítám jakékoliv připomínky či náměty.