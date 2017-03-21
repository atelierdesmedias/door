#!/bin/bash
###############################################################################
# Make sure everything is fine.
# Exit with 0 if all is ok.
###############################################################################

function check_script ()
{
  result=`ps aux | grep -i "$1" | grep -v "grep" | wc -l`
  if [ $result -ge 1 ]
  then
    exit 0
  else
    echo "Script $1 is dead"

    exit 1
  fi
}

check_script "door_button_controller.py"
check_script "card_controler.py"
check_script "monitoring.py"
