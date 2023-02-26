#!/usr/bin/env bash

TB_OBJ=tb.o
iverilog ./counter/verilated_dpi/tb.v -o $TB_OBJ
iverilog-vpi ./counter/verilated_dpi/verilated_vpi.c
vvp -M . -mverilated_vpi $TB_OBJ
gtkwave dump.vcd