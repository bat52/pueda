#!/usr/bin/env bash

# actual dependencies
sudo apt update
sudo apt install verilator iverilog yosys gtkwave python3-pip

# python dependencies
pip3 install -r requirements.txt

# vcd viewer
git clone https://github.com/yne/vcd.git 
cd vcd 
make 
sudo make install

# useful stuff
sudo apt install ipython3
