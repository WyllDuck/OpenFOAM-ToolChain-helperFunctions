from os import listdir
from os.path import isfile, join

from scipy.interpolate import CubicSpline
import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2

SIZE = 5

# get file path with os
GLOBAL_DIR = os.path.dirname(os.path.abspath(__file__))



def read_file (file_path):

    with open(file_path, "r") as file:

        lines = file.readlines()
        img_path = GLOBAL_DIR + "/graphs/" + lines[0].replace("\n", "")
        image = cv2.imread(img_path)
        
        p0 = lines[1].split(" ")
        p1 = lines[2].split(" ")

        p0 = [eval("np.array({})".format(p.replace("\n",""))) for p in p0]
        p1 = [eval("np.array({})".format(p.replace("\n",""))) for p in p1]

        x, y = p0[0]
        cv2.line(image, (x+SIZE, y+SIZE), (x-SIZE, y-SIZE), (255, 0, 0), 3)
        cv2.line(image, (x+SIZE, y-SIZE), (x-SIZE, y+SIZE), (255, 0, 0), 3)

        cv2.putText(image, str(p0[1]), p0[0], font,
				    fontScale, color, thickness, cv2.LINE_AA)

        x, y = p1[0]
        cv2.line(image, (x+SIZE, y+SIZE), (x-SIZE, y-SIZE), (255, 0, 0), 3)
        cv2.line(image, (x+SIZE, y-SIZE), (x-SIZE, y+SIZE), (255, 0, 0), 3)

        cv2.putText(image, str(p1[1]), p1[0], font,
				    fontScale, color, thickness, cv2.LINE_AA)
        
        # File Name
        cv2.putText(image, file_path.split("/")[-1], (50,100), font,
				    fontScale, color, thickness, cv2.LINE_AA)

        points = [ eval("np.array({})".format(p.replace("\n",""))) for p in lines[4:] if p != "\n"]
        points = np.array(points)

        for x,y in points:
            cv2.line(image, (x+SIZE, y+SIZE), (x-SIZE, y-SIZE), (0, 0, 255), 3)
            cv2.line(image, (x+SIZE, y-SIZE), (x-SIZE, y+SIZE), (0, 0, 255), 3)
            
        # Showing the image
        if False:
            cv2.imshow('image', image)
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Save Image
        save_path = GLOBAL_DIR + '/check_images/' + file_path.split("/")[-1].replace(".txt", "") + "_" + lines[0].split(".")[0] + ".png"
        isWritten = cv2.imwrite(save_path, image)
        if isWritten:
            print("Image SUCCESSFULLY saved to: \n\t {}".format(save_path))
        else:
            print("FAILED to save image to: \n\t {}".format(save_path))

        return points, p0, p1


if __name__ == "__main__":

    allFiles = [f for f in listdir(GLOBAL_DIR + "/points") if isfile(join(GLOBAL_DIR + "/points", f))]

    # if folder "check_images" does not exist, create it
    if not os.path.exists(GLOBAL_DIR + "/check_images"):
        os.makedirs(GLOBAL_DIR + "/check_images")

    START = -8
    STOP = 24
    STEP = 0.1

    AoA_study = np.linspace(START, STOP, int((STOP-START)/STEP + 1))
    data = np.zeros([len(AoA_study), len(allFiles) + 1])
    data[:,0] = AoA_study

    header = ["AoA"]
    idx = 1

    for file in allFiles:
        points, p0, p1 = read_file(GLOBAL_DIR + "/points/" + file)

        step = abs(p0[1] - p1[1]) / abs(p0[0] - p1[0])
        points = (points - p1[0]) * step
        points[:,1] = -points[:,1] # invert y, in an image, y is inverted.
        points += p1[1]

        spl = CubicSpline(points[:,0], points[:,1], extrapolate=False)

        data[:,idx] = spl(AoA_study)
        title = file.replace(".txt", "")
        header.append(title)

        plt.scatter(points[:,0], points[:,1])
        plt.plot(AoA_study, data[:,idx])
        plt.grid()
        plt.title(title)
        plt.xlabel("AoA")
        
        plot_path = GLOBAL_DIR + "/check_images/" + title + ".png"
        plt.savefig(plot_path)
        plt.clf() # clean plot

        idx += 1

    # Make 3 files for each type CA, CN, Cm
    groups = ["CA", "CN", "Cm"]

    # Split in groups
    header_ = [[],[],[]]
    cols_   = [[],[],[]]
    for i in range(len(header)):
        if groups[0] in header[i]:
            header_[0].append(header[i])
            cols_[0].append(i)
        elif groups[1] in header[i]:
            header_[1].append(header[i])
            cols_[1].append(i)
        elif groups[2] in header[i]:
            header_[2].append(header[i])
            cols_[2].append(i)
        else: 
            print("ERROR! Header '{}' does not belong to any group".format(header[i]))

    for i in range(len(groups)):

        # force 0 deg to be null (for CN and Cm)
        if groups[i] != "CA":
            idx = np.where(data[:,0] == 0)[0][0]
            data[idx,:] = 0

        data_ = data[:,[0] + cols_[i]]
        df = pd.DataFrame(data_)

        # Save to File
        data_path = GLOBAL_DIR + "/" + "{}_coefficients.csv".format(groups[i])
        print("data saved to: {}".format(data_path))
        df.to_csv(data_path, header=["AoA"] + header_[i], index=None)