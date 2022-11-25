## ResNet50 Pneumonia CLassifier

If you are new to Deep Learning, feel free to take a look at the following resources.

**What are Neural Networks?** <br>
* [3Blue1Brown](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) (Recommended)
* [IBM Technology](https://www.youtube.com/watch?v=jmmW0F0biz0&ab_channel=IBMTechnology) (Short Explanation)

**What is a Convolutional Neural Network?**
* [codebasics](https://www.youtube.com/watch?v=zfiSAzpy9NM&ab_channel=codebasics) (Recommended)
* [IBM Technology](https://www.youtube.com/watch?v=QzY57FaENXg&ab_channel=IBMTechnology) (Short Explanation)

**What is ResNet architecture?**
* [Original Paper](https://arxiv.org/abs/1512.03385) (Basic understanding of Conv-net required)
* [Understanding and Visualizing ResNets](https://towardsdatascience.com/understanding-and-visualizing-resnets-442284831be8)


### ResNet-50 Classifier 
ResNet-50 is a type of a Convolutional Neural Net architecture that was developed to solve the problem of ***Vanishing gradient*** in larg CNN models. We will use a pre-trained model from [Tensorflow](https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet50/ResNet50). We will freeze the base layer, add custom top layers and train the top-most layers only. Once the model is trained, metrics are collected to fine-tune the model as needed. Finally, we will use a [Grad-Cam](https://keras.io/examples/vision/grad_cam/) to visualize where the model "looks at" to make predictions.

<img src="/viral-pneumonia.jpeg" width=250px height=250px> <img src="/pn2.jpg" width=250px height=250px>


*Note: The project was built on Google Colab. It is recommended you run the notebook on Colab. Building and training large CNN models is resource intensive. If you chose to run the model locally, please ensure there is sufficient hardware (GPU) to run the workload.*
