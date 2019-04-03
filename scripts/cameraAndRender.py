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

'''
*********************************************************************
'''

# delete Render Window
def deleteRenderWnd(*args):
    cmds.deleteUI("RenderWindow", window=True)

# create Render Window
def windowRender(*args):
    # checks to see if window exists. if so, delete it.
    if (cmds.window("RenderWindow", q=True, exists=True) == True):
        cmds.deleteUI("RenderWindow", window=True)     

    # create window
    renderWindow = cmds.window("RenderWindow", title="Render Setup", iconName='Render Setup', bgc=[0.0, 0.1, 0.1], sizeable=False)
    cmds.rowColumnLayout( numberOfColumns=2 )

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #___________________________________________________________________________
    
    #_________________________TEST RENDER_________________________________________
    
    # perform a test render of the current scene
    cmds.button(label='Test Render', bgc=[1,1,0])
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #____________________________RENDER_____________________________________________
    
    # button to Render the current scene
    cmds.button(label='RENDER', bgc=[0,1,0])
    # blank space for ui elements
    cmds.text(label="")
    
    #_______________________GO BACK BUTTON________________________________________________
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # button go back to previous window
    cmds.button(label=' Go Back. ', bgc=[1,1,1])
    # blank space for ui elements
    cmds.text(label="") 
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #_________________________CLOSE BUTTON__________________________________________________

    # button to close the current window
    cmds.button(label='Close', command=deleteRenderWnd, bgc=[1,0,0])
    cmds.setParent('..')
    
    # Force show window
    cmds.showWindow(renderWindow)
    
    # Force resize the window
    cmds.window( renderWindow, edit=True, widthHeight=(900, 777), tlc=[0,0] )

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
    spotLightX = cmds.intSlider("spotLighSliderX", q=True, v=True)
    spotLightY = cmds.intSlider("spotLighSliderY", q=True, v=True)
    spotLightZ = cmds.intSlider("spotLighSliderZ", q=True, v=True)
    
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
    
# Quesry slider values for ambient light intensity and color
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
    dirLInt = cmds.intSlider("direLightIntSlider", q=True, v=True)
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
    
# Create Lighting Setup Window
def windowLighting(*args):
    # checks to see if window exists. if so, delete it.
    if (cmds.window("LightingWindow", q=True, exists=True) == True):
        cmds.deleteUI("LightingWindow", window=True)
        
    # turns on "all lights" and "shadows" for the viewport so that we get an accurate depction of lighting.
    cmds.modelEditor('modelPanel4', e=True, dl='all', sdw=True)       

    # create window
    lightWindow = cmds.window("LightingWindow", title="Lighting Setup", iconName='Lighting Setup', bgc=[0.2, 0.2, 0.0], rtf=True, sizeable=False)
    cmds.rowColumnLayout( numberOfColumns=2 )

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #__________________________AMBIENT LIGHT_________________________________________________

    # ambient light checkbox
    cmds.text(label="Ambient Light:  ", al="left")
    cmds.checkBox("ambientLightBool", label='', onc=createAmbientLight, ofc=delAmbientLight)
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control ambient light intensity
    cmds.text(label="Ambient Light Intensity")
    # blank space for ui elements
    cmds.text(label="")
    ambLightIntSlider = cmds.intSlider("ambLightIntSlider", min=1, max=20, value=10, step=1, dc=queryAmbLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control ambient light color
    cmds.text(label="Ambient Light Color: RED")
    # blank space for ui elements
    cmds.text(label="")
    ambLightColRSlider = cmds.intSlider("ambLightColRSlider", min=0, max=100, value=100, step=1, dc=queryAmbLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control ambient light color
    cmds.text(label="Ambient Light Color: GREEN")
    # blank space for ui elements
    cmds.text(label="")
    ambLightColGSlider = cmds.intSlider("ambLightColGSlider", min=0, max=100, value=100, step=1, dc=queryAmbLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control ambient light color
    cmds.text(label="Ambient Light Color: BLUE")
    # blank space for ui elements
    cmds.text(label="")
    ambLightColBSlider = cmds.intSlider("ambLightColBSlider", min=0, max=100, value=100, step=1, dc=queryAmbLightSliders)
    # blank space for ui elements
    cmds.text(label="")

    # blank space for ui elements
    cmds.separator(h=40)
    cmds.text(label="")
    
    #______________________________DIRECTIONAL LIGHT_____________________________________________
    
    # directional light
    cmds.text(label="Directional Light:  ", al="left")
    cmds.checkBox("dirLightBool", label='', onc=createDirLight, ofc=delDirLight)
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control directional light x rotation
    cmds.text(label="Directional Light Rotation X")
    # blank space for ui elements
    cmds.text(label="")
    dirLightRotXSlider = cmds.intSlider("dirLightRotXSlider", min=0, max=359, value=72, step=1, dc=queryDirLightSlider)
    
    # blank space for ui elements
    cmds.text(label="")   
    
    # slider to control direction light y rotation
    cmds.text(label="Directional Light Rotation Y")
    # blank space for ui elements
    cmds.text(label="")
    dirLightRotYSlider = cmds.intSlider("dirLightRotYSlider", min=0, max=359, value=180, step=1, dc=queryDirLightSlider)
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the directional light intensity
    cmds.text(label="Directional Light Intensity")
    # blank space for ui elements
    cmds.text(label="")
    dirLightIntSlider = cmds.intSlider("direLightIntSlider", min=1, max=100, value=50, step=1, dc=queryDirLightSlider)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the directional light color RED
    cmds.text(label="Directional Light Color RED")
    # blank space for ui elements
    cmds.text(label="")
    dirLightColRSlider = cmds.intSlider("dirLightColRSlider", min=0, max=100, value=100, step=1, dc=queryDirLightSlider)
    
    # blank space for ui elements
    cmds.text(label="")
    
    # slider to control the directiona light color GREEN
    cmds.text(label="Directional Light Color GREEN")
    # blank space for ui elements
    cmds.text(label="")
    dirLightColGSlider = cmds.intSlider("dirLightColGSlider", min=0, max=100, value=100, step=1, dc=queryDirLightSlider)
    
    # blank space for ui elements
    cmds.text(label="")
    
    # slider to control the directional light color BLUE
    cmds.text(label="Directional Light Color BLUE")
    # blank space for ui elements
    cmds.text(label="")
    dirLightColBSlider = cmds.intSlider("dirLightColBSlider", min=0, max=100, value=100, step=1, dc=queryDirLightSlider)
    
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.separator(h=40)
    cmds.text(label="")
    
    #_____________________________SPOT LIGHT______________________________________________

    # spotlight checkbox
    cmds.text(label="Spot Light: ", al="left")
    cmds.checkBox("spotLightBool", label='', onc=createSpotLight, ofc=deleteSpotLight)

    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # slider for Spot Light X
    cmds.text(label="Spotlight Pos X: ")
    # blank space for ui elements
    cmds.text(label="")
    camFOVSlider = cmds.intSlider("spotLighSliderX", min=-1000, max=1000, value=0, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")

    # slider for Spot Light Y
    cmds.text(label="Spotlight Pos Y: ")
    # blank space for ui elements
    cmds.text(label="")
    camFOVSlider = cmds.intSlider("spotLighSliderY", min=-1000, max=1000, value=0, step=1, dc=querySpotLightSliders)

    # blank space for ui elements
    cmds.text(label="")

    # slider for Spot Light Z
    cmds.text(label="Spotlight Pos Z: ")
    # blank space for ui elements
    cmds.text(label="")
    camFOVSlider = cmds.intSlider("spotLighSliderZ", min=-1000, max=1000, value=0, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the spot light intensity
    cmds.text(label='Spotlight Intensity')
    # blank space for ui elements
    cmds.text(label="")
    spotLightIntSlider = cmds.intSlider("spotLightIntSlider", min=1, max=100, value=50, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the spot light color RED
    cmds.text(label="Spotlight Color RED")
    # blank space for ui elements
    cmds.text(label="")
    spotLightColRSlider = cmds.intSlider("spotLightColRSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the spot light color GREEN
    cmds.text(label="Spotlight Color GREEN")
    # blank space for ui elements
    cmds.text(label="")
    spotLightColGSlider = cmds.intSlider("spotLightColGSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the spot light color BLUE
    cmds.text(label="Spotlight Color BLUE")
    # blank space for ui elements
    cmds.text(label="")
    spotLightColBSlider = cmds.intSlider("spotLightColBSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the spot light cone angle
    cmds.text(label="Spotlight Cone Angle")
    # blank space for ui elements
    cmds.text(label="")
    spotLightConeSlider = cmds.intSlider("spotLightConeSlider", min=0, max=100, value=100, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # slider to control the spot light dropoff 
    cmds.text(label="Spotlight Dropoff")
    # blank space for ui elements
    cmds.text(label="")
    spotLightDropoffSlider = cmds.intSlider("spotLightDropoffSlider", min=0, max=256, value=0, step=1, dc=querySpotLightSliders)
    # blank space for ui elements
    cmds.text(label="")   
    
    # blank space for ui elements
    cmds.separator(h=40)
    cmds.text(label="")
    
    #________________________RENDER WINDOW BUTTON__________________________________________
    
    # button to close the current window and open the Render Settings Window.
    cmds.button(label="Step #3: Rendering", command=openRenderWnd, bgc=[0,1,0])
    # blank space for ui elements
    cmds.text(label="")  
    
    #_______________________GO BACK BUTTON________________________________________________
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # button go back to previous window
    cmds.button(label=' Go Back. ', bgc=[1,1,1])
    # blank space for ui elements
    cmds.text(label="") 
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    #_________________________CLOSE BUTTON__________________________________________________

    # button to close the current window
    cmds.button(label='Close', command=deleteLightingWindow, bgc=[1,0,0])
    cmds.setParent('..')
    
    # Force show window
    cmds.showWindow(lightWindow)
    
    # Force resize the window
    cmds.window( lightWindow, edit=True, widthHeight=(175, 985), tlc=[0,0] )

# Delete Camera Window
def deleteCameraWnd(*args):
    cmds.deleteUI("CameraWindow", window=True)
    windowLighting()

# Create Camera Setup Window
def windowCamera():
    # checks to see if window exists. if so, delete it.
    if (cmds.window("CameraWindow", q=True, exists=True) == True):
        cmds.deleteUI("CameraWindow", window=True)
        
    # make window
    camWindow =cmds.window("CameraWindow", title="Camera Setup", iconName='Camera Setup', bgc=[0.2, 0.2, 0.2], sizeable=True)
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

    # button to move onto Lighting
    cmds.button(label=' Step #2: Lighting ', command=deleteCameraWnd, bgc=[0,1,0])

    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")
    
    # button go back to previous window
    cmds.button(label=' Go Back. ', bgc=[1,1,1])
    # blank space for ui elements
    cmds.text(label="")
    
    # blank space for ui elements
    cmds.text(label="")
    cmds.text(label="")

    # button to close the current window
    cmds.button(label='Close', command=('cmds.deleteUI(\"' + camWindow + '\", window=True)'), bgc=[1,0,0])
    cmds.setParent('..')
    
    #Force show window
    cmds.showWindow(camWindow)
    
    # Force resize the window
    cmds.window( camWindow, edit=True, widthHeight=(250, 405), tlc=[0,0] )

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
        
# Delete Main Window for open camera window
def deleteMain(*args):
    cmds.deleteUI("MainWindow", window=True)
    windowCamera()
    
# Delete Main Window for close
def deleteMainWindow(*args):
    cmds.deleteUI("MainWindow", window=True)

# Create Main Window
def windowMain(*args):
    #checks to see if window exists. if so, delete it.
    if (cmds.window("MainWindow", q=True, exists=True) == True):
        cmds.deleteUI("MainWindow", window=True)
    
    # create Main Window
    mainWindow = cmds.window("MainWindow", title="Main Window", iconName='Main', widthHeight=(500, 100), bgc=[0,0,0], sizeable=True)
    cmds.rowColumnLayout( numberOfRows=5 )
                                               
    #text to describe tool
    cmds.text(label="Auto Render Sprite Sheet Tool", bgc=[0.5,0.5,0.5]) 
    
    # text body
    cmds.text(label="This tool will automate setting up a camera and allow user refinemnet of view. Then a lighting setup will be created based on the users selction.  Lastly, Once render is hit, Maya will render the scene then spit out a sprite sheet.", ww=True)

    #spacer
    cmds.text(label="")     
     
    # make button to open Camera Setup Window.
    cmds.button(label='Step #1: Camera Setup', align='center', bgc=[0,1,0], command=deleteMain)
   
    # button to close the current window
    cmds.button(label='Close', command=deleteMainWindow, bgc=[1,0,0])
    cmds.setParent('..')
    
    #Force show window
    cmds.showWindow(mainWindow)
    
    # Force resize the window
    cmds.window( mainWindow, edit=True, widthHeight=(240, 150), tlc=[0,0] )

'''
*********************************************************************
RUN DEFINITIONS
*********************************************************************
'''

# run defs
windowMain()