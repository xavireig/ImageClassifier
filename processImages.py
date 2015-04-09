import numpy
from PIL import Image
import os
import pandas as pd
import pylab as pl
from sklearn.decomposition import RandomizedPCA
from sklearn.neighbors import KNeighborsClassifier

SIZE = (300, 150)
def img_to_matrix(filename):
    # takes a filename and turns it into a numpy array of RGB pixels
    img = Image.open(filename)
    img = img.resize(SIZE)
    img = list(img.getdata())
    # some images seem to be corrupt and fail here
    try:
        img = map(list, img)
    except:
        return -1
    img = numpy.array(img)
    return img
 
def flatten_image(img):
    # takes in an (m, n) numpy array and flattens it into an array of shape (1, m * n)
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return img_wide[0]

img_dir = "images/"
images_dir = [img_dir + f for f in os.listdir(img_dir)]

data = []
processed = 0
skipped = 0
normalized_size = 0

for dir in images_dir:
    for image in os.listdir(dir):
        image = dir + "/" + image
        img = img_to_matrix(image)
        # handling the case of error when processing images
        if isinstance(img, int):
            skipped += 1
            continue            
        else:
            img = flatten_image(img)
            processed += 1
            data.append(img)

# find any element with different size and remove it
same_size = len(data[0])
data_new = []
i = 0
for d in data:
    if len(d) == same_size:
        data_new.append(d)
        i += 1

data = data_new

data = numpy.array(data)
print len(data)
print str(processed) + " images processed and " + str(skipped) + " images skipped."

pca = RandomizedPCA(n_components=2)
X = pca.fit_transform(data)
df = pd.DataFrame({"x": X[:, 0], "y": X[:, 1]})
df["label"] = ["elephant","elephant","elephant","elephant","elephant", "elephant","elephant","elephant","elephant","elephant", "elephant","elephant","elephant","elephant","elephant", "elephant","elephant","elephant","elephant","elephant", "elephant", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe", "giraffe"]
print df
colors = ["red", "yellow"]

for label, color in zip(df['label'].unique(), colors):
    mask = df['label']==label
    pl.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)
    
pl.legend()
pl.show()