# Helper Functions - <a href="https://www.example.com/my great page">OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis</a>
__by Félix Marti Valverde__

This repository is part of a greater project found in the main repository _OpenFOAM ToolChain for Rocket Aerodynamic Analysis_ (https://github.com/WyllDuck/OpenFOAM-ToolChain-for-Rocket-Aerodynamic-Analysis). The functions contained here are miscelaneous calculations and or data extraction scripts to validate the CFD methodology followed in the main repository.

### links

## SETUP

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
      <li><i>get_boundary_conditions.py</i>: </li>
      <li><i>get_boundary_conditions.py</i></li>
      <li><i>atmosphere.py</i></li>
    </ul>
  </li>

  <li><b><i>CSV_FILES</i></b></li>
</ul>

## SOURCES
