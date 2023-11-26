
TB=tb
TB_V=${TB}.v
TB_OBJ=${TB}.o
VPI=verilated_vpi
VPI_C=${VPI}.c

clean: 
	rm -f ${TB_OBJ}
	
${TB_OBJ}: clean	
	iverilog ${TB_V} -o ${TB_OBJ}

vpi:
	iverilog-vpi ${VPI_C} # --cflags "-Wstrict-prototypes"

sim: ${TB_OBJ} vpi
	vvp -M . -m${VPI} ${TB_OBJ}

view:
	# gtkwave dump.vcd
	vcd < dump.vcd # text output

all: sim view