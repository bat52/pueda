DATA=../../../data/icarus
DUMP_V=${DATA}/src/dump.v
DUMP_I=-I${DATA}/inc/
# DUMP=${DUMP_I} ${DUMP_V} --DDUMP_LEVEL=0 -DDUMP_MODULE=${DUT}

DUT=counter
SRC=../rtl/${DUT}
SRC_V=${SRC}.v
TB=counter_tb
TB_V=../tb/${TB}.v
SRC_C=dut.cpp test.cpp tests.c

DUMP=${DUMP_I} -DDUMP_EN -DDUMP_LEVEL=0 -DDUMP_MODULE=${TB} -DTRACE_DEBUG --trace --trace-structs 

VERILATOR_OUT=./obj_dir

check: 
	verilator --version
	echo "WARNING: verilog testbench only works for verilator version > 5.002 "
	# https://www.reddit.com/r/FPGA/comments/14w95s2/verilator_do_i_need_to_maintain_two_testbench/

clean: check
	rm -rf ${VERILATOR_OUT}

verilate: clean
	verilator -j `nproc` --binary ${DUMP_V} ${SRC_V} ${TB_V} ${DUMP} --top ${TB}

sim: verilate
	${VERILATOR_OUT}/V${TB}

vcd: sim
	vcd < dump.vcd | cat