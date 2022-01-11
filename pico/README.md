I2C komunikace Raspberry Pi Pico s obvody reálného času (rtc).

Odzkoušeno na obvodech:

- PCF8523
- PCF8563
- PCF8583
- MCP7940x ( odzkoušeno na: MCP7940M, MCP79402, MCP79411, MCP79412)
- DS3231

Předpokládám čas v 24h formátu (AM/PM neřeším).

Napsáno v MicroPython.

Seznam souborů:

* rtc.py ... knihovna pro komunikaci s rtc obvody (knihovnu nutno nahrát do adresáře LIB v Pico)
* example.py ... příklady komunikace s rtc obvody
* schematic.pdf ... schéma připojení rtc k Raspberry

Uvítám jakékoliv připomínky či náměty.
