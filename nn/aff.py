import tensorflow as tf
import numpy as np

# generate data
x = np.random.rand(100).astype(np.float32)
y = x * 0.1 + 0.3

# create tesorflow structure start
Weights = tf.Variable(tf.random.uniform([1], -1.0, 1.0))
biase = tf.Variable(tf.zeros([1]))

y_real = Weights * x + biase
loss = tf.reduce_mean(tf.square(y - y_real))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

# initial tensorflow structure
init = tf.initialize_all_variables()

session = tf.Session()
session.run(init)

for step in range(2000):
    session.run(train)
    if step % 20 == 0:
        print(step, session.run(Weights), session.run(biase))
