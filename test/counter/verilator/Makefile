
SRC=../rtl/counter
SRC_V=${SRC}.v
TB_V=../tb/counter_tb.v
SRC_C=dut.cpp test.cpp tests.c
VERILATOR_OUT=./obj_dir

check: 
	verilator --version
	echo "WARNING: verilog testbench only works for verilator version > 5.002 "
	# https://www.reddit.com/r/FPGA/comments/14w95s2/verilator_do_i_need_to_maintain_two_testbench/

clean: check
	rm -rf ${VERILATOR_OUT}

verilate: clean
	verilator -j `nproc` --binary ${SRC_V} ${TB_V}

sim: verilate
	${VERILATOR_OUT}/Vcounter