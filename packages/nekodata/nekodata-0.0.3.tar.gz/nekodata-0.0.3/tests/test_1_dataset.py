from nekodata.dataset import Dataset
import numpy as np
from torchvision import datasets, transforms

def test_init():
    mnist_train = Dataset('MNIST', train=True)
    mnist_test = Dataset('MNIST', train=False)

    mnist_train_true = datasets.MNIST('../data', train=True, download=True)
    mnist_test_true = datasets.MNIST('../data', train=False, download=True)

    assert len(mnist_train) == len(mnist_train_true)
    assert np.array_equal(np.asarray(mnist_train[0][0]), np.asarray(mnist_train_true[0][0]))
    assert mnist_train[0][1] == mnist_train_true[0][1]

    assert len(mnist_test) == len(mnist_test_true)
    assert np.array_equal(np.asarray(mnist_test[0][0]), np.asarray(mnist_test_true[0][0]))
    assert mnist_test[0][1] == mnist_test_true[0][1]