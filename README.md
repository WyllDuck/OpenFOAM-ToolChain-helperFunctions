# Helper Functions - <a href="https://www.example.com/my great page">OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis</a>
__by Félix Marti Valverde__

This repository is part of a greater project found in the main repository _OpenFOAM ToolChain for Rocket Aerodynamic Analysis_ (https://github.com/WyllDuck/OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis). The functions contained here are miscelaneous calculations and or data extraction scripts to validate the CFD methodology followed in the main repository.

### links

## SETUP

Install all the requiered python libraries 
```bash
python3 -m pip install -r requirements.txt
```

## CONTENT

<ul>
  <li><b>data</b>: <i>PDFs</i> containing only the relevant wind-tunnel graphs used to validate the CFD results. Data comes from sources [1][2].</li>
  
  <li><b>graph</b>: All the pages contained in the pdf from <i>data</i> are converted to <i>JPEG</i> images in order to procced to data digitalization using python scripts.</li>
  
  <li><b>paper_plots</b>: This folder <b>only contains Python scripts used to generate the plots in the report</b>. Click on link above to access the report.</li>
  
  <li><b>paraview_states_plots</b>: This folder <b>contains the Paraview state files used to postprocess CFD results in the report</b> in addition to the raw images added in the report. Click on link above to access the report.</li>
  
  <li><b>points</b>: Contains a set of <b>TXT</b> with information to extract each image in <b>graphs</b> to valuable aerodynamic coefficients</li>

  ---

  <li><b><i>PYTHON_SCRIPTS</i></b>
    <ul>
      <li><i>picture2coefficients.py</i>: Looks in the <i>points</i> folder and proceeds to change the reference frame from pixel position in image to the described reference frame based on the respective graph in <i>graphs</i>. Then using the new data points available it goes on to feed it to a spline line to interpolate the remaining data points. Finally, the resulting data in saved in <i>CSV</i> files. See <i>CSV_FILES</i> for more information on the files generated. Additionally, a folder named <i>check_images</i> 2 images per graph, one overlaying the <i>TXT</i> information over the original image in <i>graphs</i> and another image with the generated spline data points.</li>  
      <li><i>get_boundary_conditions.py</i>: Calculates the different boundary conditions requiered for each Mach Number to keep a constant Reynolds number.</li>
      <li><i>atmosphere.py</i>: Model of the atmosphere used to calculate inlet conditions in the <i>get_boundary_conditions.py</i> script</li>
      <li><i>get_configuration_files.py</i>: Configurable script assess in the generation of large amounts of configuration files for each CFD simulation. For more information on the structure and the usage of these configuration files please visit the main repository: https://github.com/WyllDuck/OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis </li>
    </ul>
  </li>

  <li><b><i>CSV_FILES</i></b></li>
  <ul>
    <li><i>CA_coefficients.csv</i>: Axial Aerodynamic Coefficient vs. Angle of Attack and Mach Number</li>
    
    <li><i>CN_coefficients.csv</i>: Normal Aerodynamic Coefficient vs. Angle of Attack and Mach Number</li>
    
    <li><i>Cm_coefficients.csv</i>: Pitch Moment Aerodynamic Coefficient vs. Angle of Attack and Mach Number</li>
    
    <li><i>boundary_conditions.csv</i>: All relevant inlet boundary conditions for each Mach number</li>
    
  </ul>
</ul>

## SOURCES
