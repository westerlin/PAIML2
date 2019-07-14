import numpy as np
import math


samples = [[(1,0,1),(1,0,1)],[(1,0,0),(1,0,0)],[(0,0,1),(0,0,1)],[(1,1,0),(1,1,0)],[(0,1,0),(0,1,0)]]
samples_all = [[(1,1,1),(1,1,1)],[(1,0,1),(1,0,1)],[(1,0,0),(1,0,0)],[(0,0,1),(0,0,1)],[(1,1,0),(1,1,0)],[(0,1,0),(0,1,0)]]

samples = [[(1,1),(1)],[(1,0),(1)],[(0,0),(0)]]
samples_all = [[(1,1),(1)],[(1,0),(1)],[(0,0),(0)],[(0,1),(1)]]

samples = [[(1,1),(0)],[(1,0),(1)],[(0,0),(0)],[(0,1),(1)]]
samples_all = [[(1,1),(0)],[(1,0),(1)],[(0,0),(0)],[(0,1),(1)]]

sigmoid_func = lambda x: 1 / (1+math.exp(-x))
sigmoid = np.vectorize(sigmoid_func)

#dsigmoid_func = lambda x: 1 / (1+math.exp(-x)) * (1-1 / (1+math.exp(-x)))
dsigmoid_func = lambda x: sigmoid_func(x) * (1-sigmoid_func(x))
dsigmoid = np.vectorize(dsigmoid_func)

loss_func = lambda x: x*x/2
loss = np.vectorize(loss_func)

round_func = lambda x: int(round(x))
afrund = np.vectorize(round_func)

y0 = np.array((1,1,1))

if isinstance(samples[0][0],int):
	isize = 1
else:
	isize = len(samples[0][0])
size = 6
if isinstance(samples[0][1],int):
	osize = 1
else:
	osize = len(samples[0][1])

w1 = np.random.rand(isize,size)
#w1 = w1/10 + .5
w1 = w1/10 
w2 = np.random.rand(size,osize)
#w2 = w2/10 + .5
w2 = w2/10 

#print(w1,w2)

t1 = np.random.rand(size)
#t1 = t1/10 + .5
t1 = t1/10 
t2 = np.random.rand(osize)
#t2 = t2/10 + .5
t2 = t2/10 
"""
z1 = 0
z2 = 0
y1 = 0
y2 = 0
delta = 0
loss_value1 = 0
"""
#print(t2)

def runforward(sample):
	global z1,y1,z2,y2,delta,loss_value1

	z1 = np.dot(y0,w1) +t1
	y1 = sigmoid(z1)

	z2 = np.dot(y1,w2) +t2
	y2 = sigmoid(z2)

	delta = y2-np.array(sample[1])
	loss_value1 = loss(delta)


# w * x = z -> sigmod

# dL / dy2 *  dy2 / dz2 * dz2/dw2
# ( delta )*(dSigmoid(z2))* y1

# w1 * y0 = z1
# y1 = sigmoid(z1)
# z2 = w2 * y1
# y2 = sigmoid(z2)

# dL/w1 = dL/dy2 * dy2/dz2      * dz2/dy1 * dy1/dz1 * dz1/dw1
#       = delta. * dSigmoid(z2) * w2 * dSigmod(z1) * z1  

steps = 0.5


if 1==1:
	minerror = 999999999
	for a in range(500000):
		err = -99999999
		for sample in samples:
			y0 = np.array(sample[0])

			runforward(sample)

			dsig2 = y2*(1-y2) #dsigmoid(z2)
			dsig1 = y1*(1-y1) #dsigmoid(z1)

			dx = -steps*np.dot(w2,delta * dsig2)

			# first layer
			for c in range(0,isize):
				for r in range(0,size):
					correct2_0 = dsig1[r]*y0[c]*dx[r]
					w1[c,r] += correct2_0

			# second layer
			for r in range(0,size):
				for c in range(0,osize):
					corr = -steps*delta[c] * dsig2[c] * y1[r]
					w2[r,c] += corr


			correct1_1 = -steps*delta * dsig2
			t2 += correct1_1

			for r in range(0,size):
				correct2_1 = -steps*delta * dsig2 * dsig1[r]
				for corr in correct2_1:
					t1[r] += corr

			err = max(np.dot(loss_value1,np.ones(osize)),err)

		if a % 1000==0 and 1==0:
			print(np.dot(loss_value1,np.ones(osize)),y2-y0)
		minerror = min(err,minerror)	
		if minerror < 0.01 : 
			print("Neural net was trained after %d iterations, with max error at %f .. " % (a,minerror))
			break


#my = np.matrix(((1,3,2),(1,2,1),(8,5,1)))
#print(my)
#print(np.dot(my.I,my))

print("\nSamples and reproductions\n")
for sample in samples_all:
	y0 = np.array(sample[0])

	runforward(sample)
	if sample in samples:
		print(" - (trained)    ",end="\t")
	else:
		print(" - (generalized)",end="\t")
	print (np.array(sample[1]),end="\t")
	print (afrund(y2),end="\t")
	print("Error = {:.8f}".format(np.dot(loss_value1,np.ones(osize))))
#print(t2)
#print(t2[0],t2[1],t2[2])
#for a in range(-10000,10000):
#	print(sigmoid_func(a/1000))