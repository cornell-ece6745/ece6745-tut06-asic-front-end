#=========================================================================
# s02-synopsys-dc-synth/run.tcl
#=========================================================================

set_app_var target_library "$env(ECE6745_STDCELLS)/stdcells.db"
set_app_var link_library   "* $env(ECE6745_STDCELLS)/stdcells.db"

analyze -format sverilog $env(TOPDIR)/sim/build/SortUnitStruct__p_nbits_8__pickled.v
elaborate SortUnitStruct__p_nbits_8

create_clock clk -name ideal_clock1 -period 0.3

set_input_delay  -clock ideal_clock1 [expr 0.3*0.05] [all_inputs]
set_output_delay -clock ideal_clock1 [expr 0.3*0.05] [all_outputs]

set_max_fanout 20 SortUnitStruct__p_nbits_8
set_max_transition [expr 0.25*0.3] SortUnitStruct__p_nbits_8

check_design

compile

write -format verilog -hierarchy -output post-synth.v
write -format ddc     -hierarchy -output post-synth.ddc
write_sdc -nosplit post-synth.sdc

report_timing -nosplit -transition_time -nets -attributes

report_area -nosplit -hierarchy

report_power -nosplit -hierarchy

exit
