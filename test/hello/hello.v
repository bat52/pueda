module hello_tb();

initial
  begin
    $display("Hello World!");
  end

always @(*) begin
  #1
  $finish ;
end

// `include "dump.vh"

endmodule