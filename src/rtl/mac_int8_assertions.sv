`timescale 1ns/1ps

module mac_int8_assertions (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic signed [19:0] acc_out
);

    property no_overflow;
        @(posedge clk) acc_out inside {[-524288:524287]};
    endproperty

    property reset_clears_acc;
        @(posedge clk) (!rst_n) |=> (acc_out == 20'sd0);
    endproperty

    property enable_gating_holds_state;
        @(posedge clk) disable iff (!rst_n) (!en) |=> (acc_out == $past(acc_out));
    endproperty

    assert property (no_overflow);
    assert property (reset_clears_acc);
    assert property (enable_gating_holds_state);

endmodule
