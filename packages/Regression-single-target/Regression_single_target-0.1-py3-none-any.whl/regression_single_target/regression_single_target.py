import numpy as np
import matplotlib.pyplot as plt
import os
class Regression_single_target:
    def __init__(self, lr=0.01, num_iters=1000):
        """
        Constructor for the Regression_single_target class.

        Parameters:
        lr (float): learning rate for gradient descent (default=0.01).
        num_iters (int): number of iterations for gradient descent (default=1000).
        """
        self.lr = lr
        self.num_iters = num_iters
        self.weights = None
        self.bias = None
        self.loss_history = []

    def fit(self, X, y):
        """
        Fit linear regression model to the data.

        Parameters:
        X (numpy.ndarray): input data of shape (n_samples, n_features).
        y (numpy.ndarray): target labels of shape (n_samples, 1).

        Returns:
        None
        """
        n_samples, n_features = X.shape

        # Initialize the weights and bias
        self.weights = np.zeros((n_features, 1))
        self.bias = 0

        # Gradient descent
        for i in range(self.num_iters):
            y_predicted = np.dot(X, self.weights) + self.bias

            dw = (1/n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1/n_samples) * np.sum(y_predicted - y)

            self.weights -= self.lr * dw.T  # Transpose dw
            self.bias -= self.lr * db

            # Record the loss at each iteration
            self.loss_history.append(self.mean_squared_error(y, y_predicted))

    def predict(self, X):
        """
        Predict target labels for new data.

        Parameters:
        X (numpy.ndarray): new input data of shape (n_samples, n_features).

        Returns:
        numpy.ndarray: predicted target labels of shape (n_samples, 1).
        """
        y_predicted = np.dot(X, self.weights) + self.bias
        return y_predicted

    def mean_squared_error(self, y_true, y_pred):
        """
        Compute the mean squared error between true and predicted target labels.

        Parameters:
        y_true (numpy.ndarray): true target labels of shape (n_samples, 1).
        y_pred (numpy.ndarray): predicted target labels of shape (n_samples, 1).

        Returns:
        float: mean squared error between true and predicted target labels.
        """
        return np.mean((y_true - y_pred) ** 2)

    def plot_loss_history(self):
        """
        Plot the loss history over the course of training.

        Parameters:
        None

        Returns:
        None
        """
        plt.plot(range(self.num_iters), self.loss_history)
        plt.title('Loss vs. Iterations')
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.savefig('loss_history.png', dpi=300)
        plt.clf()

    def plot_data(self):
        """
        Plot the input data and target labels.

        Parameters:
        None

        Returns:
        None
        """
        plt.scatter(X,y)
        plt.title('Data vs labels')
        plt.xlabel('Data [X]')
        plt.ylabel('Labels [y]')
        plt.savefig('dataplot.png', dpi=300)
        plt.clf()

    def plot_regression(self, X, y, X_new, y_pred):
        """
        Plot the linear regression line on top of the input data and target labels.

        Parameters:
        X (numpy.ndarray): input data of shape (n_samples, n_features).
        y (numpy.ndarray): target labels of shape (n_samples, 1).
        X_new (numpy.ndarray): new input data of shape (n_samples_new, n_features).
        y_pred (numpy.ndarray): predicted target labels of shape (n_samples_new, 1).

        Returns:
        None
        """
        plt.scatter(X, y)
        plt.plot(X_new, y_pred, 'r')
        plt.title('Linear Regression')
        plt.xlabel('X')
        plt.ylabel('y')
        plt.savefig('regression.png', dpi=300)
        plt.clf()
    def to_latex(self, filename):
        """
        Generates a LaTeX document with the training parameters, plots of the data and label,
        loss vs iterations, and the linear regression line.

        Parameters:
        filename (str): The name of the LaTeX file to be generated.
        """
        with open(filename, 'w') as f:
            f.write('\\documentclass{article}\n')
            f.write('\\usepackage{graphicx}\n')
            f.write('\\begin{document}\n\n')
            
            f.write('Training parameters:\n')
            f.write('\\begin{itemize}\n')
            f.write('\\item Learning rate: {}\n'.format(self.lr))
            f.write('\\item Number of iterations: {}\n'.format(self.num_iters))
            f.write('\\end{itemize}\n\n')
            f.write("\\")
            f.write('Data vs label:\n')
            f.write('\\begin{figure}[h]\n')
            f.write('\\centering\n')
            f.write('\\includegraphics[scale = 0.5]{dataplot.png}\n')
            f.write('\\end{figure}\n\n')
            f.write("\\")
            f.write("\newpage")
            f.write('Loss vs. iterations:\n')
            f.write('\\begin{figure}[h]\n')
            f.write('\\centering\n')
            f.write('\\includegraphics[scale = 0.5]{loss_history.png}\n')
            f.write('\\end{figure}\n\n')
            f.write("\\")
            f.write('Linear regression:\n')
            f.write('\\begin{figure}[h]\n')
            f.write('\\centering\n')
            f.write('\\includegraphics[scale = 0.5]{regression.png}\n')
            f.write('\\end{figure}\n\n')
            
            f.write('\\end{document}\n')
        
        # Compile the LaTeX file to PDF
        os.system('pdflatex {}'.format(filename))

