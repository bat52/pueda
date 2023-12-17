
TB=tb
TB_V=${TB}.v
TB_OBJ=${TB}.o
VPI=verilated_vpi
VPI_C=${VPI}.c
VCD=dump.vcd

DUT=counter
DUT_RTL_DIR=../rtl
DUT_VERILATED_DIR=./obj_dir

all: sim view

clean: 
	rm -rf *.o *.vpi *.vcd ${DUT_VERILATED_DIR}
	
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

verilate:
	verilator -cc ${DUT_RTL_DIR}/${DUT}.v
	make -C ${DUT_VERILATED_DIR} -f V${DUT}.mk