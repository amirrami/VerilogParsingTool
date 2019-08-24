module addsub
(
	input [7:0] dataa,
	input [7:0] datab,
	input add_sub,	  // if this is 1, add; else subtract
	input clk,
	output reg [8:0] result
);
	parameter test1 = 3'b 102;
	parameter test2 = 3'b 101; //amir
	parameter test3 = 3'b 101;

	always @ (posedge clk)
	begin
		if (add_sub)
			result <= dataa + datab;
		else
			result <= dataa - datab;
	end

endmodule
