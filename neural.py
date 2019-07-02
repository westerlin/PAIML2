import numpy as np
import math


samples2 = [(1,1,1),(1,0,1),(1,0,0),(0,1,1),(0,0,1),(1,1,0),(0,1,0)]
samples = [(1,1,1),(1,0,1),(1,0,0),(0,1,1),(0,0,1),(1,1,0),(0,1,0)]

sigmoid_func = lambda x: 1 / (1+math.exp(-x))
sigmoid = np.vectorize(sigmoid_func)

#dsigmoid_func = lambda x: 1 / (1+math.exp(-x)) * (1-1 / (1+math.exp(-x)))
dsigmoid_func = lambda x: sigmoid_func(x) * (1-sigmoid_func(x))
dsigmoid = np.vectorize(dsigmoid_func)

loss_func = lambda x: x*x/2
loss = np.vectorize(loss_func)

y0 = np.array((1,1,1))

size = 10

w1 = np.random.rand(3,size)
#w1 = w1/10 + .5
w1 = w1/10 
w2 = np.random.rand(size,3)
#w2 = w2/10 + .5
w2 = w2/10 

#print(w1,w2)

t1 = np.random.rand(size)
#t1 = t1/10 + .5
t1 = t1/10 
t2 = np.random.rand(3)
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

def runforward():
	global z1,y1,z2,y2,delta,loss_value1

	z1 = np.dot(y0,w1) +t1
	y1 = sigmoid(z1)

	z2 = np.dot(y1,w2) +t2
	y2 = sigmoid(z2)

	delta = y2-y0
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

steps = 1.5


if 1==1:
	minerror = 999999999
	for a in range(500000):
		err = -99999999
		for sample in samples:
			y0 = np.array(sample)

			runforward()

			dsig2 = y2*(1-y2) #dsigmoid(z2)
			dsig1 = y1*(1-y1) #dsigmoid(z1)
			dx = -steps*np.dot(w2,delta * dsig2)

			if 1==1:
				for c in range(0,3):
					for r in range(0,size):
						correct2_0 = dsig1[r]*y0[c]*dx[r]
						w1[c,r] += correct2_0

						#dz1_dw1 = -dsigmoid(z1)[r] * y0[c]
						#correct2_0 = -steps*delta * dsigmoid(z2) * dz1_dw1*w2[r,c]

			if 1==1:
				for r in range(0,size):
					for c in range(0,3):
						corr = -steps*delta[c] * dsig2[c] * y1[r]
						w2[r,c] += corr


			#correct1_0 = -steps*delta * dsigmoid(z2) * np.dot(y1,np.ones((size,3))) 
			#correct1_0 = -steps*delta * np.outer(y1,dsigmoid(z2))

			#w2 = w2 + correct1_0
			correct1_1 = -steps*delta * dsig2
			t2 += correct1_1

			#dz1_dw1 = dsigmoid(z1) * np.dot(y0,np.ones((3,size))) 
			#print(dz1_dw1.shape)
			#print(w2.shape)
			#print(np.dot(dz1_dw1,w2).shape)
			#w1 = w1 + correct2_0
			if 1==1:
				for r in range(0,size):
					correct2_1 = -steps*delta * dsig2 * dsig1[r]
					for corr in correct2_1:
						t1[r] += corr
			err = max(np.dot(loss_value1,np.array((1,1,1))),err)

		if a % 1000==0 and 1==1:
			print(np.dot(loss_value1,np.array((1,1,1))),y2-y0)
		minerror = min(err,minerror)	
		if minerror < 0.01 : break


#my = np.matrix(((1,3,2),(1,2,1),(8,5,1)))
#print(my)
#print(np.dot(my.I,my))

for sample in samples2:
	y0 = np.array(sample)

	runforward()

	print(y0[0],y0[1],y0[2],end="\t")
	print(int(round(y2[0])),int(round(y2[1])),int(round(y2[2])),end="\t")
	print("{:.8f}".format(np.dot(loss_value1,np.array((1,1,1)))))
#print(t2)
#print(t2[0],t2[1],t2[2])
#for a in range(-10000,10000):
#	print(sigmoid_func(a/1000))