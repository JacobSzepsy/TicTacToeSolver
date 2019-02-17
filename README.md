# Why we did it
With AI and specifically machine learning being a fast growing technology we wanted to learn more about it and get first hand experience in working with a program that utilizes these concepts.
# What does it do?
This program utilizes a neural network to train a computer to be able to play a human in tic tac toe.
# How does it work?
To create the neural network the keras framework is utilized with tensorflow as a backend. The network consists of an input layer with 18 input nodes and a single node output layer and uses a linear model rather than utilizing an activation function. For the loss function the mean squared error loss function is used.

The network was first trained in the train.py program through reinforced learning by assessing how it played against an opponent and having it adjust the weight values accordingly. Once thorougly trained the model was then put into use against a human player in play.py. TTTmodel.h5 is a save file of the trained neural network to allow it to be ported from train.py to play.py.
# Results
Below are images of the win rates gathered during two different times training the neural network using different amounts of data.
**Improvement in win-rate when trained on 10,000 games (~30% increase)**
![10k game training](https://i.gyazo.com/119678b3fdfa606144988e8cc6bee205.png)
**Improvement in win-rate when trained on 20,000 games (~18% increase)**
![20k game training](https://i.gyazo.com/69e716c22038b7b32929072da2ccec98.jpg)
