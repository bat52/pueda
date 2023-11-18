#!/usr/bin/env bash

# actual dependencies
sudo apt install verilator iverilog yosys gtkwave

# vcd viewer
git clone https://github.com/yne/vcd.git 
cd vcd 
make 
sudo make install

# useful stuff
sudo apt install python3-pip ipython3
