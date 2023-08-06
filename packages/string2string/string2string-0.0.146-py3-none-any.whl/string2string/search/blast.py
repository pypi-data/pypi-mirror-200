"""
    This module contains different BLAST algorithms. The following algorithms are available:
        (a) QuickBLASTP is an accelerated version of BLASTP that is very fast and works best if the target percent identity is 50% or more.
        (b) BlastP simply compares a protein query to a protein database.
        (c) PSI-BLAST allows the user to build a PSSM (position-specific scoring matrix) using the results of the first BlastP run.
        (d) PHI-BLAST performs the search but limits alignments to those that match a pattern in the query.
        (e) DELTA-BLAST constructs a PSSM using the results of a Conserved Domain Database search and searches a sequence database.

    The following classes are available:
        (a) QuickBlastP
        (b) BlastP
        (c) PSIBlast
        (d) PHIBlast
        (e) DeltaBlast
"""

from typing import Union, List, Tuple, Optional
import numpy as np
import pandas as pd
import os


# Define a parent class for the BLAST algorithms
class BLAST:
    def __init__(self):
        pass

    
