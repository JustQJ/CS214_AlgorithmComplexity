

import pulp
import copy
import numpy
#from visualization import Visualized


def liner(K, N, J, M, Cost, Exu,Dslot):
	#print(Cost)
	Xs=[]
	for i in range(K):
		Xs.append([])
		for j in range(N[i]):
			Xs[i].append([])
			for k in range(J):
				Xs[i][j].append(0)


	#the Y
	Y0=[]
	for i in range(K):
		Y0.append([])
		for j in range(N[i]):
			Y0[i].append([])
			for k in range(J):
				Y0[i][j].append(0)


	Y1=[]
	for i in range(K):
		Y1.append([])
		for j in range(N[i]):
			Y1[i].append([])
			for k in range(J):
				Y1[i][j].append(0)


		#the solution of liner program
	# define the problem

	TaskProblem = pulp.LpProblem("Task_Allocation_Problem",pulp.LpMinimize)

	#define the decision varibles

	X=copy.deepcopy(Xs)

	for k in range(K):
		for i in range(N[k]):
			for j in range(J):
				Y0[k][i][j]=pulp.LpVariable('Y0['+str(k)+']'+'['+str(i)+']'+'['+str(j)+']', 0,None, 'Continuous')
				Y1[k][i][j]=pulp.LpVariable('Y1['+str(k)+']'+'['+str(i)+']'+'['+str(j)+']', 0,None, 'Continuous')
				X[k][i][j]=pulp.LpVariable('X['+str(k)+']'+'['+str(i)+']'+'['+str(j)+']', 0,None, 'Continuous')
				



	#define the objective function

	TaskProblem += pulp.lpSum([Y0[k][i][j]+numpy.power(M,Cost[k][i][j]+Exu[k][i][j])*Y1[k][i][j] for k in range(K) for i in range(N[k]) for j in range(J)])

	# define the constraint

	for k in range(K):
		for i in range(N[k]):
			for j in range(J):
				TaskProblem += (X[k][i][j]==Y1[k][i][j] )
	for k in range(K):
		for i in range(N[k]):
	 		for j in range(J):
	 			TaskProblem += (Y0[k][i][j]+Y1[k][i][j]==1)




	for k in range(K):
		for i in range(N[k]):
			TaskProblem += (pulp.lpSum([X[k][i][j] for j in range(J)])==1)



	for j in range(J):
			TaskProblem += (pulp.lpSum([X[k][i][j] for k in range(K) for i in range(N[k])])<=Dslot[j])
	TaskProblem.solve()
	for k in range(K):
		for i in range(N[k]):
			for j in range(J):
				Xs[k][i][j]=X[k][i][j].varValue
	return Xs





#find the max k in all task
def Find_k(X, Cost, Exu_time):
	max_time=0
	result=0
	for k in range(len(X)):
		for i in range(len(X[k])):
			for j in range(len(X[k][i])):
				time = X[k][i][j]*(Cost[k][i][j]+Exu_time[k][i][j])
				if max_time < time:
					max_time = time
					result = k
	return result

def AllocStage(K,N,J,Cost,Exu,Dslot):
	#copy all input 
	Ktmp=K
	Ntmp=copy.deepcopy(N)
	
	Cost_tmp=copy.deepcopy(Cost)
	Exu_tmp=copy.deepcopy(Exu)
	Dslot_tmp=copy.deepcopy(Dslot)


	#define the result 
	result=[]
	for k in range(K):
		result.append([])
		for i in range(N[k]):
			result[k].append([])
			for j in range(J):
				result[k][i].append(0)

	#record the the original order of the task 
	Task_Order=[]
	for k in range(K):
		Task_Order.append(k)


	while Ktmp>0:
		Mtmp=J*sum(Ntmp)
		Xtmp=liner(Ktmp, Ntmp, J, Mtmp, Cost_tmp, Exu_tmp, Dslot_tmp)
		# find the task k with the longest time
		max_task_k=Find_k(Xtmp, Cost_tmp, Exu_tmp)

		# find the original k
		Orginal_k=0
		for k in range(K):
			if Task_Order[k]==max_task_k:
				Orginal_k=k
				Task_Order[k]=-1         #set -1 to represent this task k is already allocated
				break


		#write to the result
		

		for i in range(N[Orginal_k]):
			for j in range(J):
				result[Orginal_k][i][j]=Xtmp[max_task_k][i][j]
		

		#update all data for the next loop
		#update the Task_Order
		Order=0
		for k in range(K):
			if Task_Order[k]!=-1:
				Task_Order[k]=Order
				Order=Order+1


		#update the Dslot_temp
		for j in range(J):
			for i in range(Ntmp[max_task_k]):
				Dslot_tmp[j]=Dslot_tmp[j]-Xtmp[max_task_k][i][j]

		#update the Cost_temp

		del Cost_tmp[max_task_k]

		#update the  Exu_tmp
		del Exu_tmp[max_task_k]
		
		#update the Ntmp
		del Ntmp[max_task_k]
	

		
		#update the k
		Ktmp=Ktmp-1


	return result








if __name__ == '__main__':
	

	K=2    #the number of task
	N=[2,2]  #the children task of task[i]
	J=3           # the number of datacenter  
	#M=J*sum(N)  #compute the 

	# the cost c[k][i][j]  
	Cost=[]
	for i in range(K):
		Cost.append([])
		for j in range(N[i]):
			Cost[i].append([])
			for k in range(J):
				Cost[i][j].append(2)


	Cost[0][0][0]=2
	Cost[0][0][1]=1.25
	Cost[0][0][2]=0.67
	Cost[0][1][0]=0
	Cost[0][1][1]=1.25
	Cost[0][1][2]=0.67
	Cost[1][0][0]=2
	Cost[1][0][1]=1.25
	Cost[1][0][2]=1.67
	Cost[1][1][0]=3
	Cost[1][1][1]=1.89
	Cost[1][1][2]=0


	# the execution time of the task 
	Exu=[]
	for i in range(K):
		Exu.append([])
		for j in range(N[i]):
			Exu[i].append([])
			for k in range(J):
				Exu[i][j].append(1)


	# the number of slots in datacenter i D[i]
	Dslot=[]
	for i in range(J):
		Dslot.append(2)
	Dslot[2]=1

	print(AllocStage(K, N, J,  Cost, Exu,Dslot))

	'''
	Task_name=['A','B','C']


	N=[2,3,2]

	Datacenter_Num=3

	DataSlot=[2,2,2]






	Start=[]
	Finish=[]
	Location=[]

	for k in range(len(Task_name)):
		Start.append([])
		Finish.append([])
		Location.append([])
		for i in range(N[k]):
			Start[k].append(i)
			Finish[k].append(i+1)
			Location[k].append(k)


	Visualized(Task_name, N, Start, Finish, Location,Datacenter_Num, DataSlot)
'''





