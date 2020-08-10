import tensorflow as tf
import numpy as np


def layer(inputs, size_i, size_o, activation_func=None):
    Weights = tf.Variable(tf.random.normal([size_i, size_o]))
    biases = tf.Variable(tf.zeros([1, size_o]) + 0.1)

    Wx_plus_b = tf.matmul(inputs, Weights) + biases
    if activation_func == None:
        outputs = Wx_plus_b
    else:
        outputs = activation_func(Wx_plus_b)

    return outputs


xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])

x_data = np.linspace(-1, 1, 1000)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

layer_1 = layer(xs, 1, 10, activation_func=tf.nn.relu)
layer_2 = layer(layer_1, 10, 1, activation_func=None)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - layer_2), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(loss)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)

    for i in range(1000):
        sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 50 == 0:
            print(sess.run(loss, feed_dict={xs: x_data, ys: y_data}))
