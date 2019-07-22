import tensorflow as tf
import numpy as np

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv3d(x, W):
    return tf.nn.conv3d(x, W, strides=[1, 1, 1, 1, 1], padding='VALID')

def avg_pool_3d(x):
    return tf.nn.avg_pool3d(x, ksize=[1, 2, 2, 2, 1],
                        strides=[1, 2, 2, 2, 1], padding='VALID')

def init_weights(shape):
    """ Weight initialization """
    weights = tf.random_normal(shape, stddev=0.1)
    return tf.Variable(weights)

def batch_norm(x, n_out, phase_train):
    """
    Batch normalization on convolutional maps.
    Ref.: http://stackoverflow.com/questions/33949786/how-could-i-use-batch-normalization-in-tensorflow
    Args:
        x:           Tensor, 4D BHWD input maps
        n_out:       integer, depth of input maps
        phase_train: boolean tf.Varialbe, true indicates training phase
        scope:       string, variable scope
    Return:
        normed:      batch-normalized maps
    """
    with tf.variable_scope('bn'):
        beta = tf.Variable(tf.constant(0.0, shape=[n_out]),
                                     name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[n_out]),
                                      name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0,1,2], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.5)

        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)

        mean, var = tf.cond(phase_train,
                            mean_var_with_update,
                            lambda: (ema.average(batch_mean), ema.average(batch_var)))
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return normed

def normalize(x, n_out, phase_train):
    """Returns a batch-normalized version of x."""

    beta = tf.Variable(tf.constant(0.0, shape=[n_out]),
                       name='beta', trainable=True)
    gamma = tf.Variable(tf.constant(1.0, shape=[n_out]),
                                      name='gamma', trainable=True)
    mean, variance = tf.nn.moments(x, [0, 1])
    with tf.control_dependencies([mean, variance]):
        return tf.nn.batch_normalization(x, mean, variance, beta, gamma, 1e-3)

def batch_norm2(x, n_out, phase_train):
    """
    Batch normalization on convolutional maps.
    Ref.: http://stackoverflow.com/questions/33949786/how-could-i-use-batch-normalization-in-tensorflow
    Args:
        x:           Tensor, 4D BHWD input maps
        n_out:       integer, depth of input maps
        phase_train: boolean tf.Varialbe, true indicates training phase
        scope:       string, variable scope
    Return:
        normed:      batch-normalized maps
    """

    # inputs_shape = x.get_shape()
    # dtype = x.dtype.base_dtype
    # axis = list(range(len(inputs_shape) - 1))
    # params_shape = inputs_shape[-1:]

    with tf.variable_scope('bn'):
        beta = tf.Variable(tf.constant(0.0, shape=[n_out]),
                                     name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[n_out]),
                                      name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.5)

        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)

        mean, var = tf.cond(phase_train,
                            mean_var_with_update,
                            lambda: (ema.average(batch_mean), ema.average(batch_var)))
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return normed


def convolutional_layer_with_pooling_3D(x_3D, kernelSize, numberOfInputChannels, numberOfOutputChannels, phase_train, keep_prob):

    W_conv = weight_variable([kernelSize, kernelSize, kernelSize, numberOfInputChannels, numberOfOutputChannels])
    b_conv = bias_variable([numberOfOutputChannels])

    h_conv = conv3d(x_3D, W_conv) + b_conv

    # h_conv_bn = tf.contrib.layers.batch_norm(h_conv,
    #                                          # data_format='NHWC',
    #                                          center=True, scale=True,
    #                                          is_training=phase_train)
    h_conv_bn = batch_norm(h_conv, numberOfOutputChannels, phase_train)
    h_conv_act = tf.nn.relu(h_conv_bn)
    h_pool = avg_pool_3d(h_conv_act)
    # h_pool_drop = tf.nn.dropout(h_pool, keep_prob)

    return h_pool

def fully_connected_layer(x, input_size, multiLayerPerceptronSize, phase_train, keep_prob):

    W = weight_variable([input_size, multiLayerPerceptronSize])
    b = bias_variable([multiLayerPerceptronSize])

    # h_bn = normalize(x, input_size, phase_train)

    h = tf.matmul(x, W) + b
    # h_bn = tf.contrib.layers.batch_norm(h,  center=True,
    #                                          scale=True,
    #                                          is_training=phase_train,
    #                                          epsilon=1e-3)
    # h_bn = batch_norm2(h, 1, phase_train)
    # h_bn = normalize(h, multiLayerPerceptronSize, phase_train)
    h_1 = tf.nn.relu(h)
    # h_1_drop = tf.nn.dropout(h_1, keep_prob)

    return h_1

def multi_layer_perceptron(x, multiLayerPerceptronSize, classNumber, phase_train, keep_prob):

    W = weight_variable([multiLayerPerceptronSize, classNumber])
    b = bias_variable([classNumber])

    yprime = tf.matmul(x, W) + b

    return yprime