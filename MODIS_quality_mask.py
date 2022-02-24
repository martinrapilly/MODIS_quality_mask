# -*- coding: windows-1258 -*-
#Name: MODIS quality mask
#Description: processes MOD13Q1 imagery (MODIS) to apply pixel reliability masks with Arcpy library
#Author: martin rapilly



import time
try:
##saves start time    
    import datetime  
    inicio = datetime.datetime.now()  
    print 'Hora de inicio: ' + str(inicio) +'\n'
    time1 = time.clock()
    time.sleep(1)

##import arcpy library and spatial analyst extension
    print "Cargando bibliotecas de funciones. Favor esperar..."
    import sys, unicodedata 
    import arcpy, os
    import arcpy.mapping as mapping
    from arcpy.sa import *
    arcpy.CheckOutExtension("Spatial")
    print "Bibliotecas cargadas.\nIniciando procesamiento.\n"
 
   
#defines images input folder path
    RutaEntrada="F:/.../INPUT_FOLDER"
#define workspace path
    arcpy.env.workspace = RutaEntrada
    
#extracts value 72 (good quality pixel value) from pixel_reliability rasters 
    RastersPixelState = arcpy.ListRasters("*state*", "TIF")
#sorts the list aphabetically (important step to match correctly with list of MODIS images with same date) 
    RastersPixelState.sort()
    print RastersPixelState
    ListRasters = arcpy.ListRasters("*b0*", "TIF")
    ListRasters.sort()
    print ListRasters
    
    

#Snap to first raster to use exact same grid for output images
    tile = ListRasters[0]
    arcpy.env.snapRaster = tile

#Checks if output images already exists; if not, extracts value 72 from pixel reliability images
    for r in RastersPixelState:
        if os.path.exists ("F:/../Stack_y_masks_"+ r[:16] + ".tif"):
            print "this file already exists: "+"Stack_y_masks_"+ r[:16] + ".tif"
        else:
       
            print "Extracting value72 from " + r
            attExtract = ExtractByAttributes(r, "Value = 72") 
    
#starts a loop to apply good quality mask on input images and stack all bands from the same date in one file
            for u in ListRasters:
                if u[:16] == r[:16]:
                    print "Applying value 72 mask on raster " + u
                    outExtractByMask = ExtractByMask(u,attExtract)
                    outExtractByMask.save('Mask72_'+ u + ".tif")
            bands = arcpy.ListRasters('Mask72_'+r[:26]+"b0*", "TIF")
            bands.sort()
            print ("bands sorted: ",bands)
            #create stack
            arcpy.CompositeBands_management(bands,"F:/.../Stack_y_masks_"+ r[:16] + ".tif")
            print "stack created for image "+r[:16]
     
##print end time    
    time2 = time.clock()
    final=datetime.datetime.now()
    print "Processing ended at " + str(final)+ ' in '+ str((time2-time1)/3600) + " hours" 
  
except Exception,e: print str(e)
