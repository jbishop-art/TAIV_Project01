# Import maya.cmds and abrevaite them to "cmds".
import maya.cmds as cmds
from functools import partial

# Import math
from math import pow,sqrt

'''
*********************************************************************
GLOBAL VARS
*********************************************************************
'''
# vars for camera translate sliders
camTransXSlider = None
#, camTransYSlider, camTransZSlider =

# vars for camera location
camTransX = 0
camTransY = 0
camTransZ = 0

'''
*********************************************************************
'''


# Render
def render(*args):
    cmds.renderSettings(cam="camera_01")
    cmds.render(None)


# Create Camera Setup Window
def windowCamera():

    # make window
    window = cmds.window(title="Camera Setup", iconName='Camera Setup', widthHeight=(400, 300), bgc=[0.2, 0.2, 0.2])
    cmds.columnLayout(adjustableColumn=False)

    # blank space for ui elements
    cmds.text(label="")

    # slider for translation of camera
    ### X
    cmds.text(label="Camera Location X: ")
    camTransXSlider = cmds.intSlider("camTransXSlider", min=-1000, max=1000, value=0, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")

    ### Y
    cmds.text(label="Camera Location Y: ")
    camTransYSlider = cmds.intSlider("camTransYSlider", min=-1000, max=1000, value=0, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")

    ### Z
    cmds.text(label="Camera Location Z: ")
    camTransZSlider = cmds.intSlider("camTransZSlider", min=-1000, max=1000, value=5, step=1, dc=queryCameraSliders)

    # blank space for ui elements
    cmds.text(label="")



    # create camera
    cmds.camera(n="camera_01", p=[cmds.intSlider(camTransXSlider, q=True, v=True), cmds.intSlider(camTransYSlider, q=True, v=True), cmds.intSlider(camTransZSlider, q=True, v=True)])
    cmds.lookThru("camera_01")

    # button to render
    cmds.button(label='Step #2: Render', command=render, bgc=[1,1,0])

    # blank space for ui elements
    cmds.text(label="")

    # button to close the current window
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), bgc=[1,0,0])
    cmds.setParent('..')
    cmds.showWindow(window)

    return camTransXSlider, camTransYSlider, camTransZSlider

# Query slider values for camera location
def queryCameraSliders(*args):
    camTransX = cmds.intSlider("camTransXSlider", q=True, v=True)
    camTransY = cmds.intSlider("camTransYSlider", q=True, v=True)
    camTransZ = cmds.intSlider("camTransZSlider", q=True, v=True)

    #Translate camera
    cmds.move(camTransX*0.01, camTransY*0.01, camTransZ*0.01, "camera_01", absolute=True)

# Delete Main Window
def deleteMain(*args):
    cmds.deleteUI("MainWindow", window=True)
    windowCamera()

# Create Main Window
def windowMain(*args):
    # create Main Window
    mainWindow = cmds.window("MainWindow", title="Main Window", iconName='Main', widthHeight=(400, 200), bgc=[0,0,0])
    cmds.columnLayout(adjustableColumn=False)

    # make button to open Camera Setup Window.
    cmds.button(label='Camera Setup', command=deleteMain)

    # blank space for ui elements
    cmds.text(label="")

    cmds.setParent('..')
    cmds.showWindow(mainWindow)

'''
*********************************************************************
RUN DEFINITIONS
*********************************************************************
'''

# run defs
windowMain()