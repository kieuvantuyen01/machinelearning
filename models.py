import nn


class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.
        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.
        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.
        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        dot_product = nn.as_scalar(self.run(x))
        if dot_product >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        full_accuracy = False
        while not full_accuracy:  # Loop until 100% training accuracy has been achieved
            full_accuracy = True
            for x, y in dataset.iterate_once(batch_size):
                examples = self.get_prediction(x)
                if examples != nn.as_scalar(y):
                    self.get_weights().update(x, nn.as_scalar(y))
                    full_accuracy = False


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

        self.hiddenLayerSize = 50
        self.inputSize = 1
        self.outputSize = 1
        self.batchSize = 10
        self.learningRate = 0.01

        self.W1 = nn.Parameter(self.inputSize, self.hiddenLayerSize)
        self.W2 = nn.Parameter(self.hiddenLayerSize, self.outputSize)
        self.b1 = nn.Parameter(1, self.hiddenLayerSize)
        self.b2 = nn.Parameter(1, self.outputSize)
        self.parametersList = [self.W1, self.W2, self.b1, self.b2]

    def run(self, x):
        """
        Runs the model for a batch of examples.
        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"

        xW1 = nn.Linear(x, self.W1)
        xW1b1 = nn.AddBias(xW1, self.b1)
        firstLayer = nn.ReLU(xW1b1)
        xW2 = nn.Linear(firstLayer, self.W2)
        predictedY = nn.AddBias(xW2, self.b2)
        return predictedY

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.
        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        predictedY = self.run(x)
        return nn.SquareLoss(predictedY, y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"

        loss = 1
        while loss >= 0.01:
            for x, y in dataset.iterate_once(self.batchSize):
                loss = self.get_loss(x, y)
                gradWRTList = nn.gradients(loss, self.parametersList)
                for i in range(len(self.parametersList)):
                    self.parametersList[i].update(gradWRTList[i], -self.learningRate)
                loss = nn.as_scalar(loss)


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.
    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.
    The goal is to sort each digit into one of 10 classes (number 0 through 9).
    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.inputSize = 784
        self.outputSize = 10

        self.hiddenLayerSize1 = 200
        self.hiddenLayerSize2 = 100
        self.batchSize = 120
        self.learningRate = 0.1

        self.W1 = nn.Parameter(self.inputSize, self.hiddenLayerSize1)
        self.W2 = nn.Parameter(self.hiddenLayerSize1, self.hiddenLayerSize2)
        self.W3 = nn.Parameter(self.hiddenLayerSize2, self.outputSize)
        self.b1 = nn.Parameter(1, self.hiddenLayerSize1)
        self.b2 = nn.Parameter(1, self.hiddenLayerSize2)
        self.b3 = nn.Parameter(1, self.outputSize)
        self.parametersList = [self.W1, self.W2, self.W3, self.b1, self.b2, self.b3]

    def run(self, x):
        """
        Runs the model for a batch of examples.
        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.
        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        xW1 = nn.Linear(x, self.W1)
        firstLayer = nn.ReLU(nn.AddBias(xW1, self.b1))
        xW2 = nn.Linear(firstLayer, self.W2)
        secondLayer = nn.ReLU(nn.AddBias(xW2, self.b2))
        xW3 = nn.Linear(secondLayer, self.W3)
        predictedY = nn.AddBias(xW3, self.b3)
        return predictedY

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.
        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).
        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        accuracy = 0
        while accuracy <= 0.975:
            for x, y in dataset.iterate_once(self.batchSize):
                loss = self.get_loss(x, y)
                gradientList = nn.gradients(loss, self.parametersList)
                for i in range(len(gradientList)):
                    self.parametersList[i].update(gradientList[i], -self.learningRate)
            accuracy = dataset.get_validation_accuracy()


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
