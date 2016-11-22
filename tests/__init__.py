import os
import sys

#  Add Gnosis module to python paths
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))
