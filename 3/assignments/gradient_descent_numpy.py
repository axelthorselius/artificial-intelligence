"""Gradient descent for linear regression with numpy
"""
import random
import numpy as np
# import datasets
import matplotlib.pyplot as plt

__author__ = 'Pierre Nugues'


def sse(X, y, w):
    """
    Sum of squared errors
    :param X:
    :param y:
    :param w:
    :return:
    """
    error = y - X @ w
    return error.T @ error


def normalize(Xy):
    maxima = np.amax(Xy, axis=0)
    D = np.diag(maxima)
    D_inv = np.linalg.inv(D)
    Xy = Xy @ D_inv
    return (Xy, maxima)


def predict(X, w):
    return X @ w


def fit_stoch(X, y, alpha, w,
              epochs=500,
              epsilon=1.0e-5):
    """
    Stochastic gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :param epochs:
    :param epsilon:
    :return:
    """
    global logs, logs_stoch
    logs = []
    logs_stoch = []
    random.seed(0)
    idx = list(range(len(X)))
    for epoch in range(epochs):
        random.shuffle(idx)
        for i in idx:
            loss = y[i] - predict(X[i], w)[0]
            gradient = loss * np.array([X[i]]).T
            w = w + alpha * gradient
            logs_stoch += (w, alpha, sse(X, y, w))
        if np.linalg.norm(gradient) < epsilon:
            break
        logs += (w, alpha, sse(X, y, w))
    print("Epoch", epoch)
    return w


def fit_batch(X, y, alpha, w,
              epochs=500,
              epsilon=1.0e-5):
    """
    Batch gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :param epochs:
    :param epsilon:
    :return:
    """
    global logs
    logs = []
    alpha /= len(X)
    for epoch in range(epochs):
        loss = y - predict(X, w)
        gradient = X.T @ loss
        w = w + alpha * gradient
        logs += (w, alpha, sse(X, y, w))
        if np.linalg.norm(gradient) < epsilon:
            break
    print("Epoch", epoch)
    return w


# if __name__ == '__main__':
#     normalized = True
#     debug = False
#     X, y = datasets.load_tsv(
#         'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
#     # Predictors
#     X = np.array(X)
#     # Response
#     y = np.array([y]).T

#     alpha = 1.0e-10
#     if normalized:
#         X, maxima_X = normalize(X)
#         y, maxima_y = normalize(y)
#         maxima = np.concatenate((maxima_X, maxima_y))
#         alpha = 1.0
#         print("-Normalized-")

#     print("===Batch descent===")
#     w = np.zeros(X.shape[1]).reshape((-1, 1))
#     w = fit_batch(X, y, alpha, w)
#     print("Weights", w)
#     print("SSE", sse(X, y, w))
#     if normalized:
#         maxima = maxima.reshape(-1, 1)
#         print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
#     if debug:
#         print("Logs", logs)
#     plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
#     plt.title("Batch gradient descent: Sum of squared errors")
#     plt.show()
#     plt.plot(list(map(lambda pair: pair[0], logs[0::3])),
#              list(map(lambda pair: pair[1], logs[0::3])),
#              marker='o')
#     for i in range(len(logs[0::3])):
#         plt.annotate(i, xy=logs[0::3][i])
#     plt.title("Batch gradient descent: Weights")
#     plt.show()

#     print("===Stochastic descent===")
#     w = np.zeros(X.shape[1]).reshape((-1, 1))
#     w = fit_stoch(X, y, alpha, w)
#     print("Weights", w)
#     print("SSE", sse(X, y, w))
#     if normalized:
#         maxima = maxima.reshape(-1, 1)
#         print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
#     if debug:
#         print("Logs", logs)
#         print("Logs stoch.", logs_stoch)
#     plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
#     plt.title("Stochastic gradient descent: Sum of squared errors")
#     plt.show()
#     plt.plot(list(map(lambda pair: pair[0], logs[0::3])),
#              list(map(lambda pair: pair[1], logs[0::3])),
#              marker='o')
#     for i in range(len(logs[0::3])):
#         plt.annotate(i, xy=logs[0::3][i])
#     plt.title("Stochastic gradient descent: Weights")
#     plt.show()
#     plt.scatter(range(len(logs_stoch[2::3])),
#                 logs_stoch[2::3],
#                 c='b', marker='x')
#     plt.title("Stochastic gradient descent: Sum of squared errors (individual updates)")
#     plt.show()
#     plt.plot(list(map(lambda pair: pair[0], logs_stoch[0::3])),
#              list(map(lambda pair: pair[1], logs_stoch[0::3])),
#              marker='o')
#     plt.title("Stochastic gradient descent: Weights (individual updates)")
#     plt.show()
