`timescale 1ns/1ps
module systolic_array #(parameter ROWS=4, COLS=4) (
    input  logic clk, rst_n, en,
    input  logic signed [7:0] weights [ROWS-1:0][COLS-1:0],
    input  logic signed [7:0] acts_in [ROWS-1:0],
    output logic signed [19:0] results_out [COLS-1:0]
);
    logic signed [7:0] a_wire [ROWS-1:0][COLS:0];
    logic signed [19:0] s_wire [ROWS:0][COLS-1:0];
    genvar r, c;
    generate
        for (r=0; r<ROWS; r++) assign a_wire[r][0] = acts_in[r];
        for (c=0; c<COLS; c++) assign s_wire[0][c] = '0;
        for (r=0; r<ROWS; r++) begin : rows
            for (c=0; c<COLS; c++) begin : cols
                mac_int8 u_mac (.clk(clk), .rst_n(rst_n), .en(en), .weight(weights[r][c]), .act(a_wire[r][c]), .acc_out());
                always_ff @(posedge clk or negedge rst_n) begin
                    if (!rst_n) begin a_wire[r][c+1] <= '0; s_wire[r+1][c] <= '0; end
                    else if (en) begin a_wire[r][c+1] <= a_wire[r][c]; s_wire[r+1][c] <= s_wire[r][c] + (a_wire[r][c] * weights[r][c]); end
                end
            end
        end
        for (c=0; c<COLS; c++) assign results_out[c] = s_wire[ROWS][c];
    endgenerate
endmodule
