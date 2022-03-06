[![streamdeck_ui - Linux kompatibles UI für das Elgato Stream Deck](art/logo_large.png)](https://timothycrosley.github.io/streamdeck-ui/)
_________________

[![PyPI version](https://badge.fury.io/py/streamdeck-ui.svg)](http://badge.fury.io/py/streamdeck-ui)
[![Test Status](https://github.com/timothycrosley/streamdeck-ui/workflows/Test/badge.svg?branch=master)](https://github.com/timothycrosley/streamdeck-ui/actions?query=workflow%3ATest)
[![codecov](https://codecov.io/gh/timothycrosley/streamdeck-ui/branch/master/graph/badge.svg)](https://codecov.io/gh/timothycrosley/streamdeck-ui)
[![Join the chat at https://gitter.im/timothycrosley/streamdeck-ui](https://badges.gitter.im/timothycrosley/streamdeck-ui.svg)](https://gitter.im/timothycrosley/streamdeck-ui?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/streamdeck-ui/)
[![Downloads](https://pepy.tech/badge/streamdeck-ui)](https://pepy.tech/project/streamdeck-ui)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)
 
_________________

[Lese die neueste Dokumentation](https://timothycrosley.github.io/streamdeck-ui/) 
[Release notes](CHANGELOG.md) 
_________________

**streamdeck_ui** Ein Linux kompatibles UserInterface für das Elgato Stream Deck.

![Streamdeck UI Usage Example](art/example.gif)

## Eigenschaften

* **Linux Kompatibel**: Ermöglicht die Nutzung aller Stream Deck Geräte mit Linux ohne code zu benötigen.
* **Mehrere Geräte**: Ermöglicht die Verbindung und Konfiguration mehrere Stream Deck Geräte an einem Computer.
* **Helligkeits-Steuerung**: Unterstützt die Einstellung der Helligkeit von der Konfigurations-Oberfläche und den Knöpfen am Gerät selbst.
* **Konfigurierbares Tastenbild**: Icon + Text, nur Icon und nur Text sind pro Taste des Stream Decks konfigurierbar.
* **Multi-Action Unterstützung**: Kommandos starten, Text schreiben und Hotkey-Kombinationen drücken mit einem einzigen Tastendruck auf dem Stream Deck.
* **Tasten-Seiten**: streamdeck_ui bietet mehrere Seiten von Tasten mit dynamischer Einstellung von Tasten zum Umschalten zwischen ihnen.
* **Automatisches Wiederverbinden**: Das Gerät wird automatisch und problemlos wieder verbunden, falls das Gerät ab- und wieder angesteckt wurde.
* **Import/Export**: Bietet das Abspeichern und Wiederherstellen ganzer Stream Deck Konfigurationen.

Die Kommunikation mit dem Streamdeck erfolgt durch die [Python Elgato Stream Deck Library](https://github.com/abcminiuser/python-elgato-streamdeck#python-elgato-stream-deck-library).

## Linux Schnellstart
**Python 3.8** wird benötigt. Sie können die Version, die sie installiert haben, überprüfen mit `python3 --version`.
### Vorgefertigte Skripte
Es gibt fertige Skripte um streamdeck_ui auf [Debian/Ubuntu](scripts/ubuntu_install.sh) und [Fedora](scripts/fedora_install.sh) zu installieren.
### Manuelle Installation
Um streamdeck_ui unter Linux zu verwenden, müssen einige System-Bibliotheken als Voraussetzung installiert werden.
Die Namen dieser Bibliotheken können, abhängig von ihrem Betriebssystem, variieren.  
Debian / Ubuntu:
``` console
sudo apt install python3-pip libhidapi-libusb0 libxcb-xinerama0
```
Fedora:
``` console
sudo dnf install python3-pip python3-devel hidapi
```
Wenn sie die GNOME shell verwenden, könnten sie eine Erweiterung, die den [KStatusNotifierItem/AppIndicator Support](https://extensions.gnome.org/extension/615/appindicator-support/) bietet, manuell installieren müssen um das Tray-Icon anzuzeigen.

Um streamdeck_ui ohne root-Rechte zu benutzen, müssen sie ihrem user vollen Zugriff auf das Gerät erlauben.

Fügen sie die folgenden udev rules mit Hilfe ihres Editors hinzu:
``` console
sudoedit /etc/udev/rules.d/70-streamdeck.rules
# Wenn das nicht funktioniert, versuchen sie:
sudo nano /etc/udev/rules.d/70-streamdeck.rules
```
Fügen sie die folgenden Zeilen ein:
``` console
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", TAG+="uaccess"
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0080", TAG+="uaccess"
```
Aktivieren sie die Regeln:
``` console
sudo udevadm trigger
```

Die Installation der Anwendung selbst erfolgt via pip:
``` console
pip3 install streamdeck-ui --user
```
Stellen sie sicher, dass `$HOME/.local/bin` in ihrem PATH enthalten ist.  
Wenn das nicht der Fall ist, fügen sie
``` console
PATH=$PATH:$HOME/.local/bin
```
an das Ende ihrer shell Konfigurationsdatei (wahrscheinlich .bashrc in ihrem home directory) hinzu.

Jetzt können sie `streamdeck` starten um mit der Konfiguration zu beginnen.

``` console
streamdeck
```

Es wird empfohlen `streamdeck` in die Autostart-Liste ihrer Fenster-Umgebung aufzunehmen. Wenn sie es verwenden wollen ohne dass das Benutzer-Interface angezeigt wird, verwenden sie`streamdeck -n`.

## Allgemeiner Schnellstart

Auf anderen Betriebssystemen müssen sie die benötigten [Abhängigkeiten](https://github.com/abcminiuser/python-elgato-streamdeck#package-dependencies) der Bibliothek installieren.
Danach verwenden sie pip zur Installation der Anwendung:

``` console
pip3 install streamdeck-ui --user
streamdeck
```

Beachten sie auch die Anleitungen für
* [CentOS 7](docs/centos.md)
* [Ubuntu 18.04](docs/ubuntu1804.md)

## Hilfe
### Befehl (Command)
Geben sie einen Befehl in das Feld "Command" ein, um ihn auszuführen. In Ubuntu/Fedora starten sie ein Terminal mit `gnome-terminal`, `obs` startet OBS.

#### Beispiele (Ubuntu)
Sie können ein tool wie `xdotool` verwenden, um mit anderen Programmen zu interagieren.

Finden sie das Fenster, das mit `Meet - ` beginnt, und setzen sie den Fokus darauf. Das hilft ihnen, wenn sie eine Google Meet Sitzung auf irgend einem Tab haben, die aber hinter anderen Fenstern verloren gegangen ist.
``` console
xdotool search --name '^Meet - .+$' windowactivate 
```
> Der Meeting-Tab muss aktiv sein wenn sie mehrere Tabs offen haben, da der Fenstertitel vom derzeit aktiven Tab gesetzt wird.

Finden sie das Fenster, das mit `Meet - ` beginnt, und senden sie `ctrl+d` dorthin. Das bewirkt das Umschalten der Stummschaltung (mute button) in Google Meet.
``` console
xdotool search --name '^Meet - .+$' windowactivate --sync key ctrl+d
```

Drehen sie die System-Lautstärke um einen gewissen Prozentsatz hoch (oder runter). Wir nehmen an, sie verwenden PulseAudio/Alsa Mixer.
``` console
amixer -D pulse sset Master 20%+
```
Wenn sie einen Befehl abgeben wollen der shell-script spezifische Dinge wie `&&` oder `|` enthält, dann starten sie ihn via bash. Dieser Befehl wird de Fokus auf Firefox setzen, indem es `wmctrl` nutzt, und dann den Fokus auf den ersten Tab verschieben: 

``` console
bash -c "wmctrl -a firefox  && xdotool key alt+1"
```

### Tasten drücken
Simuliert Tasten-Kombinationen (hot keys). Grundsätzlich werden Tasten, die gleichzeitig betätigt werden, mit einem `+` Zeichen verbunden. Trennen sie Tasten-Kombinationen mit einem `,` , wenn zusätzliche Kombinationen benötigt werden. Die Zeichenfolge `alt+F4,f` zum Beispiel bedeutet drücke und halte `alt`, gefolgt von `F4` und lass dann beide los. Drücke anschließend `f` und lass es wieder los. 

Sie können auch einen Tasten-Code im hex Format verwenden, `0x74` ist zum Beispiel der Tasten-Code für `t`. Dieser Wert wird auch manchmal als keysym bezeichnet.

> Sie können das tool `xev` verwenden um den Key-Code einer Taste zu ermitteln.
> Suchen sie in der Ausgabe nach **keysym hex value**, zum Beispiel `(keysym 0x74, t)`
>
> Verwenden sie `comma` oder `plus`, wenn sie ein `,` oder ein `+` *ausgeben* wollen.
> 
> Verwenden sie `delay <n>` um eine Verzögerung einzufügen, wobei `<n>` die Anzahl (float oder integer) der Sekunden ist. Wenn `<n>` nicht angegeben wird, wird eine Standardverzögerung von 0.5 Sekundenverwendet. Wenn `<n>` nicht als gültige Zahl erkannt wird, erfolgt keine Verzögerung.
> 

#### Beispiele
- `F11` - drückt F11. Wenn der Fokus auf einem Browser ist, schaltet das zwischen Vollbild und Normalbild hin und her.
- `alt+F4` - schließt das aktuelle Fenster.
- `ctrl+w` - schließt den aktuellen Browser-Tab.
- `cmd+left` - verkleinert das Fenster auf seine linke Hälfte. Achtung, `cmd` ist die **super** Taste (entsprechend der Windows Taste).
- `alt+plus` - drückt die  alt und die `+` Taste gleichzeitin.
- `alt+delay+F4` - drücke alt, warte dann 0.5 Sekunden, drücke dann F4. Lass beide Tasten los.
- `1,delay,delay,2,delay,delay,3` - tippe 123 mit 1-Sekunden Pausen zwischen den Tastendrucken (unter Verwendung der Standardpausen).
- `1,delay 1,2,delay 1,3` - tippe 123 mit 1-Sekunden Pausen zwischen den Tastendrucken (unter Verwendung selbst definierter Pausen).
- `e,c,h,o,space,",t,e,s,t,",enter` - tippe `echo "test"` und drücke Enter.
- `ctrl+alt+0x74` - öffnet ein neues Terminalfenster. `0x74` ist der Tasten-Code von `t`. TIP: Verwenden sie den Tasten-Code, wenn der Buchstabe nicht funktioniert.
- `0xffe5` - Caps Lock umschalten.
- `0xffaf` - Die `/` Taste im Ziffernblock der Tastatur.

Die Standardliste der Tasten finden sie [im source-code](https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key).

Die `super` Taste (Windows-Taste) kann bei einigen Linux-Versionen problematisch sein. Statt der Tastendruck-Funktion können sie dann die Befehls-Funktion wie folgt benutzen. In diesem Beispiel wollen wir die `Super` Taste und `4` drücken, was die Anwendung Nummer 4 ihrer Favoriten startet (Ubuntu).
```
xdotool key "Super_L+4"
```

### Text schreiben:
Das ist ein schneller Weg um längere Textstücke zu schreiben (Wort für Wort). Beachten sie, dass anders als in der Tastendruck-Funtion,
hier keine Spezial-(Modifikations-)Tasten akzeptiert werden. Wenn sie jedoch Enter drücken (um eine neue Zeile zu beginnen) wird auch Enter bei der Ausgabe ausgegeben.

#### Beispiele

```
Unfortunately that's a hard no.
Kind regards,
Joe
```
![nope](art/nope.gif)

## bekannte Probleme
Stellen sie sicher, dass sie die neueste Version verwenden mit `pip3 show streamdeck-ui`. Vergleichen sie es mit: [![PyPI version](https://badge.fury.io/py/streamdeck-ui.svg)](http://badge.fury.io/py/streamdeck-ui)

- Streamdeck verwendet [pynput](https://github.com/moses-palmer/pynput) zur Simulation derf **Tasten-Betätigungen** wodurch ordentliche [Unterstützung für Wayland](https://github.com/moses-palmer/pynput/issues/189) fehlt. Im Allgemeinen werden sie gute Ergebnisse bei Verwendung von X haben (Ubuntu/Linux Mint). [Dieser thread](https://github.com/timothycrosley/streamdeck-ui/issues/47) lönnte nützlich sein.
- **Taste drücken** oder **Text schreiben** funktioniert nicht unter Fedora (außerhalb von streamdeck selbst), was nicht besonders hilfreich ist. Die **Befehls-Funktion** kann aber trotzdem eine Menge.
- Version [1.0.2](https://pypi.org/project/streamdeck-ui/) hat keine Fehler-Behandlung bei der **Befehls-** und der **Taste drücken** Funktion. Deshalb müssen sie vorsichtig sein - ein ungültiger Befehl oder Tastendruck stoppt auch alle anderen Prozesse. Bitte upgraden sie zur neuesten Version.
- Einige Anwender haben berichtet, dass das Stream Deck Gerätnicht an allen USB-ports funktioniert, da es einiges an Strom verbraucht und/oder [strenge Bandbreitenanforderungen](https://github.com/timothycrosley/streamdeck-ui/issues/69#issuecomment-715887397) hat. Versuchen sie einen anderen Anschluß.
- Wenn sie einen shell script mit der Befehls-Funktion ausführen, vergessen sie nicht das shebang für die entsprechende Sprache am Anfangihrer Datei haben. `#!/bin/bash` oder `#!/usr/bin/python3` etc. Das streamdeck könnte sich andernfalls unter einigen Distros aufhängen.
