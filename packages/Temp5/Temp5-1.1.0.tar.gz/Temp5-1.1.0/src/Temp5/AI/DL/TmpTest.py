#In the name of GOD

import keras
import wx
import wx.dataview
import PIL.Image as pil

import tensorflow as tf

wx.FindWindowByName()
wx.Choice.GetStringSelection()
wx.Choice.SetStringSelection()
wx.Panel.Destroy()

wx.Bitmap.FromBuffer()
pil.fromarray().save()
wx.DC.DrawBitmap()

wx.CheckBox.GetValue()


from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout, Input
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.layers import ReLU
from keras import layers



imodel = Sequential()
imodel.add(keras.Input(shape=(200,200,3)))
Conv2D(filters=16,kernel_size=(4,4),strides=(1,1),padding='valid',activation=None)
Dense(units=16, activation=None)
MaxPool2D(pool_size=(2,2),strides=None,padding='valid')
Dropout(rate=0.4,noise_shape=None,seed=None)
Flatten()



ReLU(max_value=None,negative_slope=0,threshold=0)

VGG16(weights="imagenet", include_top=False, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),pooling=None
      ,classes=1000,classifier_activation="softmax")
VGG19(weights="imagenet", include_top=False, input_shape=(200,200,3),pooling=None,
      classes=1000,classifier_activation="softmax")

imodel.summary()
imodel.add(Dropout())
imodel.fit( x=None,y=None,batch_size=None,epochs=1,verbose='auto',callbacks=None, #{on_train_begin, on_epoch_begin, on_train_batch_begin, on_train_batch_end, on_epoch_end, on_train_end}
            validation_split=0.,validation_data=None,shuffle=True,class_weight=None,sample_weight=None,
            initial_epoch=0,steps_per_epoch=None,validation_steps=None,validation_batch_size=None,
            validation_freq=1,max_queue_size=10,workers=1,use_multiprocessing=False)

from keras.models import Functional
from keras.layers import AveragePooling2D

fmodel = keras.models.Functional()

fmodel.layers.append()

from six.moves import _thread

_thread.start_new_thread()

wx.EVT_THREAD