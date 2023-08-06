name = "FLApy"
import os
import vtk
os.environ['USE_PYGEOS'] = '0'

from FLApy import DataManagement, LAcalculator, LAHanalysis, Visualization
vtk.vtkObject.GlobalWarningDisplayOff()

