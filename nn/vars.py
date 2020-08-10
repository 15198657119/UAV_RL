import tensorflow as tf

state = tf.Variable(0, name='counter')
one = tf.constant(1, name='constant')

vals = tf.add(state, one)
update = tf.compat.v1.assign(state, vals)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for _ in range(3):
        sess.run(update)
        print(sess.run(state))
