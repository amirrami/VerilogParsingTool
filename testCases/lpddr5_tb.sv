`define VPS_FLOW
`define lpddr5_tWCKDQI_rt
`define lpddr5_tWCKDQO_rt
//    
//----------------------------------------------------------------------
//                                                                     
// Description: LPDDR5 top tb                                
//                                                                                    
//                                                                   
//----------------------------------------------------------------------
//                                                                     
// Device:      LPDDR5 Channel                                                          
// Block:       - 
// Division:    MED
// Group:       iSolve                                                 
// Designer:    
//                                                                                                                    
//----------------------------------------------------------------------
//                                                                                                                                      
// $URL:  $
// $Revision:  $
// $Date:  $
// $Author: $
//                                                                      
//----------------------------------------------------------------------


`default_nettype none
  `include "./lpddr5_channel_agt/lpddr5_agt_params_pkg.sv"

  
module lpddr5_tp #(
    ) (        
                
    );
  // pragma attribute lpddr5_tp partition_module_xrtl

  import uvm_pkg::*;
 // import lpddr5_test_pkg::*;
  
  
  wire  clk,wclk,wclk_1,wclk_2,rst_n,clk_axi,clk_apb3;
  //logic clk2x;
  wire [1:0]               WCK_rate;
  wire [DQ_WIDTH-1:0]      DQ;
  wire [DBI_WIDTH-1:0]     DMI;
  wire [STROBE_WIDTH-1:0]  RDQS_t; 
  wire [STROBE_WIDTH-1:0]  RDQS_c; 

                                           
  reg [1     :0] WCK_t,WCK_c; 
  
  wire                     wck2ck_lvl;
 `ifdef lpddr5_tWCKDQO_rt
   wire [3:0]              tWCKDQO_rt;              // run-time controllable read latency offset based on half-cycles of WCK
   reg [3:0]               tWCKDQO_rt_4;            // run-time controllable read latency offset based on half-cycles of WCK, WCK:CK=4:1
   reg [3:0]               tWCKDQO_rt_2;            // run-time controllable read latency offset based on half-cycles of WCK, WCK:CK=2:1
 `endif

  reg PCLK;
  reg PRESETn;

  wire [7:0]               PADDR;
  wire [1-1:0]             PSEL;
  wire                     PENABLE;
  wire                     PWRITE;
  wire [31:0]              PWDATA;
  wire [31:0]              PRDATA;
  wire                     PREADY;
 // wire                    PSLVERR;
 
 
 
  //--------------------------------------------------------------------
  // hardware instantiation
  //--------------------------------------------------------------------  
  lpddr5_agt_if     vif();
  lpddr5_driver_bfm v_d_bfm_if(vif);
  lpddr5_monitor_bfm v_m_bfm_if(vif);
  clock_reset cr (WCK_rate,clk,wclk,wclk_1,wclk_2,clk_axi,clk_apb3, rst_n);
  
  //assign vif.CK_t     = clk;
  //assign vif.CK_c     = (vif.CK_mode)? 'z: ~clk;
  assign vif.CK_t     = (vif.CK_off)?'z: clk;
  assign vif.CK_c     = (vif.CK_off)?'z:((vif.CK_mode)? 'z: ~clk);
  assign WCK_rate     = vif.WCK_rate;
  assign wck2ck_lvl   = vif.wck2ck_lvl; //write leveling
  

  assign vif.CK_AXI   = clk_axi;
  

  always @(posedge wclk_1)
  begin  
          vif.WCK_t=  WCK_t;		
          vif.WCK_c=  WCK_c;	
  end
 
  always @(negedge wclk_2)
  begin  
          vif.WCK_t=  WCK_t;		
          vif.WCK_c=  WCK_c;	
  end
  
  
  always @*
  begin
    if (vif.WCK_always_on)
    begin
        if (wck2ck_lvl)
        begin
            WCK_t[0] = ~wclk;
            WCK_t[1] = ~wclk;			
            WCK_c[0] = wclk;
            WCK_c[1] = wclk;			
        end 
        else
        begin
            if (vif.WCK_mode[1:0]==2'b01) //single-ended WCK_t
            begin
                WCK_t[0] = wclk;   
                WCK_c[0] = 'z;
				if (vif.WCK_1_off)begin
					WCK_t[1] = wclk;
					WCK_c[1] = 'z;
                end
                else begin
					WCK_t[1] = vif.WCK_1_value;
					WCK_c[1] = 'z;				
                end
            end
            else if (vif.WCK_mode[1:0]==2'b10) //single-ended WCK_c
            begin
                WCK_t[0] = 'z;  
                WCK_c[0] = ~wclk;
				if (vif.WCK_1_off)begin
				    WCK_t[1] = 'z;   
                    WCK_c[1] = ~wclk;	
                end
                else begin
					WCK_t[1] = 'z;
					WCK_c[1] = vif.WCK_1_value;				
                end				
            end
            else //differential
            begin
                WCK_t[0] = wclk;  
                WCK_c[0] = ~wclk;
	   			if (vif.WCK_1_off)begin
                   WCK_t[1] = wclk; 					
                   WCK_c[1] = ~wclk;	
                end
                else begin
					WCK_t[1] = ~vif.WCK_1_value;
					WCK_c[1] = vif.WCK_1_value;				
                end					
            end         
        end 
    end
    else
    begin
        if (wck2ck_lvl)
        begin
            WCK_t[0] = 1'b0;
            WCK_t[1] = 1'b0;;			
            WCK_c[0] = 1'b1;;
            WCK_c[1] = 1'b1;;			
        end 
        else
        begin
            WCK_t[0] = 'z;		
            WCK_c[0] = 'z;	
			if (vif.WCK_1_off)begin
				WCK_t[1] = 'z;
				WCK_c[1] = 'z;	
            end
            else begin
				WCK_t[1] = wclk;
				WCK_c[1] = ~wclk;				
            end				
        end 
    end
  end
  
  //assign WCK_t    = (vif.WCK_always_on ) ? (wclk)  : (wck2ck_lvl ? 0 : 'z);
  //assign WCK_c    = (vif.WCK_always_on ) ? (~wclk) : (wck2ck_lvl ? 1 : 'z);

  
  assign vif.RESET_n  = rst_n & vif.hw_rst_n;

     
`ifdef VPS_FLOW
   vps_lpddr5_sm 
`else
  veloce_lpddr5_sm
`endif  
    #(
    .DENSITY (DENSITY_CODE),
    .SERIAL_ID(SERIAL_ID),
    .DCM(DCM),
    .MANUFACT_ID(MANUFACT_ID),
    .REV_ID1(REV_ID1),
    .REV_ID2(REV_ID2),
    .tERQE(tERQE),
    .tERQX(tERQX),
  `ifndef VPS_FLOW
    .SPEED_GRADE(SPEED_GRADE),
  `endif
    .WRX_pattern (WRX_pattern ),    
    `ifndef lpddr5_tWCKDQI_rt
    .WL_offset(tWCKDQI),
    `endif  
    `ifndef lpddr5_tWCKDQO_rt   
    .RL_offset(tWCKDQO),
    `endif
    .BYTE_MODE(XMODE_CODE),
    //.BYTE_MODE_LAT_SUPPORT(XMODE_lat_CODE),
    .x8_lat_for_x16(x8_lat_for_x16),
    .tRDQS_PRE(tRDQS_PRE),
`ifdef VPS_FLOW		
    .ID(ID),
    .VERSION(VERSION),
    .UNIQUE_ID(UNIQUE_ID),
`endif 	
    .tADR(tADR)

    //.RL_RDBI_INCR(RL_RDBI_INCR)
    )
    lpddr5_top
    (
    .RESET_N    (vif.RESET_n),                 // Asynchronous reset 
    .CK_t       (vif.CK_t),                    // Clock (diff pair)
    .CK_c       (vif.CK_c),                    // ~Clock (diff pair)
     ////
    .WCK_t      (vif.WCK_t),                   // Datat Clock (diff pair)                
    .WCK_c      (vif.WCK_c),                   // ~Datat Clock (diff pair)    
    .CS         (vif.CS),                      // Chip select   
    .CA         (vif.CA),                      // Command Add

  
`ifdef VPS_FLOW                             
    .CK_t_en    (1'b1) ,
    .CK_c_en    (1'b1) ,
    .WCK_t_en   (1'b1) ,
    .WCK_c_en   (1'b1) ,
    .CLK_AXI    (vif.CK_AXI) ,	
    .pclk       (clk_apb3),
    .pclk_en    (1'b1),
    .presetn    (vif.RESET_n),
    .psel       (PSEL),
    .penable    (PENABLE),
    .pwrite     (PWRITE),
    .paddr      (PADDR),
    .pwdata     (PWDATA),
    .pready     (PREADY),
    .prdata     (PRDATA),	
`endif 

    .DQ         (DQ),                          // Data Port    
    .DMI        (DMI),                         // Data masking and Data inversion , byte based mode
    .RDQS_t     (RDQS_t),                      // Read strobe(diff pair) 
    .RDQS_c     (RDQS_c)                       // ~Read strobe(diff pair)
	

    );

`ifdef VELOCE_FLOW
     //PC checks
    assign vif.VIOLATION                   = lpddr5_top.VIOLATION;
    assign lpddr5_top.check_disable        = ~vif.check_enable; //0 ==> enable , 1 disable
    //assign lpddr5_top.TEMP           = vif.TEMP;
    assign vif.fire_group                  = lpddr5_top.lpddr5_prot_check.fire_group;
`endif 
        
    assign lpddr5_top.WCK2DQI_osc_cnt_lsb = vif.WCK2DQI_osc_cnt_lsb;
    assign lpddr5_top.WCK2DQI_osc_cnt_msb = vif.WCK2DQI_osc_cnt_msb;
    assign lpddr5_top.WCK2DQO_osc_cnt_lsb = vif.WCK2DQO_osc_cnt_lsb;
    assign lpddr5_top.WCK2DQO_osc_cnt_msb = vif.WCK2DQO_osc_cnt_msb;
    
    assign  vif.ZQ_INTERVAL = lpddr5_top.veloce_lpddr5_core.lpddr5_sm_ctrl.ZQ_INTERVAL ; 
    
    
    assign lpddr5_top.twlo                = vif.twlo;
    assign lpddr5_top.wl_zero             = vif.wl_zero;
 

    /// inout bits 
    assign  DQ[6:0]         = vif.DQ_en ? vif.dq[6:0] : 'z;
    assign  vif.DQ[6:0]     = (vif.DQ_en == 0 ) ? DQ[6:0] : vif.dq[6:0] ;  

    assign  DQ[7]         = vif.DQ_en_7 ? vif.dq[7] : 'z;
    assign  vif.DQ[7]     = (vif.DQ_en_7 == 0 ) ? DQ[7] : vif.dq[7] ;  

    assign  DMI[0]        = vif.DMI_en_0 ? vif.dmi[0] : 'z;
    assign  vif.DMI[0]    = (vif.DMI_en_0 == 0 ) ? DMI[0] : vif.dmi[0] ;    
    
`ifndef BYTE_MODE   
    assign  DQ[15:8]         = vif.DQ_en ? vif.dq[15:8]   : 'z;
    assign  vif.DQ[15:8]      = (vif.DQ_en == 0 ) ? DQ[15:8]   : vif.dq[15:8]   ;  
    assign  DMI[1]        = vif.DMI_en_1 ? vif.dmi[1] : 'z;
    assign  vif.DMI[1]    = (vif.DMI_en_1 == 0 ) ? DMI[1] : vif.dmi[1] ;    
`endif  
    assign  RDQS_t     =  vif.RDQS_en ? vif.rdqs_t : 'z ; 
    assign  vif.RDQS_t = (vif.RDQS_en == 0 ) ? RDQS_t : vif.rdqs_t ; 
    
    assign  RDQS_c      = vif.RDQS_en ? vif.rdqs_c : 'z ; 
    assign  vif.RDQS_c  = (vif.RDQS_en == 0 ) ? RDQS_c :vif.rdqs_c ; 

    
 /* initial begin 
    if ($test$plusargs("en_chk"))
       PC_en =1;
    else
       PC_en =0;  
	   	import uvm_pkg::uvm_config_db;

    uvm_config_db #(bit)::set(null, "","PC_en", PC_en);
  end*/
 


`ifdef APB3_FLOW	
  
  // Instantiation of Master module
  apb_master #(.SLAVE_COUNT(1),
               .ADDR_WIDTH(8),
               .WDATA_WIDTH(32),
               .RDATA_WIDTH(32),
               .IF_NAME("APB3_MASTER_IF"))
  master(
          .PCLK(clk_apb3),
          .PRESETn(vif.RESET_n),
          .PADDR(PADDR),
          .PSEL(PSEL),
          .PENABLE(PENABLE),
          .PWRITE(PWRITE),
          .PWDATA(PWDATA),
          .PRDATA(PRDATA),
          .PREADY(PREADY),
          .PSLVERR(),
          .PPROT(),
          .PSTRB()
        );
     
`endif 
 
//tbx vif_binding_block  
  initial begin
	import uvm_pkg::uvm_config_db;
	
    uvm_config_db #(virtual lpddr5_agt_if)::set(null, "uvm_test_top", "vif_vif", vif);
    uvm_config_db #(virtual lpddr5_driver_bfm)::set(null, "uvm_test_top", "vif_d_bfm", v_d_bfm_if);
    uvm_config_db #(virtual lpddr5_monitor_bfm)::set(null, "uvm_test_top", "vif_m_bfm",v_m_bfm_if);
    //uvm_config_db #(bit)::set(null, "","PC_en", PC_en);	  
  end
 

endmodule
