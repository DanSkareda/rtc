I2C komunikace Raspberry Pi (Zero, 4B) s obvodem reálného času (rtc) PCF8523.

Pro komunikaci s rtc je nutné v systému povolit I2C. Poté pro kontrolu správného připojení napište v terminálu "i2cdetect -y 1". Mělo by to vypsat tabulku a v ní adresu rtc 0x68.

Předpokládám čas v 24h formátu (AM/PM neřeším).

Napsáno v Python3.

Seznam souborů:

    rtc.py ... knihovna pro komunikaci s obvody řady PCF8523
    setup.py ... automatické (podle systému, případně manuální) nastavení datumu a času v obvodu
    difference.py ... přesné změření rozdílu časů mezi obvodem a pc
    alarm.py ... nastavuje alarm v obvodu na shodu hodin a minut
    battery.py ... nastavuje obvod vzhledem k baterii
    map.py ... vypíše komentovaný obsah celé paměti obvodu
    schematic.pdf ... schéma připojení rtc k Raspberry

Uvítám jakékoliv připomínky či náměty.
