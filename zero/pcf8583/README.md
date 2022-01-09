I2C komunikace Raspberry Pi (Zero, 4B) s obvodem reálného času (rtc) PCF8583.

Pro komunikaci s rtc je nutné v systému povolit I2C. Poté pro kontrolu správného připojení napište v terminálu "i2cdetect -y 1". Mělo by to vypsat tabulku a v ní adresu rtc 0x50 nebo 0x51.

Předpokládám čas v 24h formátu (AM/PM neřeším).

Napsáno v Python3.

Seznam souborů:

    rtc.py ... knihovna pro komunikaci s obvody řady PCF8583
    setup.py ... automatické (podle systému, případně manuální) nastavení datumu a času v obvodu
    difference.py ... přesné změření rozdílu časů mezi obvodem a pc
    alarm.py ... nastavuje alarm v obvodu
    map.py ... vypíše komentovaný obsah celé paměti obvodu (včetně testu sram)
    schematic.pdf ... schéma připojení rtc k Raspberry

Uvítám jakékoliv připomínky či náměty.
