#!/bin/bash
cd http_file/
gnome-terminal --geometry=200x24 --title="http-server for host" -- bash -c "python3 http-serv-tes.py; exec bash"