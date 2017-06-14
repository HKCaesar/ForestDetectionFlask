from load import * 
from predict import * 
import keras.models

model = init()
predict("temp.jpg",model)
