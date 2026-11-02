// 8-bit counter used as the FP5A LibreLane smoke design.
module cnt8 (
    input  wire       clk,
    input  wire       rst,
    output reg  [7:0] q
);
    always @(posedge clk) begin
        if (rst)
            q <= 8'd0;
        else
            q <= q + 8'd1;
    end
endmodule
