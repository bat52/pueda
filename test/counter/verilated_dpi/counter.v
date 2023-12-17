// https://www.geeksforgeeks.org/counter-design-using-verilog-hdl/

// Here we will learn to write a verilog HDL to design a 4 bit counter
module counter(clk,reset,up_down,load,data,count);
  //define input and output ports
  input clk,reset,load,up_down;
  input [3:0] data;
  output reg [3:0] count;
  
  //always block will be executed at each and every positive edge of the clock
  always @(posedge clk) 
  begin
    if(reset)        //Set Counter to Zero
      count <= 0;
    else if(load)    //load the counter with data value
      count <= data;
    else if(up_down) //count up
      count <= count + 1;
    else             //count down
      count <= count - 1;
  end

endmodule /* counter */