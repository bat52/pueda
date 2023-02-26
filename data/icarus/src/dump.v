
module dump;
    initial begin
        `ifndef DUMP_FST_VPI
            $dumpfile("dump.vcd");            
            $dumpvars(   `DUMP_LEVEL,`DUMP_MODULE);
        `else
            $fstDumpfile("dump.fst");
            $fstDumpvars(`DUMP_LEVEL,`DUMP_MODULE);
        `endif
    end
endmodule