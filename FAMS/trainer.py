import os
import cv2
import numpy as np
from PIL import Image

# import pil
# from pil.image import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataset'
if not os.path.exists('./recognizer'):
    os.makedirs('./recognizer')


def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    face = []
    ids = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        face.append(faceNp)
        ids.append(ID)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return np.array(ids), face


Ids, face = getImagesWithID(path)
recognizer.train(face, Ids)
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
