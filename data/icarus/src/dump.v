
module dump;
    initial begin
        `ifndef DUMP_FST_VPI
            `ifndef DUMP_FST
                $dumpfile("dump.vcd");
            `else
                $dumpfile("dump.fst");
            `endif
            $dumpvars(   `DUMP_LEVEL,`DUMP_MODULE);
        `else
            $fstDumpfile("dump.fst");
            $fstDumpvars(`DUMP_LEVEL,`DUMP_MODULE);
        `endif
    end
endmodule