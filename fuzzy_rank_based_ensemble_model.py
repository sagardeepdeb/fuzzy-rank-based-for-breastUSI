# -*- coding: utf-8 -*-
"""Fuzzy rank based ensemble model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vIfRT25EM8Q4f8eHxWfakAYvogtbmfhH
"""

from google.colab import drive
drive.mount('/content/drive')

from keras import initializers,regularizers,optimizers
init =initializers.glorot_normal(seed=1)
bias_init =initializers.Constant(value=0.1)

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.utils import load_img, img_to_array, array_to_img
import pickle
import os
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from tensorflow.keras.optimizers import RMSprop,Adam
from tensorflow import keras 
from tensorflow.keras import layers
from keras.models import Model

from keras.preprocessing.image import ImageDataGenerator
from sklearn import model_selection
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix

#Data Augmentation
def augment(path,IMG_DIM):
  
  datagen = ImageDataGenerator(rotation_range=40,width_shift_range=.2,height_shift_range=.2,shear_range=.2,zoom_range=.2,horizontal_flip=True,fill_mode='nearest')

  #to list all directories in a specific folder
  directories = os.listdir(path)

  files_path = []
  labels = []
  for i in range(len(directories)):
    ls = []
    curPath = path +'/' +directories[i] + '/*'
    ls = glob.glob(curPath)
    temp = []
    for img in ls:
      x = img_to_array(load_img(img,target_size = IMG_DIM))
      x = x.reshape((1,)+x.shape)
      temp.append(x)
    
    i = 0
    target = 800
    for batch in datagen.flow(temp,batch_size=4,save_to_dir=curPath[:-1],save_format='jpg'):
      i += 1
      if len(ls) + i*4>800:
        break

#Creating Frame
def createFrame(path,IMG_DIM):
  train_imgs = []
  labels = []
  #getting all folder name
  directories = os.listdir(path)
  for i in range(len(directories)):
    ls = []
    temp = []
    curPath = path +'/' +directories[i] + '/*'
    #getting all files name
    ls = glob.glob(curPath)
    for img in ls:
      x = img_to_array(load_img(img,target_size = IMG_DIM))
      temp.append(x)

    #print(len(ls))
    train_imgs  = train_imgs + temp
    label = []
    label = [i]*len(ls)
    labels += label

  df = pd.DataFrame(list(zip(train_imgs,labels)))
  df = df.sample(frac = 1) 
  return df

def kFold(df):
  
  df['kfold'] = -1
  df = df.reset_index(drop=True)
  y = df[1]
  kf = model_selection.StratifiedKFold(n_splits=6)
  for f,(t_,v_) in enumerate(kf.split(X=df,y=y)):
    df.loc[v_,'kfold'] = f

  return df
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
#Customized CNN models
def DenseNet(train_imgs,train_labels,class_no,num_epochs=20):
  print("-------------------------------------DENSENET--------------------------------------------")
  input_shape_densenet = (IMG_WIDTH, IMG_WIDTH, 3)
  densenet_model = keras.applications.DenseNet169(include_top=False,weights="imagenet",input_tensor=None,input_shape=input_shape_densenet,pooling=None)
  densenet_model.trainable = True
  for layer in densenet_model.layers[:5]:
    layer.trainable=False
  for layer in densenet_model.layers[5:]:
    layer.trainable=True

  layer = keras.layers.Flatten()(densenet_model.output)
  layer = keras.layers.Dense(units=1024,activation='relu')(layer)
  layer = keras.layers.Dropout(0.5)(layer)
  layer = keras.layers.Dense(units=128,activation='relu')(layer)
  layer = keras.layers.Dense(units=class_no,activation='softmax')(layer)
  model = keras.models.Model(densenet_model.input, outputs=layer)
  model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001,beta_1=0.9,beta_2=0.999,epsilon=1e-07,amsgrad=False,name="Adam"),loss='categorical_crossentropy',metrics=['acc'])

  history = model.fit(train_imgs, train_labels, validation_data = (test_imgs, test_labels) , batch_size=32,callbacks=[callback], epochs=num_epochs,verbose=1)
  # summarize history for accuracy
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy of Densenet')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  print("------------------------------------------------------------------------------------------")
  return model

def VGG19(train_imgs,train_labels,class_no,num_epochs=20):
  print("-------------------------------------VGG19--------------------------------------------")
  input_shape_VGG19 = (IMG_WIDTH, IMG_WIDTH, 3)
  VGG19_model = keras.applications.VGG19(include_top=False,weights="imagenet",input_tensor=None,input_shape=input_shape_VGG19,pooling=None)
  VGG19_model.trainable = True
  for layer in VGG19_model.layers[:5]:
    layer.trainable=False
  for layer in VGG19_model.layers[5:]:
    layer.trainable=True

  layer = keras.layers.Flatten()(VGG19_model.output)
  layer = keras.layers.Dense(units=1024,activation='relu')(layer)
  layer = keras.layers.Dropout(0.5)(layer)
  layer = keras.layers.Dense(units=128,activation='relu')(layer)
  layer = keras.layers.Dense(units=class_no,activation='softmax')(layer)
  model = keras.models.Model(VGG19_model.input, outputs=layer)
  model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001,beta_1=0.9,beta_2=0.999,epsilon=1e-07,amsgrad=False,name="Adam"),loss='categorical_crossentropy',metrics=['acc'])

  history = model.fit(train_imgs, train_labels, validation_data = (test_imgs, test_labels) , batch_size=32,callbacks=[callback], epochs=num_epochs,verbose=1)
  # summarize history for accuracy
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy of VGG19')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  print("------------------------------------------------------------------------------------------")
  return model

def Inception(train_imgs,train_labels,test_imgs, test_labels,class_no,num_epochs=20):
  print("-------------------------------------INCEPTION-------------------------------------------")

  pre_trained_model2 = keras.applications.InceptionV3(input_shape = (IMG_WIDTH,IMG_WIDTH,3),include_top = False,weights='imagenet')
  for layer in pre_trained_model2.layers[:5]:
    layer.trainable=False
  for layer in pre_trained_model2.layers[5:]:
    layer.trainable=True
  x = keras.layers.Flatten()(pre_trained_model2.output)
  x = layers.Dense(1028,activation='relu')(x)
  x = layers.Dropout(0.5)(x)
  x = layers.Dense(64,activation='relu')(x)
  x = layers.Dense(class_no,activation='softmax')(x)
  model3 = Model(pre_trained_model2.input,x)
  model3.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001,beta_1=0.9,beta_2=0.999,epsilon=1e-07,amsgrad=False,name="Adam"),loss='categorical_crossentropy',metrics=['acc'])
  history = model3.fit(train_imgs, train_labels, validation_data = (test_imgs, test_labels) , batch_size=32,callbacks=[callback], epochs=num_epochs,verbose=1)
  # summarize history for accuracy
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy of Inception')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  print("-----------------------------------------------------------------------------------------")
  return model3
#Customized CNN models

def Xception(train_imgs,train_labels,test_imgs, test_labels,class_no,num_epochs=20):
  print("-------------------------------------XCEPTION---------------------------------------------")
  pre_trained_model = keras.applications.Xception(input_shape = (IMG_WIDTH,IMG_WIDTH,3), include_top=False,weights="imagenet")
  for layer in pre_trained_model.layers[:5]:
    layer.trainable=False
  for layer in pre_trained_model.layers[5:]:
    layer.trainable=True
  x = keras.layers.Flatten()(pre_trained_model.output)
  x = layers.Dense(256,activation='relu')(x)
  x = layers.Dropout(0.5)(x)
  x = layers.Dense(32,activation='relu')(x)
  x = layers.Dense(class_no,activation='softmax')(x)
  model1 = Model(pre_trained_model.input,x)
  model1.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001,beta_1=0.9,beta_2=0.999,epsilon=1e-07,amsgrad=False,name="Adam"),loss='categorical_crossentropy',metrics=['acc'])
  history = model1.fit(train_imgs, train_labels, validation_data = (test_imgs, test_labels) , batch_size=32,callbacks=[callback], epochs=num_epochs,verbose=1)
  # summarize history for accuracy
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('model accuracy of Xception')
  plt.ylabel('accuracy')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  # summarize history for loss
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.show()
  print("------------------------------------------------------------------------------------------")
  return model1

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
from keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.utils import load_img, img_to_array, array_to_img
import pickle
import os
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from tensorflow.keras.optimizers import RMSprop,Adam
from tensorflow import keras 
from tensorflow.keras import layers
from keras.models import Model

from keras.preprocessing.image import ImageDataGenerator
from sklearn import model_selection
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix


#Fuzzy Rank-based Ensemble:
def getScore(model,test_imgs):
  res = model.predict(test_imgs)
  return res 

def generateRank1(score,class_no):
  rank = np.zeros([class_no,1])
  scores = np.zeros([class_no,1])
  scores = score
  for i in range(class_no):
      rank[i] = 1 - np.exp(-((scores[i]-1)**2)/2.0)
  return rank

def generateRank2(score,class_no):
  rank = np.zeros([class_no,1])
  scores = np.zeros([class_no,1])
  scores = score
  for i in range(class_no):
      rank[i] = 1 - np.tanh(((scores[i]-1)**2)/2)
  return rank

def generateRank3(score,class_no):
  rank = np.zeros([class_no,1])
  scores = np.zeros([class_no,1])
  scores = score
  for i in range(class_no):
      rank[i] = 1/(1 + np.exp(-scores[i]))
  return rank

def doFusion(res0,res1,res2,res3,label,class_no):
  cnt = 0
  id = []
  for i in range(len(res1)):
      rank0 = generateRank1(res0[i],class_no)*generateRank2(res0[i],class_no)*generateRank3(res0[i],class_no)
      rank1 = generateRank1(res1[i],class_no)*generateRank2(res1[i],class_no)*generateRank3(res0[i],class_no)
      rank2 = generateRank1(res2[i],class_no)*generateRank2(res2[i],class_no)*generateRank3(res0[i],class_no)
      rank3 = generateRank1(res3[i],class_no)*generateRank2(res3[i],class_no)*generateRank3(res0[i],class_no)
      rankSum = rank0 + rank1 + rank2 + rank3
      rankSum = np.array(rankSum)
      scoreSum = 1 - (res0[i] + res1[i] + res2[i] + res3[i])/4
      scoreSum = np.array(scoreSum)
      
      fusedScore = (rankSum.T)*scoreSum
      cls = np.argmin(rankSum)
      if cls<class_no and label[i][cls]== 1:
          cnt += 1
      id.append(cls)
  print(cnt/len(res1))
  return id

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
from keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.utils import load_img, img_to_array, array_to_img
import pickle
import os
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from tensorflow.keras.optimizers import RMSprop,Adam
from tensorflow import keras 
from tensorflow.keras import layers
from keras.models import Model

from keras.preprocessing.image import ImageDataGenerator
from sklearn import model_selection
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix

'''
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_directory', type=str, default = '.', help='Directory where the image data is stored')
parser.add_argument('--epochs', type=int, default = 20, help='Number of Epochs of training')
args = parser.parse_args()
'''
path1 = "/content/drive/MyDrive/BUSI/"
if path1[-1]=='/':
  path1 = path1[:-1]

num_epochs = 50

IMG_WIDTH=128
IMG_HEIGHT=128
IMG_DIM = (IMG_WIDTH, IMG_HEIGHT,3)

df = createFrame(path1,IMG_DIM)
df = kFold(df)

target_names = os.listdir(path1)
num_classes = len(target_names)

df

import sklearn.metrics as metrics
num_epochs = 100
for i in range(1,6):
  print(f"----------------------------------------------------FOLD NO {i}-------------------------------------------------------")
  dfTrain = df[df['kfold']!=i]
  dfTest = df[(df['kfold']==i)] 
  train_imgs = list(dfTrain[0])
  train_imgs = np.array(train_imgs)
  train_imgs = train_imgs/255
  train_labels = np.array(dfTrain[1])
  encoder = LabelEncoder()
  encoder.fit(train_labels)
  train_labels = encoder.transform(train_labels)
  train_labels = np_utils.to_categorical(train_labels)

  test_imgs = list(dfTest[0])
  test_imgs = np.array(test_imgs)
  test_imgs = test_imgs/255
  test_labels = np.array(dfTest[1])
  encoder = LabelEncoder()
  encoder.fit(test_labels)
  test_labels = encoder.transform(test_labels)
  test_labels = np_utils.to_categorical(test_labels)
  model0 = VGG19(train_imgs,train_labels,class_no=num_classes,num_epochs=num_epochs)
  #VGG19(train_imgs,train_labels,class_no,num_epochs=20)
  model1 = DenseNet(train_imgs,train_labels,class_no=num_classes,num_epochs=num_epochs)
  model2 = Inception(train_imgs,train_labels,test_imgs, test_labels,class_no=num_classes,num_epochs=num_epochs)
  model3 = Xception(train_imgs,train_labels,test_imgs, test_labels,class_no=num_classes,num_epochs=num_epochs)
  print("BASE LEARNERS ACCURACY-----------0.VGG19 1.DENSENET 2.INCEPTION 3.XCEPTION")

  model0.evaluate(test_imgs, test_labels, batch_size=32)
  model1.evaluate(test_imgs, test_labels, batch_size=32)
  model2.evaluate(test_imgs, test_labels, batch_size=32)
  model3.evaluate(test_imgs, test_labels, batch_size=32)

  res0 = model0.predict(test_imgs) 
  res1 = model1.predict(test_imgs)
  res2 = model2.predict(test_imgs) 
  res3 = model3.predict(test_imgs)
  predictedClass = doFusion(res0,res1,res2,res3,test_labels,class_no=num_classes)

  leb0 = np.argmax(res0,axis=-1) 
  leb1 = np.argmax(res1,axis=-1)
  leb2 = np.argmax(res2,axis=-1)
  leb3 = np.argmax(res3,axis=-1)
  actual = np.argmax(test_labels,axis=-1)
  
  print('VGG19 base learner')
  print(classification_report(actual, leb0,target_names = target_names))
  confusion_matrix = metrics.confusion_matrix(actual, leb0)
  cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = target_names)
  cm_display.plot()
  plt.show()
  print('Densenet-169 base learner')
  print(classification_report(actual, leb1,target_names = target_names))
  confusion_matrix = metrics.confusion_matrix(actual, leb1)
  cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = target_names)
  cm_display.plot()
  plt.show()
  print('Inception base learner')
  print(classification_report(actual, leb2,target_names = target_names))
  confusion_matrix = metrics.confusion_matrix(actual, leb2)
  cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = target_names)
  cm_display.plot()
  plt.show()
  print('Xception base learner')
  print(classification_report(actual, leb3,target_names = target_names))
  confusion_matrix = metrics.confusion_matrix(actual, leb3)
  cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = target_names)
  cm_display.plot()
  plt.show()
  print('Ensembled')
  print(classification_report(actual, predictedClass,target_names = target_names))
  confusion_matrix = metrics.confusion_matrix(actual, predictedClass)
  cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = target_names)
  cm_display.plot()
  plt.show()


  print(f"--------------------------------------------------END OF FOLD NO {i}--------------------------------------------------------")