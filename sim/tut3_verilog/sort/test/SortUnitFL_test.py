#=========================================================================
# SortUnitFL_test
#=========================================================================

import pytest
from copy       import deepcopy
from random     import randint, seed

from pymtl3 import *
from pymtl3.stdlib.test_utils import run_test_vector_sim, mk_test_case_table
from tut3_verilog.sort.SortUnitFL import SortUnitFL

#-------------------------------------------------------------------------
# test vectors
#-------------------------------------------------------------------------

tvec_stream = [ [ 4, 3, 2, 1 ], [ 9, 6, 7, 1 ], [ 4, 8, 0, 9 ] ]
tvec_dups   = [ [ 2, 8, 9, 9 ], [ 2, 8, 2, 8 ], [ 1, 1, 1, 1 ] ]
tvec_sorted = [ [ 1, 2, 3, 4 ], [ 1, 3, 5, 7 ], [ 4, 3, 2, 1 ] ]

# To ensure reproducible testing

seed(0xdeadbeef)
tvec_random = [ [ randint(0,0xff) for _ in range(4) ] for _ in range(20) ]

#-------------------------------------------------------------------------
# Syntax helpers
#-------------------------------------------------------------------------

# We define the header string here since it is so long. Then reference
# the header string and include a comment to label each of the columns.

header_str = \
  ( "in_val",   "in_[0]",  "in_[1]",  "in_[2]",  "in_[3]",
    "out_val*", "out[0]*", "out[1]*", "out[2]*", "out[3]*" )

# We define a global variable 'x' so that we can simply use the x
# character instead of '?' to indicate don't care reference outputs

x = '?'

#-------------------------------------------------------------------------
# mk_test_vector_table
#-------------------------------------------------------------------------

def mk_test_vector_table( nstages, inputs ):

  # Add initial invalid outputs to the list of output values

  outputs_val = [[0,x,x,x,x]]*nstages

  # Sort inputs and prepend valid bit to each list of inputs/outputs

  inputs_val  = []
  for input_ in inputs:
    inputs_val.append( [1] + input_ )
    outputs_val.append( [1] + deepcopy( sorted(input_) ) )

  # Add final invalid inputs to the list of input values

  inputs_val.extend( [[0,0,0,0,0]]*nstages )

  # Put inputs_val and outputs_val together to make test_vector_table

  test_vector_table = [ header_str ]
  for input_,output in zip( inputs_val, outputs_val ):
    test_vector_table.append( input_ + output )

  return test_vector_table

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

def test_basic():
  run_test_vector_sim( SortUnitFL(), [ header_str,
    # in  in  in  in  in  out out out out out
    # val [0] [1] [2] [3] val [0] [1] [2] [3]
    [ 0,  0,  0,  0,  0,  0,  x,  x,  x,  x ],
    [ 1,  4,  2,  3,  1,  0,  x,  x,  x,  x ],
    [ 0,  0,  0,  0,  0,  1,  1,  2,  3,  4 ],
    [ 0,  0,  0,  0,  0,  0,  x,  x,  x,  x ],
  ] )

#-------------------------------------------------------------------------
# Parameterized Testing with Test Case Table
#-------------------------------------------------------------------------
# Note: FL is always 1-stage!

test_case_table = mk_test_case_table([
  (                 "nstages inputs      "),
  [ "1stage_stream", 1,      tvec_stream  ],
  [ "1stage_dups",   1,      tvec_dups    ],
  [ "1stage_sorted", 1,      tvec_sorted  ],
  [ "1stage_random", 1,      tvec_random  ],
  [ "2stage_stream", 2,      tvec_stream  ],
  [ "2stage_dups",   2,      tvec_dups    ],
  [ "2stage_sorted", 2,      tvec_sorted  ],
  [ "2stage_random", 2,      tvec_random  ],
  [ "3stage_stream", 3,      tvec_stream  ],
  [ "3stage_dups",   3,      tvec_dups    ],
  [ "3stage_sorted", 3,      tvec_sorted  ],
  [ "3stage_random", 3,      tvec_random  ],
])

@pytest.mark.parametrize( **test_case_table )
def test_sort_fl( test_params ):
  nstages = test_params.nstages
  inputs  = test_params.inputs
  run_test_vector_sim( SortUnitFL(), mk_test_vector_table( 1, inputs ) )

#-------------------------------------------------------------------------
# Parameterized Testing of With nstages = [ 1, 2, 3, 4, 5, 6 ]
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "n", [ 1, 2, 3, 4, 5, 6 ] )
def test_sort_fl_random( n ):
  run_test_vector_sim( SortUnitFL(), mk_test_vector_table( 1, tvec_random ) )
