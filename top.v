module top(
		input CLK,
		input rst,
		output TXD,
		
		input RXD,
		output [7:0]LED
		);

wire [7:0] rx_data;
wire rcvd;


clk_new clk_new
   (// Clock in ports
    .CLK_IN1(CLK),      // IN
    // Clock out ports
    .CLK_OUT1(CLK_OUT),     // OUT
    // Status and control signals
    .RESET(RESET),// IN
    .LOCKED(LOCKED));      // OUT


rx_ser serial_rx (
    .c_rx(CLK_OUT), 
    .rxd(RXD), 
    .flag(rcvd), 
    .rx_1(rx_data)
    );


reg reset;
//assign reset = 0;
reg  we;
reg  [11:0] addr;
reg  [47:0]  din;
wire [47:0] dout;

bram bram (
  .clka(CLK_OUT), // input clka
  .rsta(reset), // input rsta
  .wea(we), // input [0 : 0] wea
  .addra(addr), // input [11 : 0] addra
  .dina(din), // input [47 : 0] dina
  .douta(dout) // output [47 : 0] douta
);


reg [7:0] data;
reg [39:0] tim;
reg trig;
reg [30:0] cntr;
reg x;
reg [15:0] seq_len;
reg [15:0] lnum;
reg [7:0] lstr;
reg [7:0] lend;
reg [7:0] llen;
reg [15:0] lcnt;

reg [15:0] lnum2;
reg [7:0] lstr2;
reg [7:0] lend2;
reg [7:0] llen2;
reg [15:0] lcnt2;

reg [7:0] step;  // state machine cases
reg [7:0] ind;

always @ (posedge CLK_OUT)begin

//  if(trig ==0) 
//  begin  
	if(rcvd == 1)
	begin
	case(step)
	8'd0: begin
				if(rx_data == 8'b01110111)  // press w button to enable writing
				begin
					step <= 8'd1; 	// go to next case step
					ind <= 8'd47;
					addr <= 0;
					trig <= 0;
				end
				else if(rx_data == 8'b01110010)
				begin
					addr <= 0;
					trig <= 1;
					step <= 8'd0;
				end
				else begin
					step <= 8'd0 ;
				end
			end
	8'd1: begin
				seq_len[15:8] <= rx_data;  // receive length byte2
				step <= 8'd2;
			end
	8'd2: begin
				seq_len[7:0] <= rx_data;   // receive length byte1
				step <= 8'd3;
			end
	8'd3: begin
				lstr[7:0] <= rx_data;   // start of the loop byte
				step <= 8'd4;
			end
	8'd4: begin
				lend[7:0] <= rx_data;   // end of the loop byte
				step <= 8'd5;
			end
	8'd5: begin
				llen <= lend - lstr;    // calculates the difference between start and end loop
				lnum[15:8] <= rx_data;  // receives number of repeatations in the loop
				step <= 8'd6;
			end
	8'd6: begin
				lnum[7:0] <= rx_data;   // receives number of repeatations in the loop
				step <= 8'd7;
			end
			
	8'd7: begin
				lstr2[7:0] <= rx_data;   // start of the loop byte
				step <= 8'd8;
			end
	8'd8: begin
				lend2[7:0] <= rx_data;   // end of the loop byte
				step <= 8'd9;
			end
	8'd9: begin
				llen2 <= lend2 - lstr2;    // calculates the difference between start and end loop
				lnum2[15:8] <= rx_data;  // receives number of repeatations in the loop
				step <= 8'd10;
			end
	8'd10: begin
				lnum2[7:0] <= rx_data;   // receives number of repeatations in the loop
				step <= 8'd11;
			end


	8'd11: begin
				if(we ==1)
				begin
					we <= 0;
					addr <= addr + 1;
				end
					din[ind -:8]  <= rx_data;
					data <= din[47:40];
					ind <= ind - 8'd8;
				if(ind == 8'd7)
				begin
					we <= 1;
					ind <= 8'd47;
				end 
				if (addr == seq_len)
				begin
					 step <= 8'd12;
					 we <= 0;
					 ind <= 8'd0;
				end
			end

	8'd12: begin
					step <= 8'd0;
			end
	endcase
	end

// external trigger  
	if(rst == 0 && x == 0)   // external trigger
	begin
//     we   <= 0;  // disable write
   	  addr <= 0;
	     trig <= 1;
		  x <= 1;  // latch
	end
   
	if(rst == 1 )   // external trigger latch enables it to trigger only once when triggered
	begin
   	  x <= 0;		  
	end
//   end
   

// read out the data which was stored in the bram as 'trig' goes high  
  if(trig == 1 )    // readout data stored in bram
  begin
	data <= dout[47:40];  // data from bram (dout) is stored on the data register which is assigned to output
	cntr <= cntr + 1;   // some discripancy in while storing the data in 0th address
	tim <= dout[39:0];
	if(cntr >= tim)
	begin
		if(addr == lend)  // first loop
		begin
		cntr <= 0;
			if(lcnt < lnum)begin
			addr <= addr - llen;
			lcnt <= lcnt + 1;
			end
			else begin
			addr <= addr + 1;   // bram address increases
			cntr <= 0;
			lcnt <= 8'd0;
			end
		end

		else if(addr == lend2)  // second loop
		begin
		cntr <= 0;
			if(lcnt2 < lnum2)begin
			addr <= addr - llen2;
			lcnt2 <= lcnt2 + 1;
			end
			else begin
			addr <= addr + 1;   // bram address increases
			cntr <= 0;
			lcnt2 <= 8'd0;
			end
		end
		
		else begin
		addr <= addr + 1;   // bram address increases
		cntr <= 0;
		end
	end
	if(addr == seq_len)  // sets limit on the bram address
	begin
		trig <= 0;
	end
  end	

end


assign LED = data;
assign TXD = RXD;   // just returns all the RX data to TX for testing

endmodule
