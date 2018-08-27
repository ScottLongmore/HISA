README.TXT -  CSU/CIRA/RAMMB Hurricane Intensity and Strength Algorithm (HISA) 
              Author: Scott Longmore, Cooperative Institute for Research in the Atmosphere (CIRA) 
              Contact: Scott.Longmore@colostate.edu
              Last Edit: 2018-08-27


Version Number: v2.0.3

Release Date: beta 

Configuration Target:

  - Source Directory Structure

    src/
       makefile - Master makefile
       gfspack/ - gfspack code
       ShortTermTrack/ - ShortTermTrack code
       afdeck/ - afdeck code
       satcenter/ - satcenter code
       oparet/ - oparet TC wind estimation code
       common/ - common source code 

    scripts/
       python/ - python scripts
          HISA/ - HISA system 
             HISA.py - HISA system driver
             libHISA.py - HISA library routines
             dataset.py - parent dataset class (abstract)
             ADECK.py - ATCF/ADECK dataset class 
             GFS.py - GFS dataset class
             ATMS.py - MiRS/ATMS dataset class
             NDE.py - NDE I/O class
          pool/ - MIRS data subset extraction code
             data_pool.py - Extracts a subset of MIRS data from netCDF files to the query subdirectory
          convert/ - converts XYA/RZA files to netCDF
            convert2netCDF.py - netCDF converter
          plot/ - TC wind estimation plotting software
            main_read_plot_xya.py - Plots Wind Field Estimation File
          lib/ - library utility modules and routines 
          test/ - unit tests for system components
            fixtures/ - test data

    bin/ - compiled binaries
       bin2pack.x - converts GFS GRIB to pack format
       ShortTermTrack_mirs.x - find track from current or previous synoptic time
       afdeck.x - determines coordinates from track file
       satcenter.x -  determine satelite scanline time closest to storm
       oparet.x - hurricane intensity and strength estimation algorithm 
   
    etc/ - configuration and supplemenatry data files
          HISA.json - HISA master configuration file (will be split into sub-files in future)
          mirs_atms_img.ini - configuration file for data pool
          oparet/oparet.cfg - scale, offset, and valid values for oparet input data
          oparet/coeffs/<instrument>
             oparet_params.cfg - main <instrument> config file
             pmn_atms0.inp.coef - Pressure miniumn coefficents?  
             r34_atms0.inp.coef - 34kt radius coefficients 
             r50_atms0.inp.coef - 50kt radius coefficients
             r64_atms0.inp.coef - 64kt radius coefficients
             vmx_atms0.inp.coef - Max velocity coeffcients
          convert/xya2netCDF.json - XYA oparet text output to netCDF config
          convert/rza2netCDF.json - RZA oparet text output to netCDF config
          plot/plots_config.txt - ploting configuration file
    
    doc/ - documentation files
          StatusCodes.txt - general and script/executable specific status/exit/error codes

    test/ - component test directory

  - Working Directory Structure

    <RootDir>/ - Root Working Directory

       HISA.PCF - Process Control File, including all path, directory, external program, variables, settings, data filename, etc
       HISA.PSF - Process Status File
       HISA.LOG - Process Log File

       data/ - Input data files: storm track ATCF adeck (text), GFS (grib), and MIRS ATMS (netCDF) 

          <jtwc|nhc)_aBaSnYYYY.dat.YYYYmmddHHMMSS" - Input adeck file 
          <gfs.tHHz.pgrb2.1p00.fHHH.YYYYmmdd> - GFS analysis file (grib or pack)
          <NPR-MIRS-(SND|IMG)_vVVrR_Sat_sYYYYmmddHHMMFFF_eYYYYmmddHHMMFFF_cYYYYmmddHHMMFFF.nc> - MIRS data files (netCDF)

       model/ - Conversion of GFS grib to pack files
          *.bin - variable bin files
          AVN.DAT - GFS pack file
          
       database/ - MIRS subset data

       <BaSnYYYY>/ - Storm processing sub-directories
                     Ba - Basins: [al|ep|wp|cp|io|sh] 
                     Sn - Storm Number
                     YYYYY - Year

           ShortTermTrack_mirs.x - Find track from current or previous synoptic time
              <aBaSnYYYY.dat> - Input adeck file 
              <BaSnYYYY.inp>  - Output storm track file
             
           afdeck.x - Determines coordinates from track file
              <BaSnYYYY.inp> - Input storm track file
              COORDINATES - Output coordinates file

           satcenter.x - Determine satelite scanline time closest to storm
              <BaSnYYYY_YYYYMMDD>.<variable> - Input variable files from pool query (renamed with prefix)
              TIMES - Output time file

           oparet.x - Determines wind fields from MIRS satelite data and GFS model boundary conditions
              AVN.DAT - Input GFS model data file
              <variable.txt> - Input variable files linked to <BaSnYYYY_YYYYMMDD>.<variable> 
              COORTIMES - Input COORDINATE/TIMES concatenated file
              <BaSnYYYY_YYYYMMDD>.LOC - Output Location file 
              <BaSnYYYY_YYYYMMDD>.XYA - Output Wind Field Estimation file 
              <BaSnYYYY_YYYYMMDD>.STA - Output Statistics file 
              <BaSnYYYY_YYYYMMDD>.RZA - Output Variable file 
              <BaSnYYYY_YYYYMMDD>.FIX - Output Intensity/Size Estimation
              <BaSnYYYY_YYYYMMDD>.AFX - Output Aid File  
              <BaSnYYYY_YYYYMMDD>.log - Output Log file 

            main_read_plot_xya.py - Plots Wind Field Estimation File
              <BaSnYYYY_YYYYMMDD>.XYA - Input Wind Field Estimation file 
              <BaSnYYYY_YYYYMMDD>_T_ATMS_250mb.png -    Output 250mb temperature image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_200mb.png - Output 200mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_250mb.png - Output 250mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_300mb.png - Output 300mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_400mb.png - Output 400mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_500mb.png - Output 500mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_600mb.png - Output 600mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_700mb.png - Output 700mb wind field image file
              <BaSnYYYY_YYYYMMDD>_UV+Z_ATMS_800mb.png - Output 800mb wind field image file

       output/
         TC-<BaSnYYYY>_<ver>_<sat>_sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS.AFX - AMSU TC AFX fix file
         TC-<BaSnYYYY>_<ver>_<sat>_sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS_<SnB>_FIX - AMSU TC (JTWC) fix file
         TC-<BaSnYYYY>-XYA_<ver>_<sat>_sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS.nc - XYA netCDF files 
         TC-<BaSnYYYY>-RZA_<ver>_<sat>_sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS.nc - RZA netCDF files 
         TC-<BaSnYYYY>-<field>-<level>_<ver>_<sat>_sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS.png - Storm image files 

       log/
         <subprocess>.log - Sub-process log files

Reference Documents:


Compilation Instructions:

  The master makefile is located in the src/ directory. To compile simply run

     make

  To install executables in the bin/ directory

    make install

  - Compiler Warnings

    No compiler warning with gcc/gfortran 4.4.7-1

Product Control File Description:

    The following data files are needed for HISA: 

       -  The latest ATCDF adeck storm track text files avaiable from NHC/JTWC 
       -  The latest GFS model analysis (F000) file in grib2 format 
       -  The latest set of MIRS (AMSU/ATMS) netCDF files within the last 9hr

Product Status File Description:
      
    The following products will be generated and staged in the working
    directory output/ subdirectory

       TC-<BaSnYYYY>_sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS.<EXT> - Product files for each active storm defined in PSF
       TC-<BaSnYYYY>-<field>-<level>__sYYYYMMDDHHMMSSS_eYYYYMMDDHHMMSSS_cYYYYMMDDHHMMSSS.png - Product image for each active storm files defined in PSF

Production Rule Definitions:

    To be added
