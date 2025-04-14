# DICOM-Loader-and-Automation-with-Jython
ImageJ (Fiji) script written in Jython (Python for ImageJ). It's tailored for handling DICOM datasets, and automates multiple preprocessing steps.


The script:

- Loads a DICOM folder.

- Applies contrast enhancement + LUT.

- Flips image orientation (user may adjust their orientation settings).

- Reslices to generate orthogonal views (top, left).

- Applies Max Intensity Projection (MIP).

- Saves each MIP as a BMP image.

- Arranges all outputs visually for comparison.


To run the script: 
1- Download 'loader.py' from the repository
2- Locate imagej folder in your system: Search for imagej and select 'Open file location'
3- Open plugins folder
4- Copy and paste 'loader.py' into the plugins folder
5- Restart ImageJ (Fiji)
6- Run 'loader' from plguins tab
