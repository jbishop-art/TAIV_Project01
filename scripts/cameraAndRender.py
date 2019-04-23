#||||||||||||||||||||||||||||||||||
'''
Render assistant tool for Maya.
--allows the user to set up a camera and lighting easily.
--Save/Load settings for camera and lights.
--Easy to use buttons to drive windows for render settings and test render window.
--Render a single frame or a sequence.

Future Work:
--Sprite sheet automation output.
--Add more lighting options and more light functionality.
--Import/Export camera and lights as FBX.

'''

# Import maya.cmds and abrevaite them to "cmds".
import maya.cmds as cmds
from functools import partial

# Import functionality to use Mel specific commands within Python.
import maya.mel as mel

# Import math
from math import pow,sqrt

# Import os functionality to be able to read & write files and navigate windows structure.
import os

# Import JSON functionality.
import json

'''
*********************************************************************
GLOBAL VARS
*********************************************************************
'''

# vars for camera translate sliders
camTransXSlider = None
camTransYSlider = None
camTransZSlider = None

# bool for checkbox, camera always look at origin.
camLookAt = None

# vars for camera location
camTransX = 0
camTransY = 0
camTransZ = 0

# var for camera FOV
camFOV = 20

# vars for spot light location
spotLightX = 0
spotLightY = 0
spotLightZ = 0

# vars for spot light intensity
spotLightInt = 0

# vars for spot light color
spotLightColR = 0
spotLightColG = 0
spotLightColB = 0

# vars for spot light cone angle
spotLightCone = 0

# vars for spot light dropoff
spotLightDropoff = 0

# vars for ambient light intensity
ambLInt = 0

# vars for ambient light color
ambLColR = 0
ambLColG = 0
ambLColB = 0

# var for directional light rotation
dirLRotX = 0
dirLRotY = 0
    
# var for directional light intensity   
dirLInt = 0

# var for directional light color
dirLColR = 0
dirLColG = 0
dirLColB = 0

#------------------Read/Wrtie Vars -----------------#

path = cmds.internalVar(userWorkspaceDir=True)

cameraSettingsFileName = 'cameraSettings - JSON'
cameraSettings = {}

lightSettingsFileName = 'lightSettings - JSON'
lightSettings = {}

'''
*********************************************************************
'''

############ -Read & Write Files- ####################

# Write JSON to file.
def writeSettings(path, fileName, data):
    filePathNameWExt = path + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

# Load settings.
def loadSettings(path, fileName):
    with open(path + '/' + fileName + '.json', 'r') as fp:
        return json.load(fp)

# ____________________Camera_______________________________

# Execute JSON write after populating list with vars of settings.
def executeWriteCameraSettings(*args):
    # update all vars associated with Camera
    camTransXSlider = cmds.intSlider("camTransXSlider", q=True, v=True)
    camTransYSlider = cmds.intSlider("camTransYSlider", q=True, v=True)
    camTransZSlider = cmds.intSlider("camTransZSlider", q=True, v=True)
    camLookAt = cmds.checkBox("cameraLookAtBool", q=True, v=True)
    camTransX = cmds.intSlider("camTransXSlider", q=True, v=True)
    camTransY = cmds.intSlider("camTransYSlider", q=True, v=True)
    camTransZ = cmds.intSlider("camTransZSlider", q=True, v=True)
    camFOV = cmds.intSlider("camFOVSlider", q=True, v=True)

    # clear list
    cameraSettings = {}

    # populate cameraSettings {}
    cameraSettings['camTransXSlider'] = camTransXSlider
    cameraSettings['camTransYSlider'] = camTransYSlider
    cameraSettings['camTransZSlider'] = camTransZSlider
    cameraSettings['camLookAt'] = camLookAt
    cameraSettings['camTransX'] = camTransX
    cameraSettings['camTransY'] = camTransY
    cameraSettings['camTransZ'] = camTransZ
    cameraSettings['camFOV'] = camFOV
    writeSettings(path, cameraSettingsFileName, cameraSettings)

# Load camera settings.
def loadCameraSettings(*args):
    #intialize camDic
    camDic = ''

    #load setting strings into camDic
    camDic = loadSettings(path, cameraSettingsFileName)

    # populate cameraSettings {}
    camTransXSlider = camDic.get("camTransXSlider", "")
    camTransYSlider = camDic.get("camTransYSlider", "")
    camTransZSlider = camDic.get("camTransZSlider", "")
    camLookAt = camDic.get("camLookAt", "")
    camTransX = camDic.get("camTransX", "")
    camTransY = camDic.get("camTransY", "")
    camTransZ = camDic.get("camTransZ", "")
    camFOV = camDic.get("camFOV", "")

    cmds.checkBox("cameraLookAtBool", e=True, v=camLookAt)
    cmds.text("transXLabel", e=True, label=camTransX)
    cmds.intSlider("camTransXSlider", e=True, v=camTransXSlider)
    cmds.text("transYLabel", e=True, label=camTransY)
    cmds.intSlider("camTransYSlider", e=True, v=camTransYSlider)
    cmds.text("transZLabel", e=True, label=camTransZ)
    cmds.intSlider("camTransZSlider", e=True, v=camTransZSlider)
    cmds.intSlider("camFOVSlider", e=True, v=camFOV)

    # set camera to loaded settings
    queryFOV()
    queryCameraSliders()

# ________________________Lights________________________________

# Execute JSON write after populating list with vars of settings.
def executeWriteLightSettings(*args):
    # update all vars associated with Lighting
    ambLightBool = cmds.checkBox("ambientLightBool", q=True, v=True)
    dirLightBool = cmds.checkBox("dirLightBool", q=True, v=True)
    spotLightBool = cmds.checkBox("spotLightBool", q=True, v=True)
    spotLightX = cmds.intSlider("spotLightSliderX", q=True, v=True)
    spotLightY = cmds.intSlider("spotLightSliderY", q=True, v=True)
    spotLightZ = cmds.intSlider("spotLightSliderZ", q=True, v=True)
    spotLightInt = cmds.intSlider("spotLightIntSlider", q=True, v=True)
    spotLightColR = cmds.intSlider("spotLightColRSlider", q=True, v=True)
    spotLightColG = cmds.intSlider("spotLightColGSlider", q=True, v=True)
    spotLightColB = cmds.intSlider("spotLightColBSlider", q=True, v=True)
    spotLightCone = cmds.intSlider("spotLightConeSlider", q=True, v=True)
    spotLightDropoff = cmds.intSlider("spotLightDropoffSlider", q=True, v=True)
    ambLInt = cmds.intSlider("ambLightIntSlider", q=True, v=True)
    ambLColR = cmds.intSlider("ambLightColRSlider", q=True, v=True)
    ambLColG = cmds.intSlider("ambLightColGSlider", q=True, v=True)
    ambLColB = cmds.intSlider("ambLightColBSlider", q=True, v=True)
    dirLRotX = cmds.intSlider("dirLightRotXSlider", q=True, v=True)
    dirLRotY = cmds.intSlider("dirLightRotYSlider", q=True, v=True)
    dirLInt = cmds.intSlider("dirLightIntSlider", q=True, v=True)
    dirLColR = cmds.intSlider("dirLightColRSlider", q=True, v=True)
    dirLColG = cmds.intSlider("dirLightColGSlider", q=True, v=True)
    dirLColB = cmds.intSlider("dirLightColBSlider", q=True, v=True)

    # clear list
    lightSettings = {}

    # populate lightSettings {}
    lightSettings['ambLightBool'] = ambLightBool
    lightSettings['dirLightBool'] = dirLightBool
    lightSettings['spotLightBool'] = spotLightBool
    lightSettings['spotLightX'] = spotLightX
    lightSettings['spotLightY'] = spotLightY
    lightSettings['spotLightZ'] = spotLightZ
    lightSettings['spotLightInt'] = spotLightInt
    lightSettings['spotLightColR'] = spotLightColR
    lightSettings['spotLightColG'] = spotLightColG
    lightSettings['spotLightColB'] = spotLightColB
    lightSettings['spotLightCone'] = spotLightCone
    lightSettings['spotLightDropoff'] = spotLightDropoff
    lightSettings['ambLInt'] = ambLInt
    lightSettings['ambLColR'] = ambLColR
    lightSettings['ambLColG'] = ambLColG
    lightSettings['ambLColB'] = ambLColB
    lightSettings['dirLRotX'] = dirLRotX
    lightSettings['dirLRotY'] = dirLRotY
    lightSettings['dirLInt'] = dirLInt
    lightSettings['dirLColR'] = dirLColR
    lightSettings['dirLColG'] = dirLColG
    lightSettings['dirLColB'] = dirLColB
    writeSettings(path, lightSettingsFileName, lightSettings)

# Load camera settings.
def loadLightSettings(*args):

    # intialize lightDic
    lightDic = ''

    # load setting strings into lightDic
    lightDic = loadSettings(path, lightSettingsFileName)

    # populate lightSettings {}
    ambLightBool = lightDic.get("ambLightBool")
    dirLightBool = lightDic.get("dirLightBool")
    spotLightBool = lightDic.get("spotLightBool")
    spotLightX = lightDic.get("spotLightX", "")
    spotLightY = lightDic.get("spotLightY", "")
    spotLightZ = lightDic.get("spotLightZ", "")
    spotLightInt = lightDic.get("spotLightInt", "")
    spotLightColR = lightDic.get("spotLightColR", "")
    spotLightColG = lightDic.get("spotLightColG", "")
    spotLightColB = lightDic.get("spotLightColB", "")
    spotLightCone = lightDic.get("spotLightCone", "")
    spotLightDropoff = lightDic.get("spotLightDropoff", "")
    ambLInt = lightDic.get("ambLInt", "")
    ambLColR = lightDic.get("ambLColR", "")
    ambLColG = lightDic.get("ambLColG", "")
    ambLColB = lightDic.get("ambLColB", "")
    dirLRotX = lightDic.get("dirLRotX", "")
    dirLRotY = lightDic.get("dirLRotY", "")
    dirLInt = lightDic.get("dirLInt", "")
    dirLColR = lightDic.get("dirLColR", "")
    dirLColG = lightDic.get("dirLColG", "")
    dirLColB = lightDic.get("dirLColB", "")

    # set light to loaded settings
    cmds.checkBox("ambientLightBool", e=True, v=ambLightBool)
    if ambLightBool == True:
        createAmbientLight()
    else:
        delAmbientLight()
    cmds.checkBox("dirLightBool", e=True, v=dirLightBool)
    if dirLightBool == True:
        createDirLight()
    else:
        delDirLight()
    cmds.checkBox("spotLightBool", e=True, v=spotLightBool)
    if spotLightBool == True:
        createSpotLight()
    else:
        deleteSpotLight()
    cmds.intSlider("spotLightSliderX", e=True, v=spotLightX)
    cmds.intSlider("spotLightSliderY", e=True, v=spotLightY)
    cmds.intSlider("spotLightSliderZ", e=True, v=spotLightZ)
    cmds.intSlider("spotLightIntSlider", e=True, v=spotLightInt)
    cmds.intSlider("spotLightColRSlider", e=True, v=spotLightColR)
    cmds.intSlider("spotLightColGSlider", e=True, v=spotLightColG)
    cmds.intSlider("spotLightColBSlider", e=True, v=spotLightColB)
    cmds.intSlider("spotLightConeSlider", e=True, v=spotLightCone)
    cmds.intSlider("spotLightDropoffSlider", e=True, v=spotLightDropoff)
    cmds.intSlider("ambLightIntSlider", e=True, v=ambLInt)
    cmds.intSlider("ambLightColRSlider", e=True, v=ambLColR)
    cmds.intSlider("ambLightColGSlider", e=True, v=ambLColG)
    cmds.intSlider("ambLightColBSlider", e=True, v=ambLColB)
    cmds.intSlider("dirLightRotXSlider", e=True, v=dirLRotX)
    cmds.intSlider("dirLightRotYSlider", e=True, v=dirLRotY)
    cmds.intSlider("dirLightIntSlider", e=True, v=dirLInt)
    cmds.intSlider("dirLightColRSlider", e=True, v=dirLColR)
    cmds.intSlider("dirLightColGSlider", e=True, v=dirLColG)
    cmds.intSlider("dirLightColBSlider", e=True, v=dirLColB)

    # set lights to loaded settings
    queryDirLightSlider()
    queryAmbLightSliders()
    querySpotLightSliders()

#####################################################

# render based on current render settings a SINGLE frame
def renderFrame(*args):
    cmds.render()
    
# render based on current render settings a SEQUENCE
def renderSeq(*args):
    mel.eval('RenderSequence')

# open render settings window.
def renderSettingsWindow(*args):
    mel.eval('unifiedRenderGlobalsWindow')
    
# open the IPR window to see a test render.
def testRenderWindow(*args):
    mel.eval('IPRRenderIntoNewWindow')
       
# delete Render Window
def deleteRenderWnd(*args):
    cmds.deleteUI("RenderWindow", window=True)
    
# delete the Render Window and create the lighting window.  Go Back.
def goBackRenderWindow(*args):
    # delete the Render Window.
    deleteRenderWnd()
    
    # create the Lighting Window()
    windowLighting()
      
# ********************Create Render Window**********************
def windowRender(*args):
    # checks to see if window exists. if so, delete it.
    if (cmds.window("RenderWindow", q=True, exists=True) == True):
        cmds.deleteUI("RenderWindow", window=True)     

    # create window
    renderWindow = cmds.window("RenderWindow", title="Render Setup", iconName='Render Setup', bgc=[0.2, 0.2, 0.2], sizeable=False)
    cmds.rowColumnLayout( numberOfColumns=2 )

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #___________________________________________________________________________
    
    #________________________RENDER SETTINGS____________________________________
    # Open the render settings window to allow the user to chose how they want to render the scene.
    cmds.button(label='Render Settings', command=renderSettingsWindow, bgc=[0.3,0.3,0.3])
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #_________________________TEST RENDER_________________________________________
    
    # perform a test render of the current scene
    cmds.button(label='Test Render',command=testRenderWindow, bgc=[0.3,0.3,0.3])
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #____________________________RENDER SINGLE FRAME_____________________________________________
    
    # button to Render the current scene
    cmds.button(label='RENDER FRAME', command=renderFrame, bgc=[0.3,0.3,0.3])
    # blank space for ui elements
    cmds.text(label="")
    
    #____________________________RENDER SEQUENCE_____________________________________________
    
    # button to Render the current scene
    cmds.button(label='RENDER SEQUENCE', command=renderSeq, bgc=[0.3,0.3,0.3])
    # blank space for ui elements
    cmds.text(label="")
    
    #_______________________GO BACK BUTTON________________________________________________
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # button go back to previous window
    cmds.button(label=' Go Back. ', command=goBackRenderWindow, bgc=[0.3,0.3,0.3])
    # blank space for ui elements
    cmds.text(label="") 
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #_________________________CLOSE BUTTON__________________________________________________

    # button to close the current window
    cmds.button(label='Close', command=deleteRenderWnd, bgc=[0.3,0.3,0.3])
    cmds.setParent('..')
    
    # Force show window
    cmds.showWindow(renderWindow)
    
    # Force resize the window
    cmds.window( renderWindow, edit=True, widthHeight=(115, 215), tlc=[0,0], sizeable=False )

# create ambient light
def createAmbientLight(*args):
    # Create an ambientLight light
    light = cmds.ambientLight(name="Ambient Light", intensity=0.8)

    # Change the light intensity
    cmds.ambientLight( light, e=True, intensity=0.5 )
    
# delete ambient light
def delAmbientLight(*args):
    cmds.delete('Ambient_Light')
    
# create directional light
def createDirLight(*args):
    dirLight = cmds.directionalLight(name="Directional Light", rotation=(45,30,15), intensity=0.5)
    
# delete directional light
def delDirLight(*args):
    cmds.delete('Directional_Light')       
    
# create spot light
def createSpotLight(*args):
    # Create a spot light
    light = cmds.spotLight(n='spotlight_01', coneAngle=45)
    
    # Change the cone angle value
    cmds.spotLight( light, e=True, coneAngle=33 )

    # create camera to tie spot light to
    cmds.camera(n='spotlightAnchor_01')
    
    #set lookthrough to Main Camera, "camera_01."
    cmds.lookThru('camera_01')

    # contrain spotlight to camera anchor
    cmds.parent('spotlight_01', 'spotlightAnchor_01')
    
# delete spot light
def deleteSpotLight(*args):
    # Delete directional Light
    cmds.delete('spotlight_01')
    cmds.delete('spotlightAnchor_01')
        
# Query slider values for spot light location
def querySpotLightSliders(*args):
    # set var for translates from spotlight Anchor slider translations settings.
    spotLightX = cmds.intSlider("spotLightSliderX", q=True, v=True)
    spotLightY = cmds.intSlider("spotLightSliderY", q=True, v=True)
    spotLightZ = cmds.intSlider("spotLightSliderZ", q=True, v=True)
    
    # set vars for spot light intensity
    spotLightInt = cmds.intSlider("spotLightIntSlider", q=True, v=True)

    # set vars for spot light color
    spotLightColR = cmds.intSlider("spotLightColRSlider", q=True, v=True)
    spotLightColG = cmds.intSlider("spotLightColGSlider", q=True, v=True)
    spotLightColB = cmds.intSlider("spotLightColBSlider", q=True, v=True)

    # set vars for spot light cone angle
    spotLightCone = cmds.intSlider("spotLightConeSlider", q=True, v=True)
    
    # set vars for spot light dropoff
    spotLightDropoff = cmds.intSlider("spotLightDropoffSlider", q=True, v=True)

    # set Translate spotLight anchor
    cmds.move(spotLightX*0.02, spotLightY*0.02, spotLightZ*0.02, "spotlightAnchor_01", absolute=True)
    
    # update the spot light attributes per slider update
    cmds.spotLight("spotlight_01", e=True, i=(spotLightInt * 0.1), rgb=[spotLightColR * 0.01, spotLightColG * 0.01, spotLightColB * 0.01], ca=spotLightCone, do=spotLightDropoff)

    # always have spotlight anchor look at center
    cmds.viewPlace('spotlightAnchor_01', la=(0,0,0))
    
# Query slider values for ambient light intensity and color
def queryAmbLightSliders(*args):
    # set var for values from globals
    ambLInt = cmds.intSlider("ambLightIntSlider", q=True, v=True)
    ambLColR = cmds.intSlider("ambLightColRSlider", q=True, v=True)
    ambLColG = cmds.intSlider("ambLightColGSlider", q=True, v=True)
    ambLColB = cmds.intSlider("ambLightColBSlider", q=True, v=True)
    
    # change color of ambient light base on slider values
    cmds.ambientLight('Ambient_Light', e=True, i=(ambLInt * 0.1), rgb=[ambLColR *0.01, ambLColG *0.01, ambLColB *0.01])
    
# Query slider values for directional light rotation, intensity and color
def queryDirLightSlider(*args):
    # set var for values from globals    
    dirLRotX = cmds.intSlider("dirLightRotXSlider", q=True, v=True)
    dirLRotY = cmds.intSlider("dirLightRotYSlider", q=True, v=True)
    dirLInt = cmds.intSlider("dirLightIntSlider", q=True, v=True)
    dirLColR = cmds.intSlider("dirLightColRSlider", q=True, v=True)
    dirLColG = cmds.intSlider("dirLightColGSlider", q=True, v=True)
    dirLColB = cmds.intSlider("dirLightColBSlider", q=True, v=True)
    
    # change rotations based on slider values
    cmds.directionalLight('Directional_Light', e=True, rot=[dirLRotX, dirLRotY, 0], rgb=[dirLColR *0.01, dirLColG *0.01, dirLColB *0.01], i= dirLInt * 0.1)

# Delete lighting Window then open render window
def openRenderWnd(*args):
    cmds.deleteUI("LightingWindow", window=True)
    windowRender()
    
# delete lighting window
def deleteLightingWindow(*args):
    cmds.deleteUI("LightingWindow", window=True)
    
# delete lighting window then open camera window.  Go Back.
def goBackLightingWindow(*args):
    # deletes the lighting window
    deleteLightingWindow() 
    
    # creates the camera window
    windowCamera()   
    
    # deletes camera_02 after it is created due to the camra window being open.
    cmds.delete('camera_02')
    
# ******************Create Lighting Setup Window******************

def windowLighting(*args):
    # checks to see if window exists. if so, delete it.
    if (cmds.window("LightingWindow", q=True, exists=True) == True):
        cmds.deleteUI("LightingWindow", window=True)
        
    # turns on "all lights" and "shadows" for the viewport so that we get an accurate depiction of lighting.
    cmds.modelEditor('modelPanel4', e=True, dl='all', sdw=True)       

    # create window
    lightWindow = cmds.window("LightingWindow", title="Lighting Setup", iconName='Lighting Setup', bgc=[0.2, 0.2, 0.2], sizeable=False)
    cmds.rowColumnLayout( numberOfColumns=4 )

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    
    #__________________________AMBIENT LIGHT__(TAB 1)_______________________________________________

    # ambient light checkbox
    cmds.text(label="Ambient Light:  ", al="left")
    cmds.checkBox("ambientLightBool", label='', onc=createAmbientLight, ofc=delAmbientLight)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # slider to control ambient light intensity
    cmds.text(label="Ambient Light Intensity")

    ambLightIntSlider = cmds.intSlider("ambLightIntSlider", min=1, max=20, value=10, step=1, dc=queryAmbLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control ambient light color
    cmds.text(label="Ambient Light Color: RED")

    ambLightColRSlider = cmds.intSlider("ambLightColRSlider", min=0, max=100, value=100, step=1, dc=queryAmbLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control ambient light color
    cmds.text(label="Ambient Light Color: GREEN")

    ambLightColGSlider = cmds.intSlider("ambLightColGSlider", min=0, max=100, value=100, step=1, dc=queryAmbLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control ambient light color
    cmds.text(label="Ambient Light Color: BLUE")

    ambLightColBSlider = cmds.intSlider("ambLightColBSlider", min=0, max=100, value=100, step=1, dc=queryAmbLightSliders)

    # blank space for ui elements
    cmds.text(label="")

    # blank space for ui elements
    cmds.separator(h=40)
    cmds.separator(h=40)
    cmds.separator(h=40)
    cmds.separator(h=40)
    #______________________________DIRECTIONAL LIGHT_____________________________________________

    # directional light
    cmds.text(label="Directional Light:  ", al="left")
    cmds.checkBox("dirLightBool", label='', onc=createDirLight, ofc=delDirLight)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # slider to control directional light x rotation
    cmds.text(label="Directional Light Rotation X")

    dirLightRotXSlider = cmds.intSlider("dirLightRotXSlider", min=0, max=359, value=72, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control direction light y rotation
    cmds.text(label="Directional Light Rotation Y")

    dirLightRotYSlider = cmds.intSlider("dirLightRotYSlider", min=0, max=359, value=180, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the directional light intensity
    cmds.text(label="Directional Light Intensity")

    dirLightIntSlider = cmds.intSlider("dirLightIntSlider", min=1, max=100, value=50, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the directional light color RED
    cmds.text(label="Directional Light Color RED")

    dirLightColRSlider = cmds.intSlider("dirLightColRSlider", min=0, max=100, value=100, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the direction light color GREEN
    cmds.text(label="Directional Light Color GREEN")

    dirLightColGSlider = cmds.intSlider("dirLightColGSlider", min=0, max=100, value=100, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the directional light color BLUE
    cmds.text(label="Directional Light Color BLUE")

    dirLightColBSlider = cmds.intSlider("dirLightColBSlider", min=0, max=100, value=100, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")

    # blank space for ui elements
    cmds.separator(h=40)
    cmds.separator(h=40)
    cmds.separator(h=40)
    cmds.separator(h=40)

    #_____________________________SPOT LIGHT______________________________________________

    # spotlight checkbox
    cmds.text(label="Spot Light: ", al="left")
    cmds.checkBox("spotLightBool", label='', onc=createSpotLight, ofc=deleteSpotLight)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # slider for Spot Light X
    cmds.text(label="Spotlight Pos X: ")

    camFOVSlider = cmds.intSlider("spotLightSliderX", min=-1000, max=1000, value=0, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider for Spot Light Y
    cmds.text(label="Spotlight Pos Y: ")

    camFOVSlider = cmds.intSlider("spotLightSliderY", min=-1000, max=1000, value=0, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider for Spot Light Z
    cmds.text(label="Spotlight Pos Z: ")

    camFOVSlider = cmds.intSlider("spotLightSliderZ", min=-1000, max=1000, value=0, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the spot light intensity
    cmds.text(label='Spotlight Intensity')

    spotLightIntSlider = cmds.intSlider("spotLightIntSlider", min=1, max=100, value=50, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the spot light color RED
    cmds.text(label="Spotlight Color RED")

    spotLightColRSlider = cmds.intSlider("spotLightColRSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the spot light color GREEN
    cmds.text(label="Spotlight Color GREEN")

    spotLightColGSlider = cmds.intSlider("spotLightColGSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the spot light color BLUE
    cmds.text(label="Spotlight Color BLUE")

    spotLightColBSlider = cmds.intSlider("spotLightColBSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the spot light cone angle
    cmds.text(label="Spotlight Cone Angle")

    spotLightConeSlider = cmds.intSlider("spotLightConeSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider to control the spot light dropoff 
    cmds.text(label="Spotlight Dropoff")

    spotLightDropoffSlider = cmds.intSlider("spotLightDropoffSlider", min=0, max=256, value=0, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")

    # blank space for ui elements
    cmds.separator(h=40)
    cmds.separator(h=40)
    cmds.separator(h=40)
    cmds.separator(h=40)

    #________________________Save & Load Buttons________________________________________

    # blank space for ui elements
    cmds.text(label="")

    # button to save Lighting settings
    cmds.button(label=' Save Light Settings ', command=executeWriteLightSettings, bgc=[0.3,0.3,0.3])

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # button to load the Lighting settings
    cmds.button(label=' Load Light Settings ', command=loadLightSettings, bgc=[0.3,0.3,0.3])

    #________________________RENDER WINDOW BUTTON__________________________________________

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # button to close the current window and open the Render Settings Window.
    cmds.button(label="Step #3: Rendering", command=openRenderWnd, bgc=[0.3,0.3,0.3])

    #_______________________GO BACK BUTTON________________________________________________

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # button go back to previous window
    cmds.button(label=' Go Back. ',command=goBackLightingWindow, bgc=[0.3,0.3,0.3])

    #_________________________CLOSE BUTTON__________________________________________________

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # button to close the current window
    cmds.button(label='Close', command=deleteLightingWindow, bgc=[0.3,0.3,0.3])
    cmds.setParent('..')
    
    # Force show window
    cmds.showWindow(lightWindow)
    
    # Force resize the window
    cmds.window( lightWindow, edit=True, rtf=True, wh= [350,625], tlc=[0,0], sizeable=False )

# Delete Camera Window
def deleteCameraWnd(*args):
    cmds.deleteUI("CameraWindow", window=True)
    windowLighting()

# ********************Create Camera Setup Window******************
def windowCamera():
    # checks to see if window exists. if so, delete it.
    if (cmds.window("CameraWindow", q=True, exists=True) == True):
        cmds.deleteUI("CameraWindow", window=True)
        
    # make window
    camWindow =cmds.window("CameraWindow", title="Camera Setup", iconName='Camera Setup', bgc=[0.2, 0.2, 0.2], sizeable=False)
    #cmds.columnLayout(adjustableColumn=True)
    cmds.rowColumnLayout( numberOfColumns=2 )
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # checkbox for camera to always look at origin
    cmds.text(label="Camera Always Face Origin (Resets Camera):  ")
    cmds.checkBox("cameraLookAtBool", label='', onc=cameraLookAtCB, ofc=cameraLookAtCB)
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider for translation of camera
    ### X
    cmds.text(label="Camera Location X: ")
    # blank space for ui elements
    cmds.text(label="")
    cmds.text("transXLabel", label=camTransX)
    # blank space for ui elements
    cmds.text(label="")
    camTransXSlider = cmds.intSlider("camTransXSlider", min=-1000, max=1000, value=0, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    ### Y
    cmds.text(label="Camera Location Y: ")
    # blank space for ui elements
    cmds.text(label="")
    cmds.text("transYLabel", label=camTransY)
    # blank space for ui elements
    cmds.text(label="")
    camTransYSlider = cmds.intSlider("camTransYSlider", min=-1000, max=1000, value=0, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    ### Z
    cmds.text(label="Camera Location Z: ")
    # blank space for ui elements
    cmds.text(label="")
    cmds.text("transZLabel", label=camTransZ)
    # blank space for ui elements
    cmds.text(label="")
    camTransZSlider = cmds.intSlider("camTransZSlider", min=-1000, max=1000, value=5, step=1, dc=queryCameraSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # Slider to control FOV
    cmds.text(label="FOV")
    # blank space for ui elements
    cmds.text(label="")
    cmds.text("fovLabel",label=camFOV)
    # blank space for ui elements
    cmds.text(label="")
    camFOVSlider = cmds.intSlider("camFOVSlider", min=5, max=120, value=20, step=1, dc=queryFOV)    
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # create camera
    cmds.camera(n="camera_01", p=[cmds.intSlider(camTransXSlider, q=True, v=True), cmds.intSlider(camTransYSlider, q=True, v=True), cmds.intSlider(camTransZSlider, q=True, v=True)])
    cmds.lookThru("camera_01")
        
    #Line of text lines
    cmds.separator(height=40, style='in')
    
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # button to move Save Camera Settings
    cmds.button(label=' Save Camera Settings ', command=executeWriteCameraSettings, bgc=[0.3,0.3,0.3])
    
    # blank space for ui elements
    cmds.text(label="")
    
    # button to move Load Camera Settings
    cmds.button(label=' Load Camera Settings ', command=loadCameraSettings, bgc=[0.3,0.3,0.3])
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")

    # button to move onto Lighting
    cmds.button(label=' Step #2: Lighting ', command=deleteCameraWnd, bgc=[0.3,0.3,0.3])

    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # button to close the current window
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + camWindow + '\", window=True)'), bgc=[0.3,0.3,0.3])
    cmds.setParent('..')
    
    #Force show window
    cmds.showWindow(camWindow)
    
    # Force resize the window
    cmds.window( camWindow, edit=True, widthHeight=(250, 450), rtf=True,  tlc=[0,0] )

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

    # Translate camera
    cmds.move(camTransX*0.02, camTransY*0.02, camTransZ*0.02, "camera_01", absolute=True)
    
    # check bool of always face origin for camera
    camLookAt = cmds.checkBox("cameraLookAtBool", q=True, v=True)
    if camLookAt == True:
        cmds.viewPlace( "camera_01", la=(0, 0, 0) )
        # updates off of cameraLookAtCB()
        
    # update text values of sliders
    cmds.text("transXLabel", e=True, label=camTransX)
    cmds.text("transYLabel", e=True, label=camTransY)
    cmds.text("transZLabel", e=True, label=camTransZ)

# Delete Main Window for open camera window
def deleteMain(*args):
    cmds.deleteUI("MainWindow", window=True)
    windowCamera()
    
# Delete Main Window for close
def deleteMainWindow(*args):
    cmds.deleteUI("MainWindow", window=True)

# ******************Create Main Window********************
def windowMain(*args):
    #checks to see if window exists. if so, delete it.
    if (cmds.window("MainWindow", q=True, exists=True) == True):
        cmds.deleteUI("MainWindow", window=True)
    
    # create Main Window
    mainWindow = cmds.window("MainWindow", title="Main Window", iconName='Main', widthHeight=(500, 115), bgc=[0.2,0.2,0.2] )
    cmds.rowColumnLayout( numberOfRows=7 )
                                               
    #text to describe tool
    cmds.text(label="Render Assistant", bgc=[0.5,0.5,0.5]) 
    
    # text body
    cmds.text(label="This tool will automate setting up a camera and allow user refinemnet of view. Then a lighting setup will be created based on the users selction.  Lastly, define render options and render either a single frame or a sequence.", ww=True)

    #spacer
    cmds.text(label="")     
     
    # make button to open Camera Setup Window.
    cmds.button(label='Step #1: Camera Setup', align='center', bgc=[0.3,0.3,0.3], command=deleteMain)
    
    #spacer
    cmds.text(label="") 
   
    # button to close the current window
    cmds.button(label='Close', command=deleteMainWindow, bgc=[0.3,0.3,0.3])
    cmds.setParent('..')
    
    #Force show window
    cmds.showWindow(mainWindow)
    
    # Force resize the window
    cmds.window( mainWindow, edit=True, widthHeight=(240, 175), tlc=[0,0], sizeable=False )

'''
*********************************************************************
RUN DEFINITIONS
*********************************************************************
'''

# run defs
windowMain()