#!/bin/bash
###############################################################################
# Make sure everything is fine.
# Exit with 0 if all is ok.
###############################################################################

# Check MySQL

if ! mysql door -u door --password=door -e ";"
then
    echo "MySQL is dead"

    exit 1
else
    echo "MySQL OK"
fi

# Check door scripts

function check_script ()
{
  result=`ps aux | grep -i "$1" | grep -v "grep" | wc -l`
  if [ $result -ge 1 ]
  then
    echo "$1 OK"
  else
    echo "Script $1 is dead"

    exit 1
  fi
}

check_script "door_button_controller.py"
check_script "card_controler.py"
check_script "monitoring.py"

exit 0
