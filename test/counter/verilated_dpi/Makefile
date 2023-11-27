
TB=tb
TB_V=${TB}.v
TB_OBJ=${TB}.o
VPI=verilated_vpi
VPI_C=${VPI}.c
VCD=dump.vcd
DUT=counter.v

all: sim view

clean: 
	rm -rf *.o *.vpi *.vcd ./obj_dir/*
	
tb:
	iverilog ${TB_V} -o ${TB_OBJ}

vpi:
	iverilog-vpi ${VPI_C}

verilate:
	verilator --cc ${DUT} --clk clk

sim: clean tb vpi
	vvp -M . -m${VPI} ${TB_OBJ}

view:
	# gtkwave ${VCD}
	vcd < ${VCD} # text output
