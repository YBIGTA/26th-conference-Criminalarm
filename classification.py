from tensorflow import keras
import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
import matplotlib.pyplot as plt
tf.compat.v1.set_random_seed(0)
from tensorflow import keras
import numpy as np
np.random.seed(0)
import itertools
from keras.preprocessing.image import image_dataset_from_directory
import os
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
import matplotlib.pyplot as plt
from PIL import Image
import json

model_path = './classification_model/classification_model.keras'
input_path = './input/input.png'
output_dir = './output/'

class_names = ['Apple___Black_rot',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite',
 'Tomato___Target_Spot',
 'Tomato___healthy']


# model load
def load_model(model_path = model_path):
    model = keras.models.load_model(model_path)
    return model



# classification
# 일단 하드코딩으로 항상 스킨답서스가 레이블로 나오도록 해놨어요 
# -> 실제 prediction 진행하려면 hard_coding=False로 변경

def predict_disease_and_recommend(input_path, save_output=True, hard_coding=True): 
    model = load_model()
    # Load and preprocess image
    img = tf.keras.preprocessing.image.load_img(input_path, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension

    # Predict
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    # pesticide = disease_to_pesticide.get(predicted_class, "No data available")


    if save_output:
        if hard_coding:
            result = {'diseases':'Scindapsus___healthy',
              'cause':'llm으로 채워야함1',
              'solution':'llm으로 채워야함2'}

        else:
            result = {'diseases':predicted_class,
              'cause':'llm으로 채워야함1',
              'solution':'llm으로 채워야함2'}
             
        with open(output_dir+'result.json','w') as f:
            json.dump(result)

    plt.show()



# run model
predict_disease_and_recommend(input_path, save_output=True, hard_coding=True)