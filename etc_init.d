#! /bin/sh
### BEGIN INIT INFO
# Provides:          door
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO


case "$1" in
    start)
	echo "Starting door system "
	/usr/local/door/start.sh
	;;
    stop)
	echo "Stopping door system"
	/usr/local/door/stop.sh
	;;
    restart)
	/usr/local/door/stop.sh
	/usr/local/door/start.sh
	;;

    *)
	echo "Usage: /etc/init.d/blah {start|stop}"
	exit 1
	;;
esac

exit 0
