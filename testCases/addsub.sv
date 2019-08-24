module addsub();

parameter Num_inp = 256; //number of the cell_units in one row or column  Num_inp x Num_inp MMU 

parameter number_of_calc = 4; // number of matrix multiplication operation in the testbench

parameter data_size = 15;  //data size of module

parameter bridge = 25; // bridge for data science

	always @ (posedge clk)
	begin
		if (add_sub)
			result <= dataa + datab;
		else
			result <= dataa - datab;
	end



MMU_gen #(
      .tAAD(Num_inp),  //A
      .tADR(19) //A
)
Botton(
	.load(load),
        .clk(clk)
);

MMU_gen #(
      .tAAD(data_size),  //A
      .tADR(19) //A
)
Botton(
	.load(load),
        .clk(clk)
);

MMU_gen #(
	.tAAD(data_size), //A
	.tADR(18)
)
Top(
	.load(load),
        .clk(clk)
);

MMU_gen #(
	.tAAD(data_size), //A
	.tADR(18)
)
Top(
	.load(load),
        .clk(clk)
);


endmodule
