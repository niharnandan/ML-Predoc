from scipy.io import loadmat
from datetime import datetime
import pandas as pd
import numpy as np
import sys

args = str(sys.argv)
min_face_score = int(args[1]) if len(sys.argv) == 2 else 0

print("CREATING CSV DATASET")

def calc_age(taken, dob):
    # From paper
    birth = datetime.fromordinal(max(int(dob) - 366, 1))
    # assume the photo was taken in the middle of the year
    return taken - birth.year if birth.month < 7 else taken - birth.year - 1

def get_meta(mat_path, db):
    meta = loadmat(mat_path)
    full_path = meta[db][0, 0]["full_path"][0]
    dob = meta[db][0, 0]["dob"][0]  # Matlab serial date number
    gender = meta[db][0, 0]["gender"][0]
    photo_taken = meta[db][0, 0]["photo_taken"][0]  # year
    face_score = meta[db][0, 0]["face_score"][0]
    second_face_score = meta[db][0, 0]["second_face_score"][0]
    age = [calc_age(photo_taken[i], dob[i]) for i in range(len(dob))]

    return full_path, dob, gender, photo_taken, face_score, second_face_score, age

db = 'wiki'
mat_path = "data/wiki_crop/wiki.mat"
var = ["full_path", "dob", "gender", "photo_taken", "face_score", "second_face_score", 'age']
data = get_meta(mat_path, db)
d = {}
for i in var: d[i] = data[var.index(i)]

df_wiki = pd.DataFrame(data=d)

db = 'imdb'
mat_path = "data/imdb_crop/imdb.mat"
data = get_meta(mat_path, db)
d = {}
for i in var: d[i] = data[var.index(i)]

df_imdb = pd.DataFrame(data=d)

df = df_wiki.append(df_imdb, ignore_index=True)

df.to_csv('data/data.csv', index=False)

df_clean = df.loc[(df['age'] <= 100) & (df['age'] >= 0) & (np.isnan(df['second_face_score'])) & (~np.isnan(df['gender'])) & (df['face_score'] >= min_face_score)]

df_clean.to_csv('data/data_clean.csv', index=False)

print('DONE, Press any key to continue')
t = input()

exit()