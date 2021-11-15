# Door

A set of tools to manage a door lock system.

# Requirements

* the target hardware is the couple Raspberry Py 3 + Pyface
* ID Card Reader USB 125K HZ (make sure it's one emulating keyboard but most do)
* Raspian
* the following Debian packages

```
sudo apt-get install python3 python3-pip python3-setuptools python3-mysql.connector python3-evdev monit mariadb-server
```

* the following Python3 packages

```
sudo pip3 install pifacedigitalio pifacecommon
```

# Install

## Install the scripts

```
cd /usr/local
sudo git clone https://github.com/atelierdesmedias/door.git
```

## Start the system at boot time

```
cd /etc/init.d/
ln -s /usr/local/door/usr/local/door/etc_init.d
sudo update-rc.d door defaults
```

## Use monit to make sure it stay alive

```
cd /etc/monit/conf.d/
ln -s /usr/local/door/monit door
sudo monit reload
```

# Tools

## Force open the door

```
sudo python3 /usr/local/door/open.py
```

## Force close the door

```
sudo python3 /usr/local/door/close.py
```

