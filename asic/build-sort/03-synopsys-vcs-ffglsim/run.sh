#=========================================================================
# 03-synopsys-vcs-ffglsim/run.sh
#=========================================================================

(
  cd $ASICDIR/03-synopsys-vcs-ffglsim

  vcs -sverilog +lint=all -xprop=tmerge -override_timescale=1ns/1ps \
      +incdir+$TOPDIR/sim/build \
      +vcs+dumpvars+SortUnitStruct__p_nbits_8_sort-rtl-struct-random_vcs.vcd \
      -top SortUnitStruct__p_nbits_8_tb \
      +delay_mode_zero \
      +define+CYCLE_TIME=0.6 \
      +define+VTB_INPUT_DELAY=0.03 \
      +define+VTB_OUTPUT_ASSERT_DELAY=0.57 \
      $TOPDIR/sim/build/SortUnitStruct__p_nbits_8_sort-rtl-struct-random_tb.v \
      $ECE6745_STDCELLS/stdcells.v \
      $ASICDIR/02-synopsys-dc-synth/post-synth.v

  ./simv

  vcd2saif -input  ./SortUnitStruct__p_nbits_8_sort-rtl-struct-random_vcs.vcd \
           -output ./SortUnitStruct__p_nbits_8_sort-rtl-struct-random.saif
)

