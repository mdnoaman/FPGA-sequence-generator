//`timescale 1ns / 1ps

module rx_ser
   #( parameter clk_per_bit = 200)
    (
	 input c_rx,
 	 input rxd,
	 
	 output flag,
	 output [7:0]rx_1
    );
	 
reg r_rx;
reg rx;
reg [11:0]counter = 0;
reg i_flag;

reg [2:0] bit_index; // bit received
reg [7:0] rx_byte;  // recieved serial byte data
reg [2:0] states = 0;  // states for serial data bit

always @ (posedge c_rx)begin
r_rx <= rxd;
rx <= r_rx;
end



always @(posedge c_rx) begin
   case(states)
	3'd0: begin          // catch the rx low to start the communication 
			counter <= 0;
			bit_index <= 0;
				if(rx == 0)
					begin
					states <= 3'd1;
					end			
				else
				   begin
					states <= 3'd0;
					end
			end
	
	3'd1: begin
				if(counter == (clk_per_bit-1)/2) // checks if the rx remains low at middle of the duration
					begin
						if(rx == 0)  // checks for consistency in the rx low level
							begin
							counter <= 0;
							states <= 3'd2;
							end
						else
							begin
							states <= 3'd0;
							end
						
   				end
				
				else
					begin
					counter <= counter + 1;
					states <= 3'd1;
					end
			end	
	
	3'd2: begin              // receives all the 8 bits data and stores to rx_byte register
				if(counter == clk_per_bit-1)
					begin
					counter <= 0;
					rx_byte[bit_index] <= rx;
              				
					if(bit_index < 7)
						begin
						bit_index <= bit_index + 1;
						states <= 3'd2;
						end
					else
						begin
						states <= 3'd3;
						end
			      end
				else
					begin
					counter <= counter +1;
					states <= 3'd2;
					end

			end
		
	3'd3: begin   // closing the state machine
				if(counter < clk_per_bit-1)
					begin
						counter <= counter + 1;
						states <= 3'd3;
					end
				else
					begin
					counter <= 0;
					states <= 3'd4;
					i_flag <= 1;  // enalbles an indicator for 1 clock cycle to show that rx_byte is received
					end
			 end

	 3'd4: begin  // resets the state machine and goes back to state 0 where it waits for another rx byte
				states <= 3'd0;
				i_flag <= 0;
			 end
	endcase
end

assign rx_1 = rx_byte;
assign flag = i_flag;

endmodule
