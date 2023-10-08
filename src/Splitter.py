import os
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil

csv_file = "images.csv"
data = pd.read_csv(csv_file)

data = data.groupby('label').filter(lambda x: len(x) > 1)

# dela upp datasetet
train_data, temp_data = train_test_split(data, test_size=0.3, random_state=42, stratify=data['label'])
val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42, stratify=temp_data['label'])

train_data.to_csv("train.csv", index=False)
val_data.to_csv("val.csv", index=False)
test_data.to_csv("test.csv", index=False)

# skapa mappar för träning, validation och test
train_dir = "train"
val_dir = "val"
test_dir = "test"

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# för att flytta bilderrna till deras tillhörande mapp
def move_images(data, target_dir):
    for index, row in data.iterrows():
        img_path = row['image_path']
        label = row['label']
        dest_dir = os.path.join(target_dir, str(label))
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(img_path, dest_dir)

move_images(train_data, train_dir)
move_images(val_data, val_dir)
move_images(test_data, test_dir)

