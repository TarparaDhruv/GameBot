import numpy as np
import time

def nonlin(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)

	return 1/(1+np.exp(-x))
    
xxx=list()
yyy=list()

filepath = 'data1.txt'  
f = open(filepath,'r')

while True:
	line = f.readline()
	if(line==""):
		break
	yyy.append(list(map(int, line.strip().split(" "))))
	xx = list()
	i = 0
	while i<12:
		line = f.readline()
		tempx = line.strip().split(" ")
		resultsx = list(map(int, tempx))
		xx = list(xx + resultsx)
		i=i+1
	xxx.append(xx)
f.close()

X = np.asarray(xxx)
y = np.asarray(yyy)
print(X," this is x")
print(y," this is y")
'''X = np.array([[0,0],
            [0,1],
            [1,0],
            [1,1]])
                
y = np.array([[0],
			[1],
			[1],
			[0]])
'''
np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2*np.random.random((192,10)) - 1
syn1 = 2*np.random.random((10,1)) - 1
#print(syn0)
#print(syn1)
for j in range(6000):
	# Feed forward through layers 0, 1, and 2
	l0 = X
	l1 = nonlin(np.dot(l0,syn0))
	l2 = nonlin(np.dot(l1,syn1))

	# how much did we miss the target value?
	l2_error = y - l2

	if (j% 10000) == 0:
		print ("Error:" + str(np.mean(np.abs(l2_error))))
	# in what direction is the target value?
	# were we really sure? if so, don't change too much.
	l2_delta = l2_error*nonlin(l2,deriv=True)
	# how much did each l1 value contribute to the l2 error (according to the weights)?
	l1_error = l2_delta.dot(syn1.T)

	# in what direction is the target l1?
	# were we really sure? if so, don't change too much.
	l1_delta = l1_error * nonlin(l1,deriv=True)

	syn1 += l1.T.dot(l2_delta)
	syn0 += l0.T.dot(l1_delta)
	#print(l1,"l1 \n")
	#print(l1_error,"l1error \n")
	print(j,"\n")
	
print ("EOP")
np.savetxt("y.txt",y,fmt='%f' ,header= "y")
np.savetxt("l2.txt",l2,fmt='%f' ,header= "l2")

#np.savetxt(str(time.time())+".txt",syn0,fmt='%f' ,header= "syn0")
#np.savetxt(str(time.time())+".txt",syn1,fmt='%f' ,header= "syn1")

np.savetxt("syn0.txt",syn0,fmt='%f')
np.savetxt("syn1.txt",syn1,fmt='%f')
