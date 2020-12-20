#!/bin/sh
#replace YOUR_USERNAME with your linux user name
#place this script in /usr/lib/systemd/system-sleep/
#make it executable with chmod+x restart_streamdeck_wakeup.sh
#systemd automatically execute it at wake-up

case "$1" in
    post)
    runuser -l YOUR_USERNAME -c 'killall -u YOUR_USERNAME streamdeck && export DISPLAY=:0 && (/usr/bin/streamdeck &)'
        ;;
esac
