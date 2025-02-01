#=========================================================================
# 01-synopsys-vcs-rtlsim/run.sh
#=========================================================================

(
  cd $ASICDIR/01-synopsys-vcs-rtlsim

  vcs -sverilog +lint=all -xprop=tmerge -override_timescale=1ns/1ps \
      +incdir+$TOPDIR/sim/build \
      +vcs+dumpvars+SortUnitStruct__p_nbits_8_sort-rtl-struct-random_vcs.vcd \
      -top SortUnitStruct__p_nbits_8_tb \
      $TOPDIR/sim/build/SortUnitStruct__p_nbits_8_sort-rtl-struct-random_tb.v \
      $TOPDIR/sim/build/SortUnitStruct__p_nbits_8__pickled.v

  ./simv
)

