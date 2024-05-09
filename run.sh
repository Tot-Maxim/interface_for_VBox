#!/bin/bash

gnome-terminal --geometry=200x24 --title="Code for recevie" -- bash -c "sudo python3 code_for_receive.py; exec bash"
sleep 2
gnome-terminal --geometry=100x24 --title="Server" -- bash -c "sudo python3 server.py; exec bash"