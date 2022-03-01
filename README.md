# image-recognition-vs-dl-model
Test out your image recognition against a trained convolutional neural network (CNN) model via tkinter 
and see how well you stack up classifying grainy, greyscale 28x28 images.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ivanlieu/image-recognition-jupyter/HEAD?labpath=image-recog-jupyter.ipynb)

[A jupyter notebook port][image-recon-jupyter] is also available. Try in-browser by launching the binder badge above.

## About the Image Dataset
The images used for classifying that you and the CNN model will go head-to-head with are from 
the [Fashion MNIST][FMNIST] test database from Zalando Research. These test images have not been used to
train the CNN model as the model and yourself will be seeing these for the very first time.

## About the Model
### Model Construction
The deep learning model consists of 2 convolutional+ReLU layers with pooling and 2 fully connected 
layers (FCL) with xavier uniforms on initialization implemented using [PyTorch][PyTorch]. Dropout of p=0.15 is used 
on the first FCL. 

### Hyperparameters
- Criterion -- log(softmax) and non-linear likelihood loss functions 
- Optimizer -- Adam
- Learning rate -- 0.001

### Training
Training was conducted using the Fashion MNIST training database with shuffling and random horizontal 
flips (p=0.3) under 50 epochs of training. Final testing accuracy of the trained model on the entire 
Fashion MNIST testing dataset was 91.78%.

## About the Program
The python program runs a tkinter window instance for user interface where the following is displayed:
- Fashion MNIST image to be classified
- Correct clothing type from the previous image
- Buttons displaying clothing types to choose from
- User score bar and score % for image reocgnition accuracy
- Deep learning model score bar and score % for image recognition accuracy
- Total number of user correct images, deep learning model correct images, and total number of images

### Running the Program
Having all files in the same directory, start the program by running `main.py` which will open the
following tkinter UI window:

![uiWindow](https://i.imgur.com/G442PNH.png)

Clicking on any of the buttons to select the clothing type that is in the image above will update the window
contents for the next image to identify and update the score on whether the selected clothing type was correct.
### Requirements
This program was developed in python 3.7 and uses the following python packages:
- [PyTorch][PyTorch] 1.10.2 -- CUDA 11.3
- [Matplotlib][matplotlib] 3.5.1

Other versions of python, PyTorch, and Matplotlib have not been tested and may also run the program. If the program
does not run, verify installation versions match above.

## License
MIT

Free for me, free for you!

[image-recon-jupyter]: <https://github.com/ivanlieu/image-recognition-jupyter>
[FMNIST]: <https://github.com/zalandoresearch/fashion-mnist>
[PyTorch]: <https://pytorch.org/>
[matplotlib]: <https://matplotlib.org/stable/index.html>
