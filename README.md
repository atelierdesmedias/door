# Door

A set of tools to manage a door lock system.

# Requirements

* the target system is the couple Raspberry Py 3 (Raspian) + Pyface
* the following packages

```
sudo apt-get install python3 python3-pip python3-setuptools python3-pifacedigitalio python3-mysql.connector monit
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

