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

# bool for checkbox, camera always look at origin.
camLookAt = None

# vars for camera location
camTransX = 0
camTransY = 0
camTransZ = 0

# var for camera FOV
camFOV = 20




'''
*********************************************************************
'''


# Render
def render(*args):
    cmds.renderSettings(cam="camera_01")
    cmds.render(None)
    
# Create Lighting Setup Window
def windowLighting():
    #checks to see if window exists. if so, delete it.
    if (cmds.window("LightingWindow", q=True, exists=True) == True):
        cmds.deleteUI("LightingWindow", window=True)
  
    lightingWindow = cmds.window("LightingWindow", title="Lighting Setup", iconName='Lighting Setup', widthHeight=(400, 400), bgc=[0.5, 0.5, 0.5])
    cmds.columnLayout(adjustableColumn=True)
    
    # blank space for ui elements
    cmds.text(label="") 
    
       
# Delete Camera Window
def deleteCameraWnd(*args):
    cmds.deleteUI("CameraWindow", window=True)
    windowLighting()    


# Create Camera Setup Window
def windowCamera():
    #checks to see if window exists. if so, delete it.
    if (cmds.window("CameraWindow", q=True, exists=True) == True):
        cmds.deleteUI("CameraWindow", window=True)
        
    # make window
    window =cmds.window("CameraWindow", title="Camera Setup", iconName='Camera Setup', widthHeight=(400, 400), bgc=[0.2, 0.2, 0.2])
    cmds.columnLayout(adjustableColumn=True)

    # blank space for ui elements
    cmds.text(label="")
    
    # checkbox for camera to always look at origin
    cmds.text(label="Camera Always Face Origin (Resets Camera):")
    cmds.checkBox("cameraLookAtBool", label='', onc=cameraLookAtCB, ofc=cameraLookAtCB)
    
    # blank space for ui elements
    cmds.text(label="")

    # slider for translation of camera
    ### X
    cmds.text(label="Camera Location X: ")
    cmds.text("transXLabel", label=camTransX)
    camTransXSlider = cmds.intSlider("camTransXSlider", min=-1000, max=1000, value=0, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")

    ### Y
    cmds.text(label="Camera Location Y: ")
    cmds.text("transYLabel", label=camTransY)
    camTransYSlider = cmds.intSlider("camTransYSlider", min=-1000, max=1000, value=0, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")

    ### Z
    cmds.text(label="Camera Location Z: ")
    cmds.text("transZLabel", label=camTransZ)
    camTransZSlider = cmds.intSlider("camTransZSlider", min=-1000, max=1000, value=5, step=1, dc=queryCameraSliders)

    # blank space for ui elements
    cmds.text(label="")
    
    # Slider to control FOV
    cmds.text(label="FOV")
    cmds.text("fovLabel",label=camFOV)
    camFOVSlider = cmds.intSlider("camFOVSlider", min=5, max=120, value=20, step=1, dc=queryFOV)
    
    # blank space for ui elements
    cmds.text(label="")

    # create camera
    cmds.camera(n="camera_01", p=[cmds.intSlider(camTransXSlider, q=True, v=True), cmds.intSlider(camTransYSlider, q=True, v=True), cmds.intSlider(camTransZSlider, q=True, v=True)])
    cmds.lookThru("camera_01")
        
    #Line of text lines
    cmds.text(label="__________________________________")
    
    # blank space for ui elements
    cmds.text(label="")

    # button to move onto Lighting
    cmds.button(label=' Step #2: Lighting ', command=deleteCameraWnd, bgc=[1,1,0])

    # blank space for ui elements
    cmds.text(label="")

    # button to close the current window
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), bgc=[1,0,0])
    cmds.setParent('..')
    cmds.showWindow(window)

    return camTransXSlider, camTransYSlider, camTransZSlider
    
# Update FOV of Camera
def queryFOV(*args):
    camFOV = cmds.intSlider("camFOVSlider", q=True, v=True)
    cmds.viewPlace( "camera_01", fov=camFOV)  
    
    #update text value for fov slider
    cmds.text("fovLabel", e=True, label=camFOV)      


# Always face camera checkbox
def cameraLookAtCB(*args):
    camLookAt = cmds.checkBox("cameraLookAtBool", q=True, v=True)
   
    if camLookAt == True:
        #reset Camera
        cmds.viewPlace( "camera_01", vd=(0,0,-2), fov=20)
        #reset sliders for translations
        cmds.intSlider("camTransXSlider", e=True, v=0)
        cmds.intSlider("camTransYSlider", e=True, v=0)
        cmds.intSlider("camTransZSlider", e=True, v=0)
         
        #Camera always look at origin.
        cmds.viewPlace( "camera_01", la=(0, 0, 0) )
    else:
        #reset sliders for translations
        cmds.intSlider("camTransXSlider", e=True, v=0)
        cmds.intSlider("camTransYSlider", e=True, v=0)
        cmds.intSlider("camTransZSlider", e=True, v=0)
        
        #reset Camera
        cmds.viewPlace( "camera_01", vd=(0,0,-2), fov=20)             
         

# Query slider values for camera location
def queryCameraSliders(*args):
    #set var for translates from camera slider translations settings.
    camTransX = cmds.intSlider("camTransXSlider", q=True, v=True)
    camTransY = cmds.intSlider("camTransYSlider", q=True, v=True)
    camTransZ = cmds.intSlider("camTransZSlider", q=True, v=True)
    

    #Translate camera
    cmds.move(camTransX*0.02, camTransY*0.02, camTransZ*0.02, "camera_01", absolute=True)
    
    #check bool of always face origin for camera
    camLookAt = cmds.checkBox("cameraLookAtBool", q=True, v=True)
    if camLookAt == True:
        cmds.viewPlace( "camera_01", la=(0, 0, 0) )
        #updates off of cameraLookAtCB()
        
    #update text values of sliders
    cmds.text("transXLabel", e=True, label=camTransX)
    cmds.text("transYLabel", e=True, label=camTransY)
    cmds.text("transZLabel", e=True, label=camTransZ)
    
        
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