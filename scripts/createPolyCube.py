#Import maya.cmds and abrevaite them to "cmds".
import maya.cmds as cmds
#Import math
from math import pow,sqrt

#create poly cube at origin and rename it cube
def cube():
    cmds.polyCube()
    cmds.rename('pCube1', 'polyCube')
 
'''
*********************************************************************
RUN DEFINITIONS
*********************************************************************
''' 
       
#run defs    
cube()