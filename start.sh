#!/usr/bin/env bash

while true; do
	./gui_setup_pumps.py  2>&1 | tee run_log_setup_pumps.log
	./gui_select_and_serve.py 2>&1 | tee run_log_select_and_serve.log
	# Giving the option to user
	zenity --question --text "Do you want to start the YouGrogg software again?"
	# Checking if user wants to proceed
	[ $? -eq 0 ] || exit 0
done

