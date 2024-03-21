module DelayedAdder #(
    parameter N = 8
) (
    input clk,
    input reset,
    input [N-1:0] a,
    output [N-1:0] sum,
    output c
);
  reg [N-1:0] q;

  assign {c, sum} = a + q;

  always @(posedge clk or posedge reset) begin
    if (reset) begin
      q <= 0;
    end else begin
      q <= sum;
    end
  end
endmodule

module noiseCancelation #(
    parameter N = 2
) (
    input clk,
    input reset,
    input [N-1:0] i,
    input c,
    output [N:0] f
);
  reg [N-1:0] q;

  assign f = i - q + c;

  always @(posedge clk or posedge reset) begin
    if (reset) begin
      q <= 0;
    end else begin
      q <= i;
    end
  end
endmodule
