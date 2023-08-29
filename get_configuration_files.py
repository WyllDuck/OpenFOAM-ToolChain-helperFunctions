# Imports
from math import sin, cos, pi
import pandas as pd
from copy import copy
import json

import sys, os
from pathlib import Path


# Selected Regions of Interest
SELECTED_MESHES     = ["4.5M_13L"]
SELECTED_SOLVERS    = ["rhoPimpleFoam", "rhoCentralFoam", "rhoSimpleFoam"]
SELECTED_MA         = [0.6, 1.0, 1.5, 2.3, 4.63]
SELECTED_AOA        = [0, 4, 8, 16]

# Addresses Files
GLOBAL_DIR          = os.path.abspath(os.path.dirname(sys.argv[0]))
BNDS_FILE_NAME      = "boundary_conditions.csv"
CA_WINDTUNNEL_NAME  = "CA_coefficients.csv"
CN_WINDTUNNEL_NAME  = "CN_coefficients.csv"
CM_WINDTUNNEL_NAME  = "Cm_coefficients.csv"

"""
-----------------------------------------------------------------------------------------
"""

#################
#   READ FILES  #
#################

# boundary conditions file
bnds_file           = pd.read_csv(GLOBAL_DIR + "/" + BNDS_FILE_NAME)

# expect values file
CA_windTunnel_file  = pd.read_csv(GLOBAL_DIR + "/" + CA_WINDTUNNEL_NAME)
CN_windTunnel_file  = pd.read_csv(GLOBAL_DIR + "/" + CN_WINDTUNNEL_NAME)
CM_windTunnel_file  = pd.read_csv(GLOBAL_DIR + "/" + CM_WINDTUNNEL_NAME)


# FILL IN DEFAULT PARAMETERS CONFIG
config = {
    "solver": None,
    "mesh_file": None,
    "map_file": "none",
    "flowVelocity": [
        None,
        None,
        None
    ],
    "vanLeer": None,
    "minIter": None,
    "final_Co": None,
    "nprocessors": [4, 1, 1],
    "pressure": None,
    "temperature": None,
    "density": None,
    "Aref": 0.001282603306,
    "lRef": 1.04013,
    "CofR": [
        0.7286625,
        0,
        0
    ],
    "liftDir": [
        0,
        0,
        1
    ],
    "dragDir": [
        1,
        0,
        0
    ],
    "pitchAxis": [
        0,
        1,
        0
    ],
    "Cd_windTunnel": None,
    "Cl_windTunnel": None,
    "CmPitch_windTunnel": None,
}


# MAIN
def main ():

    folder_dir = GLOBAL_DIR + "/configs"
    Path(folder_dir).mkdir(parents=True, exist_ok=True)

    for solver in SELECTED_SOLVERS:
        for Ma in SELECTED_MA:
            for AoA in SELECTED_AOA:

                # Create empty configuration file
                config_ = copy(config)

                bndsMaCase = bnds_file[bnds_file["Mach Number"] == Ma].iloc[0]

                # Look up values boundary conditions
                # Velocity
                Umag = bndsMaCase["Velocity [m/s]"]
                Ux = Umag * cos(AoA / 180 * pi) 
                Uy = 0
                Uz = Umag * sin(AoA / 180 * pi) 
                config_["flowVelocity"] = [Ux, Uy, Uz]

                # Pressure
                config_["pressure"]     = bndsMaCase["Pressure [Pa]"]
                config_["temperature"]  = bndsMaCase["Temperature [K]"]
                config_["density"]      = bndsMaCase["Density [kg/m^3]"]

                # Coefficients Wind Tunnel
                search = CA_windTunnel_file[CA_windTunnel_file["AoA"] == AoA].iloc[0]
                config_["Cd_windTunnel"]        = search["M{}_CA-ALPHA".format(Ma)]
                search = CN_windTunnel_file[CN_windTunnel_file["AoA"] == AoA].iloc[0]
                config_["Cl_windTunnel"]        = search["M{}_CN-ALPHA".format(Ma)]
                
                search = CM_windTunnel_file[CM_windTunnel_file["AoA"] == AoA].iloc[0]
                config_["CmPitch_windTunnel"]   = search["M{}_Cm-ALPHA".format(Ma)]

                config_["solver"] = solver

                # rhoCentralFoam Specific
                if config_["solver"] == "rhoCentralFoam":
                    config_ = rhoCentralFoam_specific(config_)

                # ------------------------------------------------------------------------
                # Save file as JSON
                path = folder_dir + "/config_" + "{}_Ma{}_AoA{}_R{}.json".format(solver, Ma, AoA, 0)
                with open(path, 'w') as outfile:
                    json.dump(config_, outfile, indent=2, separators=(',', ': '))

    return 0


# Solver Specific Configuration Parts
def rhoCentralFoam_specific (config_):

    config_["vanLeer"]  = 250
    config_["minIter"]  = 550
    config_["final_Co"] = 0.16
    
    return config_


if __name__ == "__main__":
    main()