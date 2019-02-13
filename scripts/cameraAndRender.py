#Import maya.cmds and abrevaite them to "cmds".
import maya.cmds as cmds

#Import math
from math import pow,sqrt

#Camera creation.
def createCamera(locationX):
    cmds.camera(n="camera_01", p=[0, 0, 0])
    cmds.lookThru("camera_01")
    cmds.setAttr("camera_01.translateX", lock=True)
    cmds.setAttr("camera_01.translateY", lock=True)
    cmds.setAttr("camera_01.translateZ", lock=True)
    cmds.setAttr("camera_01.rotateX", lock=True)
    cmds.setAttr("camera_01.rotateY", lock=True)
    cmds.setAttr("camera_01.rotateZ", lock=True)
#Render
def render(*args):
    cmds.renderSettings(cam="camera_01")
    cmds.render(None)

#Create Camera Setup Window
def windowCamera(*args):
    #make window
    window = cmds.window(title="Camera Setup", iconName='Camera Setup', widthHeight=(400, 300), bgc=[0.2, 0.2, 0.2])
    cmds.columnLayout(adjustableColumn=False)

    #blank space for ui elements
    cmds.text(label="")

    #input fields for location when making camera
    ### X
    cmds.text(label="Camera Location X: ")
    locationX = cmds.textField()
    # blank space for ui elements
    cmds.text(label="")

    ### Y
    cmds.text(label="Camera Location Y: ")
    locationY = cmds.textField()
    # blank space for ui elements
    cmds.text(label="")

    ### Z
    cmds.text(label="Camera Location Z: ")
    locationZ = cmds.textField()
    # blank space for ui elements
    cmds.text(label="")

    #button to make camera
    cmds.button(label='Step #1: Create Camera', command=createCamera, bgc=[0,1,0])

    # blank space for ui elements
    cmds.text(label="")

    #button to render
    cmds.button(label='Step #2: Render', command=render, bgc=[1,1,0])

    # blank space for ui elements
    cmds.text(label="")

    #button to close the current window
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), bgc=[1,0,0])
    cmds.setParent('..')
    cmds.showWindow(window)

#Create Main Window
def windowMain():
    #create Main Window
    window = cmds.window(title="Main Window", iconName='Main', widthHeight=(400, 200), bgc=[0,0,0])
    cmds.columnLayout(adjustableColumn=False)

    #make button to open Camera Setup Window.
    cmds.button(label='Camera Setup', command=windowCamera)

    # blank space for ui elements
    cmds.text(label="")

    #button to close the Main Window
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), bgc=[1,0,0])

    cmds.setParent('..')
    cmds.showWindow(window)

'''
*********************************************************************
RUN DEFINITIONS
*********************************************************************
''' 
       
#run defs
windowMain()