`timescale 1ns/1ps
module mac_int8 (
    input  logic clk, rst_n, en,
    input  logic signed [7:0] weight, act,
    output logic signed [19:0] acc_out
);
    logic signed [19:0] acc_reg;
    
    // --- CYCLOPS-RTL OPTIMIZATION ---
    // Clock Gating: Stop clock toggling when enable is low to save dynamic power
    logic clk_gated;
    assign clk_gated = clk & en;
    // --------------------------------

    always_ff @(posedge clk_gated or negedge rst_n) begin
        if (!rst_n) acc_reg <= '0;
        else if (en) acc_reg <= acc_reg + (weight * act);
    end
    assign acc_out = acc_reg;
endmodule
