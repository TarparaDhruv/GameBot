import numpy as np
	
#x = np.empty([2,192],dtype=int)
#y = np.empty([1,0],dtype=int)
xxx=list()
yyy=list()
index=0	
filepath = 'data.txt'  
with open(filepath) as fp:  
	line = fp.readline()
	#tempy = line.strip().split(" ") 
	#resultsy = list(map(int, tempy))
	#yyy.append(resultsy)
	cnt = 1
	while line:
		temp = line.strip().split(" ") 
		results = list(map(int, temp))
		yyy.append(results)
		#y[index] = map(int, results)
		count=0
		#print("after y",results)
		line=fp.readline()
		tempx = line.strip().split(" ")
		resultsx = list(map(int, tempx))
		xx=list(resultsx)
		#print(xx)
		#print("new read row",xx)
		while line and count<12:
			tempx = line.strip().split(" ")
			resultsx = list(map(int, tempx))
			#print("new read row",count,resultsx)
			xx = list(xx + resultsx)
			print(xx )
			count=count+1
			line = fp.readline()
			#xx = np.append(xx,xxx)
			#print(resultsx)
			#np.append(l,resultsx)
		#np.insert(x,index,np.asarray(xx))
		#x[index]=10#np.asarray(xx)
		#print(x)
		#print(np.asarray(xx))
		#print( cnt)
		xxx.append(xx)
		#print(xxx)
		#line = fp.readline()
		#cnt += 1
		index=index+1
x = np.asarray(xxx)
#print(np.asarray(xxx))
y = np.asarray(yyy)
#print(xxx)
#print(x[0][0])
#print(x[0][0])
#print(y)
