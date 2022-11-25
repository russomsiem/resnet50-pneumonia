# -*- coding: utf-8 -*-
"""ResNet50-pneumonia-classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T7TexCtuAV6c2qesFmCntf6Y7ytyRzY2

Author: Siem Russom
Date: 10/4/2021
Description: ResNet-50 architecture CNN model to classify pneumonia in pediatric
            chest x-ray images.
"""

# Commented out IPython magic to ensure Python compatibility.
# Improt libraries
"""
The following libraries are required:

  - Tensorflow 2.0: Must be Tensorflow 2.0 since the model required Keras API
  - sklearn
  - Ipython
  - matplotlib
  - cv2
  - numpy
  - seaborn

The following are recommnded if working on Google Colab
  * os
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import  Conv2D,MaxPooling2D,Activation,Dropout,Flatten,Dense,BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
from IPython.display import Image, display
from sklearn.metrics import precision_recall_curve, roc_curve, accuracy_score,recall_score,precision_score,confusion_matrix, classification_report
from sklearn.decomposition import PCA
from sklearn.model_selection import  train_test_split

import numpy as np
import cv2

import datetime

# %matplotlib inline
# %load_ext tensorboard

"""
Get dataset and resize such that each image has 224x224 dimension
"""
labels = ['PNEUMONIA', 'NORMAL']
img_size = 224
def get_training_data(data_dir):
    data = [] 
    for label in labels: 
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img),cv2.IMREAD_COLOR )
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) 
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

"""
Split dataset into:
  - train: dataset to train model
  - test: dataset to test model for accuracy
  - val: dataset to validate model and tune parameters
"""
train = get_training_data('[REPLACE WITH PATH FOR TRAINING SET]')
test = get_training_data('[REPLACE WITH PATH FOR TEST SET]')
val = get_training_data('[REPLACE WITH PATH FOR VALIDATION SET]')

"""
Plot and visualize 2 images
"""
plt.figure(figsize=(5,5))
plt.imshow(train[1][0], cmap='gray')
plt.title(labels[train[1][1]])


plt.figure(figsize=(5,5))
plt.imshow(train[-1][0], cmap='gray')
plt.title(labels[train[-1][1]])

"""
  - x axis - Input to neural network
  - y axis - corresponding output

  Normalization is a transformation technique to ensure the dataset is on the same 
  scale. 
"""
X = []
y = []

for img, label in test:
  X.append(img)
  y.append(label)

for img, label in train:
  X.append(img)
  y.append(label)

for img, label in val:
  X.append(img)
  y.append(label)


#Reshape images 
X = np.array(X).reshape(-1,img_size,img_size,3)

# Normalise images
X = X/255
y = np.array(y)


x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.20, random_state=30)

print("Shape of x_train: ",x_train.shape)
print("Shape of y_train: ", y_train.shape)
print("Shape of x_test: ",x_test.shape)
print("Shape of y_test: ", y_test.shape)
print("Shape of x_val: ",x_val.shape)
print("Shape of y_val: ", y_val.shape)

"""
Data augmentation is a transformation technique to prevent the model from 
overfitting, ie learning dataset-specific patterns. We achieve this by slighly 
modifying each image like flipping, zooming, etc.
"""
aug_x_train = ImageDataGenerator(
    zoom_range = 0.02, #random zoom 20%
    horizontal_flip = True, # random horizontal flip
    width_shift_range = 0.1
    )
aug_x_train.fit(x_train)

"""Define and build model

- The architecture used for this particular model is Resnet-50. Resnet or
Residual Neural Network is a type of Convolutional Neural Network that was 
created to solve the problem of exploding and vanishing gradient descent in deeper
networks.
  Refer to this article for more: https://towardsdatascience.com/resnets-why-do-they-perform-better-than-classic-convnets-conceptual-analysis-6a9c82e06e53

- Since a pre-trained model is being used, the base layers will be frozen
      with only the top layers being trained. This is done to avoid updating
      the weights of the pre-trained model.

"""

model_d= ResNet50(weights='imagenet',include_top=False, input_shape=(224, 224, 3)) 

#Freeze all base layers
model_d.trainable = False

x= model_d.output

#Add the necessary top layers
x= GlobalAveragePooling2D()(x)
x= BatchNormalization()(x)
x = Dropout(0.6)(x)
x= Dense(512,activation='relu')(x) 
x= BatchNormalization()(x)
x= Dense(325,activation='relu')(x) 
x= BatchNormalization()(x)
x= Dropout(0.70)(x)
preds=Dense(1,activation='sigmoid')(x) #FC-layer

model=Model(inputs=model_d.input,outputs=preds)


lay = []
for layer in model.layers:
    lay.append(layer.name)
    print(layer)

ADAM = Adam(learning_rate=0.0001)
LOSS = 'binary_crossentropy'
METRIC = ['acc']

model.compile(optimizer=ADAM, loss=LOSS, metrics=METRIC)
es = EarlyStopping(monitor = 'val_loss', patience = 5, verbose = 1)
model.summary()

"""
Tensorboard is a powerful visualization and measurement tool. To use it with
this model, uncomment the subsequent two lines. For the purposes of this model,
Tensorboard is optional.
"""
# logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
# tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)

BS = 35 #define batch size
EPOCHS = 50 #define the number of epochs

history = model.fit(x_train, y_train, batch_size=BS,
                     validation_data = (x_val, y_val),
                    epochs = EPOCHS, verbose = 1)

# Evaluate model on test data
model.evaluate(x_test, y_test)

# Visualize model accuracy and loss

""" 
Refer to the link below to learn what model accuracy and loss means
(https://machine-learning.paperspace.com/wiki/accuracy-and-loss)

"""
fig, ax = plt.subplots(1, 2, figsize=(10, 3))
ax = ax.ravel()

for i, met in enumerate(['acc', 'loss']):
    ax[i].plot(history.history[met])
    ax[i].plot(history.history['val_' + met])
    ax[i].set_title('Model {}'.format(met))
    ax[i].set_xlabel('epochs')
    ax[i].set_ylabel(met)
    ax[i].legend(['train', 'val'])

# Predict outputs and plot a Confusion Matrix
"""

Refer to the link below to learn what a Confusion Matrix is
(https://machine-learning.paperspace.com/wiki/confusion-matrix)

"""
pred = model.predict(x_train)
precisions, recalls, thresholds = precision_recall_curve(y_train, pred)
predictions = model.predict(x_test)

binary_predictions = []
threshold = thresholds[np.argmax(precisions >= 0.80)]
for i in predictions:
    if i >= threshold:
        binary_predictions.append(1)
    else:
        binary_predictions.append(0) 


matrix = confusion_matrix(binary_predictions, y_test)
plt.figure(figsize=(7, 7))
ax= plt.subplot()
sns.heatmap(matrix, annot=True, ax = ax)

# labels, title and ticks
ax.set_xlabel('Predicted Labels', size=20)
ax.set_ylabel('True Labels', size=20)
ax.set_title('Confusion Matrix', size=20) 
ax.xaxis.set_ticklabels(labels)
ax.yaxis.set_ticklabels(labels)

"""
  One challenging problem with Deep Learning models is that they behave like 
  black boxes. It is incredibly difficult to have a comprehensive understanding
  of how each neuron works with other neurons to achive the final output once
  trained. 

  Judging from the accuracy + loss plot and confusion matrix, this model is
  incredibly accurate. But without understanding what the model is "looking" at,
  it would be incredibly risky to deploy the model.

  To combat this problem, we will use a Grad-cam(Gradient-weighted Class Activation Mapping).  
  Grad-cam uses a target (output) of the last Convolutional layer to produce
  a localization map to highlight the important regions of the image, or
  what the model is "looking" when it produces a prediction. 

  The code below creates grad-cam, saves image, and display it.

  For further explanation and detailed implementation walk-through, refer to
  the link below.
  (https://keras.io/examples/vision/grad_cam/) 

"""


from keras import backend as K

# Image path
img_path = "[REPLACE WITH PATH FOR TEST IMAGE]"


# Load image and convert to tensor of shape (sample,h,w,c)
img = tf.keras.utils.load_img (img_path, target_size=(224, 224))
img_tensor = tf.keras.utils.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)


# Normalize
img_tensor /= 255.


# store predictions for the image
m_pred = model.predict(img_tensor)

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    #create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )


    # compute the gradient of the prediction for the image with respect the the last conv layer activation
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    
    # get gradient of output neuron with respect to last conv layer output feature map
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # the mean intensity of gradient for specific channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    
    # multiply each chanel in feature map array with channel prediction importance,
    # then sum across all chanels to generate class activation map
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # normalize heatmap 
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

heatmap = make_gradcam_heatmap(img_tensor, model, 'conv5_block3_out')

# Display heatmap


def save_and_display_gradcam(img_path, heatmap, alpha=0.4):
    # Load image
    img = keras.preprocessing.image.load_img(img_path)
    img = keras.preprocessing.image.img_to_array(img)

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # image with RGB colorized heatmap
    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)

    # Superimpose the heatmap 
    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)

    superimposed_img.save("[REPLACE WITH PATH FOR SAVING IMAGE]")
    # Display heatmap
    display(Image("[REPLACE WITH THE ABOVE PATH]", width=255,height=255))


save_and_display_gradcam(img_path, heatmap)