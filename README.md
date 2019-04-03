# BIM2SAM.AI
Building Information Models (BIM) to Structural Analysis Models (SAM) Using Artificial Intelligence

![image](Documents/BIM2SAM.png)

### Build instructions
##### 1. Build the SAMBuilder and TclBuilder excutables

```
sh build
```
##### 2. Install Tensorflow if you haven't. 

```
pip install tensorflow
```
###### Or do it in a virtual environment (virtualenv is recommended.) Tensorflow does not work with Python 3.7 or above at the time this code is made, so Python 3.6 is recommended. 

### Training the neural net
```
cd Python/NeuralNets
python BIM2FeaturesNN_V1.py
```
### Use the neural net in a BIM->SAM->tcl pipeline. This will generate a tcl file that can be run in OpenSees:
```
cd Python
python main.py
```

### Working notes and Ongoing developments:
[Notes:](../master/Documents/WorkingNote.pptx)
