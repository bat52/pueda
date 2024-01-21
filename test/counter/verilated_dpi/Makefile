
TB=tb
TB_V=${TB}.v
TB_OBJ=${TB}.o
# VPI=verilated_vpi
VPI=verilated_vpi_dut
VPI_C=${VPI}.c
VCD=dump.vcd

DUT=counter
DUT_RTL_DIR=../rtl
DUT_VERILATED_DIR=./obj_dir

# Path to Verilator kit (from $VERILATOR_ROOT)
VERILATOR_ROOT = /usr/local/share/verilator
include $(VERILATOR_ROOT)/include/verilated.mk

all: sim view

clean: 
	rm -rf *.o *.vpi *.vcd ${DUT_VERILATED_DIR}
	
tb:
	iverilog ${TB_V} -o ${TB_OBJ}

vpi: # verilate
	iverilog-vpi -I ${VERILATOR_ROOT}/include ${VPI_C}

sim: clean tb vpi
	vvp -M . -m${VPI} ${TB_OBJ}

view:
	# gtkwave ${VCD}
	vcd < ${VCD} # text output

verilate:
	verilator -cc ${DUT_RTL_DIR}/${DUT}.v --clk clk
	make -C ${DUT_VERILATED_DIR} -f V${DUT}.mk