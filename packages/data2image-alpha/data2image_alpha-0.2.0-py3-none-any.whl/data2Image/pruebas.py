from supertml import supert
from models import tinto


model=tinto(problem="regression")
data="C:\\Users\\Borja\\PycharmProjects\\TINTORERA\\Datasets\\iris.csv"
folder="C:\\Users\\Borja\\PycharmProjects\\TINTORERA\\ResultadosEjemplos\\IGTD\\Generic"
#model.generateImages(data,folder)


import pandas as pd
from igtd import IGTD

model1 = IGTD()
model1.generateImages(data, folder)

    # generateImages(min_max_transform(data.values[:, :-1]), (4, 3), "Pearson", "Euclidean", 100, 6, 6, normDir, "squared")
