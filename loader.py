#@ File(label="Choose the DICOM folder", style="directory") dicomFolder
#@ File(label="Choose the folder to save MIPs", style="directory") mipSaveFolder

import os
from ij import IJ, ImagePlus, ImageStack
from ij.plugin import ZProjector
from ij.io import Opener
from ij.measure import Calibration

# Function to automatically adjust window and level
def autoAdjustWindowLevel(imp):
    IJ.run(imp, "Enhance Contrast", "saturated=0.35")

# Function to transform image vertically
def transformVertically(imp):
    IJ.run(imp, "Flip Vertically", "")

# Function to apply LUT
def applyLUT(imp):
    IJ.run(imp, "MPI_BlueSteel_interpolate_for_imagej", "")

# Function to load DICOM slices from a folder and set calibration
def loadDicomSlices(folder):
    stack = ImageStack()
    opener = Opener()
    files = [f for f in os.listdir(folder) if f.endswith(".dcm")]
    files.sort()  # Ensure the slices are loaded in the correct order

    calibration = None  # Initialize calibration variable

    for file in files:
        path = os.path.join(folder, file)
        imp = opener.openImage(path)
        if imp is not None:
            if calibration is None:
                calibration = imp.getCalibration()  # Get calibration from the first image
            autoAdjustWindowLevel(imp)
            applyLUT(imp)  # Apply LUT to each slice
            stack.addSlice(imp.getProcessor())
    
    imp = ImagePlus("Original DICOM Stack", stack)
    if calibration is not None:
        imp.setCalibration(calibration)  # Set calibration to the image stack
    return imp

# Function to perform maximum intensity Z-projection and maintain calibration
def maxIntensityZProjection(imp):
    zp = ZProjector(imp)
    zp.setMethod(ZProjector.MAX_METHOD)
    zp.doProjection()
    proj = zp.getProjection()
    proj.setCalibration(imp.getCalibration())  # Ensure the projection maintains the calibration
    applyLUT(proj)  # Apply LUT to MIP
    return proj

# Function to save MIP images as BMP
def saveMIPAsBMP(imp, filePath):
    IJ.saveAs(imp, "bmp", filePath)

# Function to reslice and process views
def processReslicedView(imp, startAt):
    # Reslice the stack
    IJ.run(imp, "Reslice [/]...", "output=1.0 start={} avoid".format(startAt))
    resliced_imp = IJ.getImage()
    resliced_imp.setCalibration(imp.getCalibration())  # Maintain calibration in resliced image
    transformVertically(resliced_imp)
    return maxIntensityZProjection(resliced_imp)

# Function to zoom in on an image
def zoomIn(imp, times):
    imp.show()
    for _ in range(times):
        IJ.run("In [+]")

# Function to arrange images side by side
def arrangeWindows():
    IJ.run("Tile")

# Main script
if dicomFolder is not None and mipSaveFolder is not None:
    dicomStack = loadDicomSlices(dicomFolder.getAbsolutePath())
    if dicomStack is not None:
        zoomIn(dicomStack, 3)  # Show and zoom in on the original DICOM stack
        
        # Transform the original stack vertically
        transformVertically(dicomStack)
        
        # Perform and show original stack's maximum intensity projection
        originalProj = maxIntensityZProjection(dicomStack)
        originalProj.setTitle("Max Intensity Z-Projection (Original Stack)")
        zoomIn(originalProj, 3)  # Show and zoom in on the projection
        saveMIPAsBMP(originalProj, os.path.join(mipSaveFolder.getAbsolutePath(), "Max_Intensity_Z-Projection_Original_Stack.bmp"))
        
        # Process and show Top View
        topViewProj = processReslicedView(dicomStack, "Top")
        topViewProj.setTitle("Max Intensity Z-Projection (Top View)")
        zoomIn(topViewProj, 3)  # Show and zoom in on the projection
        saveMIPAsBMP(topViewProj, os.path.join(mipSaveFolder.getAbsolutePath(), "Max_Intensity_Z-Projection_Top_View.bmp"))
        
        # Process and show Left View
        leftViewProj = processReslicedView(dicomStack, "Left")
        leftViewProj.setTitle("Max Intensity Z-Projection (Left View)")
        zoomIn(leftViewProj, 3)  # Show and zoom in on the projection
        saveMIPAsBMP(leftViewProj, os.path.join(mipSaveFolder.getAbsolutePath(), "Max_Intensity_Z-Projection_Left_View.bmp"))
        
        # Arrange all opened images side by side
        arrangeWindows()
    else:
        print("No valid DICOM images found in the folder")
else:
    print("No folder selected")
