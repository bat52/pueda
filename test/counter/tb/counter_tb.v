
// https://www.geeksforgeeks.org/counter-design-using-verilog-hdl/

// Code your testbench here
module counter_tb;
reg clk,reset,load,ud;
reg [3:0] data;
wire [3:0] count;
// instance counter design
counter ct_1(.up_down(ud),.*);
//clock generator
initial begin clk = 1'b0; repeat(30) #3 clk= ~clk;end
//insert all the input signal
initial begin reset=1'b1;#7 reset=1'b0; #35 reset=1'b1;end
initial begin #12 load=1'b1; #5 load=1'b0;end
initial begin #5 ud=1'b1;#24 ud=1'b0;end
initial begin data=4'b1000;#14 data=4'b1101;#2 data=4'b1111;end
//monitor all the input and output ports at times when any inputs changes its state
initial begin $monitor("time=%0d,reset=%b,load=%b,ud=%b,data=%d,count=%d",
                             $time,reset,load,ud,data,count);end
// `include "dump.vh"
endmodule :counter_tb