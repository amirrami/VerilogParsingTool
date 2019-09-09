
`include "./lpddr5_channel_agt/lpddr5_agt_params_pkg.sv"

module addsub();

parameter data_size = 15;  //data size of module
parameter bridge = 25; // bridge for data sr

	always @ (posedge clk)
	begin
		if (add_sub)
			result <= dataa + datab;
		else
			result <= dataa - datab;
	end


MMU_gen #(
      . data_size (`DATA_SIZE),
      .Port(Num_inp),
      .head(bridge)
)
Botton(
	.load(load),
        .clk(clk)
);

MMU_gen #(
      . data_size (`DATA_SIZE),
      .CaC(number_of_calc)
)
MMU1(
	.load(load),
        .clk(clk)
);

MSO #(
      . data_size (Num_inp),
      .BRIGDE(bridge) 
)
MSoTop(
	.load(load),
        .clk(clk)
);

ASD #(
      . data_size (`DATA_SIZE),
      .HRS(333)
)
RightPort(
	.load(load),
        .clk(clk)
);




endmodule
