# Imports
from math import sin, cos, pi
import pandas as pd
from copy import deepcopy as copy
import json

import sys, os
from pathlib import Path


# Selected Regions of Interest
SELECTED_MESHES_ADR = "/local/disk1/fvalverde/openfoam-data/sphereCases/rocketMesh/rocketShort/noFinSupport/{}/constant/polyMesh"
SELECTED_MESHES     = ["R1", "R2", "R3", "R4", "R5"]
SELECTED_SOLVERS    = ["rhoPimpleFoam", "rhoCentralFoam", "rhoSimpleFoam"]
SELECTED_MA         = [0.6, 1.0, 1.5, 2.3, 4.63]
SELECTED_AOA        = [0, 8, 16]

GENERATE = {"rhoPimpleFoam": 1, "rhoCentralFoam": 1, "rhoSimpleFoam": 0}

CROSS_SECTION_AREAS = {0: 0.001282603306, 8: 0.001282603306, 16: 0.001282603306} # {0: 0.001282603306, 8: 0.00436352, 16: 0.00774068}

# Save Directory
SAVE_DIR = "/local/disk1/fvalverde/openfoam-data/sphereCases/run" # Used to set mapFields addresses

# Addresses Files - For Generation of Config Files
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
    "nprocessors": [1, 2, 2],
    "pressure": None,
    "temperature": None,
    "density": None,
    "Aref": None,
    "lRef": 0.05715,
    "coeffs_variation": None,
    "coeffs_range": None,
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
    "purgeWrite": 5,
    "turbulentKE": None,
    "turbulentOmega": None,
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

                bndsMaCase = bnds_file[bnds_file["Mach Number [-]"] == Ma].iloc[0]

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

                config_["turbulentKE"]  = bndsMaCase["Turbulent Kinetic Energy [m^2/s^2]"]
                config_["turbulentOmega"] = bndsMaCase["Turbulent Dissipation Rate [1/s]"]

                # Coefficients Wind Tunnel
                search = CA_windTunnel_file[CA_windTunnel_file["AoA"] == AoA].iloc[0]
                config_["Cd_windTunnel"]        = search["M{}_CA-ALPHA".format(Ma)]
                search = CN_windTunnel_file[CN_windTunnel_file["AoA"] == AoA].iloc[0]
                config_["Cl_windTunnel"]        = search["M{}_CN-ALPHA".format(Ma)]
                
                search = CM_windTunnel_file[CM_windTunnel_file["AoA"] == AoA].iloc[0]
                config_["CmPitch_windTunnel"]   = search["M{}_Cm-ALPHA".format(Ma)]

                config_["solver"] = solver

                # Cross Section Area
                config_["Aref"] = CROSS_SECTION_AREAS[AoA]

                # rhoCentralFoam Specific
                if config_["solver"] == "rhoCentralFoam" and GENERATE[config_["solver"]]:

                    # rhoCentralFoam Specific R1
                    config_R1 = rhoCentralFoam_specific_R1(copy(config_))
                    simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 1, solver)
                    path = folder_dir + "/config_" + simulation_name + ".json"
                    save(config_R1, path)


                    # # rhoCentralFoam Specific R2
                    # config_R2 = rhoCentralFoam_specific_R2(copy(config_), mapFields=simulation_name)
                    # simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 2, solver)
                    # path = folder_dir + "/config_" + simulation_name + ".json"
                    # save(config_R2, path)


                    # # rhoCentralFoam Specific R3
                    # config_R3 = rhoCentralFoam_specific_R3(copy(config_), mapFields=simulation_name)
                    # simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 3, solver)
                    # path = folder_dir + "/config_" + simulation_name + ".json"
                    # save(config_R3, path)


                    # # rhoCentralFoam Specific R4
                    # config_R4 = rhoCentralFoam_specific_R4(copy(config_), mapFields=simulation_name)
                    # simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 4, solver)
                    # path = folder_dir + "/config_" + simulation_name + ".json"
                    # save(config_R4, path)


                    # rhoCentralFoam Specific R5
                    config_R5 = rhoCentralFoam_specific_R5(copy(config_), mapFields=simulation_name)
                    simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 5, solver)
                    path = folder_dir + "/config_" + simulation_name + ".json"
                    save(config_R5, path)

                
                # rhoPimpleFoam Specific
                elif config_["solver"] == "rhoPimpleFoam" and GENERATE[config_["solver"]]:
                    
                    # rhoPimpleFoam Specific R1
                    config_R1 = rhoPimpleFoam_specific_R1(copy(config_))
                    simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 1, solver)
                    path = folder_dir + "/config_" + simulation_name + ".json"
                    save(config_R1, path)


                    # # rhoPimpleFoam Specific R2
                    # config_R2 = rhoPimpleFoam_specific_R2(copy(config_), mapFields=simulation_name)
                    # simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 2, solver)
                    # path = folder_dir + "/config_" + simulation_name + ".json"
                    # save(config_R2, path)


                    # # rhoPimpleFoam Specific R3
                    # config_R3 = rhoPimpleFoam_specific_R3(copy(config_), mapFields=simulation_name)
                    # simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 3, solver)
                    # path = folder_dir + "/config_" + simulation_name + ".json"
                    # save(config_R3, path)


                    # # rhoPimpleFoam Specific R4
                    # config_R4 = rhoPimpleFoam_specific_R4(copy(config_), mapFields=simulation_name)
                    # simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 4, solver)
                    # path = folder_dir + "/config_" + simulation_name + ".json"
                    # save(config_R4, path)


                    # rhoPimpleFoam Specific R5
                    config_R5 = rhoPimpleFoam_specific_R5(copy(config_), mapFields=simulation_name)
                    simulation_name = "Ma{}_AoA{}_R{}_{}".format(Ma, AoA, 5, solver)
                    path = folder_dir + "/config_" + simulation_name + ".json"
                    save(config_R5, path)
                    
                
                # rhoSimpleFoam Specific
                elif config_["solver"] == "rhoSimpleFoam" and GENERATE[config_["solver"]]:
                    continue


                # Error
                else:
                    print("Case ignored.")

    return 0


###########################
# rhoCentralFoam Specific #
###########################

def rhoCentralFoam_specific_R1 (config_):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[0])

    config_["vanLeer"]  = 2000
    config_["minIter"]  = 3000
    config_["final_Co"] = 0.32

    config_["coeffs_variation"] = [1e-3, 1e-3, 1e-2]
    config_["coeffs_range"]     = [300, 300, 300]
        
    return config_


def rhoCentralFoam_specific_R2 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[1])

    config_["vanLeer"]  = 1000
    config_["minIter"]  = 2000
    config_["final_Co"] = 0.32

    config_["coeffs_variation"] = [1e-3, 1e-3, 5e-3]
    config_["coeffs_range"]     = [50, 50, 50]

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields
    
    return config_


def rhoCentralFoam_specific_R3 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[2])

    config_["vanLeer"]  = 800
    config_["minIter"]  = 1700
    config_["final_Co"] = 0.32

    config_["coeffs_variation"] = [1e-3, 1e-3, 5e-3]
    config_["coeffs_range"]     = [50, 50, 50]

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields
    
    return config_


def rhoCentralFoam_specific_R4 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[3])

    config_["vanLeer"]  = 400
    config_["minIter"]  = 1300
    config_["final_Co"] = 0.32

    config_["coeffs_variation"] = [1e-3, 1e-3, 5e-3]
    config_["coeffs_range"]     = [50, 50, 50]

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields
    
    return config_


def rhoCentralFoam_specific_R5 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[4])

    config_["vanLeer"]  = 400
    config_["minIter"]  = 1300
    config_["final_Co"] = 0.32

    config_["coeffs_variation"] = [1e-3, 1e-3, 5e-3]
    config_["coeffs_range"]     = [50, 50, 50]

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields
    
    return config_


# ------------------------------------------------------------------------

##########################
# rhoPimpleFoam Specific #
##########################

def rhoPimpleFoam_specific_R1 (config_):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[0])

    config_["coeffs_variation"] = [1e-3, 1e-3, 1e-2]
    config_["coeffs_range"]     = [300, 300, 300]

    return config_


def rhoPimpleFoam_specific_R2 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[1])

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields

    config_["coeffs_variation"] = 1e-3
    config_["coeffs_range"]     = 50

    return config_


def rhoPimpleFoam_specific_R3 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[2])

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields

    config_["coeffs_variation"] = 1e-3
    config_["coeffs_range"]     = 50

    return config_


def rhoPimpleFoam_specific_R4 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[3])

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields

    config_["coeffs_variation"] = 1e-3
    config_["coeffs_range"]     = 50

    return config_


def rhoPimpleFoam_specific_R5 (config_, mapFields=None):

    config_["mesh_file"] = SELECTED_MESHES_ADR.format(SELECTED_MESHES[4])

    if mapFields:
        config_["map_file"] = SAVE_DIR + "/" + mapFields

    config_["coeffs_variation"] = [1e-3, 1e-3, 5e-3]
    config_["coeffs_range"]     = [50, 50, 50]

    return config_


# ------------------------------------------------------------------------
# Save JSON File
def save (config, path):
    with open(path, 'w') as outfile:
        json.dump(config, outfile, indent=2, separators=(',', ': '))
    return 0


# ------------------------------------------------------------------------
# Creates bash script to generate all cases in the folder from the configuration files
# bash runs as follows: ./template_run.sh <configuration file> <template/solver> <output folder>

# Expected generated bash script:
# ./template_run.sh config_1.json template1 output_folder
# ./template_run.sh config_2.json template1 output_folder
# ./template_run.sh config_3.json template1 output_folder
# ...

class GenerateFromTemplates ():

    def __init__ (self, config):
        self.config = config

        return None


    def generate (self):
        return None


if __name__ == "__main__":
    main()