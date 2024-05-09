#!/bin/bash

gnome-terminal --geometry=200x24 --title="TAP interface for 10.1.1.8" -- bash -c "sudo python3 code_for_receive.py; exec bash"
sleep 5
gnome-terminal --geometry=100x24 --title="Server" -- bash -c "sudo python3 server.py; exec bash"
gnome-terminal --geometry=100x24 --title="Http" -- bash -c "sudo python3 http-start.py; exec bash"