import copy
import pulp
import numpy

from visualization import Visualized
from AllocStage import AllocStage

def AllocationGraph(DataPath, Task_Name, K, N, maxtn, Locnmax, Loctnmax, maxstage):
	

	tn=[]


	class tt:
		yu=0
		ET=0
		    #ff用来映射位置
		sstime=0         #sstime 开始运数据  stime开始执行  ftime结束执行
		stime=0
		ftime=0
		center=0

	class JJob:
		pass

	    


	Job=[]
	for i in range(K):
		Job.append(JJob())

	for i in range(K):
		Job[i].t=[]
		for j in range(maxtn):

			Job[i].t.append(tt())


	for i in range(K):
		for j in range(maxtn):
			Job[i].t[j].need=[]
			for jj in range(Locnmax):                         #!!!!!!!!!!!!!!!!!!!!!!!!
				Job[i].t[j].need.append(0)

	for i in range(K):
		for j in range(maxtn):
			Job[i].t[j].tneed=[]
			for jj in range(Loctnmax):                         #!!!!!!!!!!!!!!!!!!!!!!!!
				Job[i].t[j].tneed.append(0)

	for i in range(K):
		for j in range(maxtn):
			Job[i].t[j].ff=[]
			for jj in range(2):                         #!!!!!!!!!!!!!!!!!!!!!!!!
				Job[i].t[j].ff.append([])





	G=[[0 for i in range(N)] for i in range(N)]
	T=[[0 for i in range(N)] for i in range(N)]
	Pr=[[0 for i in range(maxtn)] for i in range(K)]
	#print(Pr)
	Loc=[[[0 for i in range(Locnmax)] for i in range(K)] for i in range(N)]
	Loct=[[[0 for i in range(Loctnmax)] for i in range(K)] for i in range(N)]


	class DDc:
		nummax=0
		numc=0
	Dc=[]
	for i in range(N):
		Dc.append(DDc())


	class sstage:
		stime=0
		ftime=0
	stage=[]


	#以上为定义声明部分



	#读入Dc.txt  数据中心计算槽数目
	with open(DataPath+'\\'+'Dc.txt',"r") as fDc:
		dataDc=fDc.readlines()
	for i in range(0,len(dataDc)):
		dataDc[i]=dataDc[i].rstrip('\n')
	for i in range(N):
		Dc[i].numc=int(dataDc[i])


	#读入G
	with open(DataPath+'\\'+'G.txt',"r") as fG:
		dataG=fG.readlines()
	for i in range(0,len(dataG)):
		dataG[i]=dataG[i].rstrip('\n')
	for i in range(N):
		for j in range(N):
			G[i][j]=int(dataG[i*N+j])



	#读入子任务数目
	with open(DataPath+'\\'+'tn.txt',"r") as ftn:
		datatn=ftn.readlines()
	for i in range(0,len(datatn)):
		datatn[i]=datatn[i].rstrip('\n')
	for i in range(K):
		tn.append(int(datatn[i]))


	#读入数据堆位置
	with open(DataPath+'\\'+'loc.txt',"r") as floc:
		dataloc=floc.readlines()
	for i in range(0,len(dataloc)):
		dataloc[i]=dataloc[i].rstrip('\n')
	for i in range(int(len(dataloc)/3)):
		lla=int(dataloc[i*3+0])-1
		llb=int(dataloc[i*3+1])-1
		llc=int(dataloc[i*3+2])-1
		
		Loc[llc][lla][llb]=1


	#读入执行时间


	with open(DataPath+'\\'+'ET.txt',"r") as fET:
		dataET=fET.readlines()
	for i in range(0,len(dataET)):
		dataET[i]=dataET[i].rstrip('\n')

	for i in range(K):
		for j in range(tn[i]):
			hao=0
			for jj in range(i):
				hao+=tn[jj]

			Job[i].t[j].ET=float(dataET[hao+j])
	


	#读入优先级
	with open(DataPath+'\\'+'pre.txt',"r") as fpre:
		datapre=fpre.readlines()
	for i in range(0,len(datapre)):
		datapre[i]=datapre[i].rstrip('\n')
	for i in range(int(len(datapre)/4)):
		la=int(datapre[i*4+0])-1
		lb=int(datapre[i*4+1])-1
		lc=int(datapre[i*4+2])-1
		ld=int(datapre[i*4+3])-1
		Pr[lc][ld]=Pr[la][lb]+1


	#读入所需数据量
	with open(DataPath+'\\'+'amount.txt',"r") as famount:
		dataamount=famount.readlines()
	for i in range(0,len(dataamount)):
		dataamount[i]=dataamount[i].rstrip('\n')
	ld1=0
	ld2=0
	up=0
	ffll=0
	for i in range(len(dataamount)):
		pan=int(dataamount[i])
		if(pan==-1):
			ld1+=1
			ld2=0
			up=0
			ffll=0
			continue
		if(pan==-2):
			ld2+=1
			up=0
			ffll=0
			continue
		if(pan==-3):
			up=0
			ffll=1
			continue

		if(ffll==0):
			Job[ld1].t[ld2].need[up]=int(dataamount[i])
		else:
			Job[ld1].t[ld2].tneed[up]=int(dataamount[i])

		up+=1;






	#以上为读入以及常量整理部分



	'''for i in range(N):
		for j in range(N):
			T[i][j]=1/G[i][j]'''



	for i in range(N):
		for j in range(N):
			if(G[i][j]>0):
				T[i][j]=1/G[i][j]
			else:
				T[i][j]=1000	

	for i in range(N):
		for j in range(N):
			for jj in range(N):
				if(T[j][i]+T[i][jj]<T[j][jj]):
					T[j][jj]=T[j][i]+T[i][jj]




	for i in range(maxstage):
		stage.append(sstage())



	for uu in range(maxstage):        #大循环
		if(uu>0):
			stage[uu].stime=stage[uu-1].ftime

		aa=[]
		KK=[]
		c=[[[0 for i in range(N)] for i in range(maxtn)] for i in range(K)]
		

		ff1=0
		ff2=0
		for yt in range(K):
			flag11=0
			for oo in range(tn[yt]):
				if(Pr[yt][oo]==uu):
					flag11=1
					Job[yt].t[oo].ff[0]=ff1
					Job[yt].t[oo].ff[1]=ff2
					ff2+=1
			if(flag11==1):
				ff1+=1
			ff2=0
		NN=[0 for tr in range(ff1)]   #NN为传递的N，同时ff1也为传递的K

		for yt in range(K):
			for oo in range(tn[yt]):
				if(Pr[yt][oo]==uu):    #确定子任务在当前stage中
					NN[Job[yt].t[oo].ff[0]]+=1

					
	                                                    #yt oo 确定子任务号
					for re in range(N):                 #re是运往的数据中心号
						max1=0                          #max1是该任务运往re的最大数据堆运送时间
						for pp in range(len(Job[yt].t[oo].need)):   #pp是所需数据堆号
							if(Job[yt].t[oo].need[pp]>0):
								min1=100000000                    #min1是某数据运往re的最小时间
								for ju in range(N): #ju号数据中心
									if(Loc[ju][yt][pp]>0):
										min1=min(min1,T[ju][re]*Job[yt].t[oo].need[pp])
								max1=max(max1,min1)
						max2=0
						for pp in range(len(Job[yt].t[oo].tneed)):
							if(Job[yt].t[oo].tneed[pp]>0):
								min1=100000000
								for ju in range(N):
									if(Loct[ju][yt][pp]>0):
										min1=min(min1,T[ju][re]*Job[yt].t[oo].tneed[pp])
								max2=max(max2,min1)

						maxz=max(max1,max2)

						c[yt][oo][re]=maxz





		Cost=[]
		for i in range(ff1):
			Cost.append([])
			for j in range(NN[i]):
				Cost[i].append([])
				for jj in range(N):
					Cost[i][j].append([])



		

		for yt in range(K):
			for oo in range(tn[yt]):
				if(Pr[yt][oo]==uu):
					for khh in range(N):
						Cost[Job[yt].t[oo].ff[0]][Job[yt].t[oo].ff[1]][khh]=c[yt][oo][khh]



		off=[]
		for i in range(ff1):
			off.append([])
			for j in range(NN[i]):
				off[i].append([])
				for jj in range(2):
					off[i][j].append([])

		for yt in range(K):
			for oo in range(tn[yt]):
				if(Pr[yt][oo]==uu):
					off[Job[yt].t[oo].ff[0]][Job[yt].t[oo].ff[1]][0]=yt
					off[Job[yt].t[oo].ff[0]][Job[yt].t[oo].ff[1]][1]=oo	



		Dslot=[]
		for i in range(N):
			Dslot.append(Dc[i].numc)



		#NN已有
		Exu=[]
		for i in range(ff1):
			Exu.append([])
			for j in range(NN[i]):
				Exu[i].append([])
				for jj in range(N):
					Exu[i][j].append([])

		for yt in range(K):
			for oo in range(tn[yt]):
				if(Pr[yt][oo]==uu):
					for khh in range(N):
						Exu[Job[yt].t[oo].ff[0]][Job[yt].t[oo].ff[1]][khh]=copy.deepcopy(Job[yt].t[oo].ET)





		#NN为传递的N，ff1为传递的K，N为传递的J


	    #AllocStage(K, N, J,  Cost, Exu,Dslot)

	
		xxx=AllocStage(ff1,NN,N,Cost,Exu,Dslot)            #xxx映射到二维xx
		xx=[]
		for i in range(ff1):
			xx.append([])
			for j in range(NN[i]):
				xx[i].append([])

		for i in range(ff1):
			for j in range(NN[i]):
				for jj in range(N):
					if(xxx[i][j][jj]==1):
						xx[i][j]=jj




		maxstageftime=0
		for i in range(ff1):
			for j in range(NN[i]):
				zh=xx[i][j]
				ofi=off[i][j][0]
				ofj=off[i][j][1]             #ofi和ofj是映射回去的位置

				Job[ofi].t[ofj].center=zh
				Job[ofi].t[ofj].sstime=stage[uu].stime
				Job[ofi].t[ofj].stime=Job[ofi].t[ofj].sstime+c[ofi][ofj][zh]
				Job[ofi].t[ofj].ftime=Job[ofi].t[ofj].stime+Job[ofi].t[ofj].ET
				maxstageftime=max(maxstageftime,Job[ofi].t[ofj].ftime)


			#	Dc[zh].numc-=1               #计算槽数目减少  (不用)

				#下面调查该子任务需要的数据位置并标成已有
				for qw in range(len(Job[ofi].t[ofj].need)):
					if(Job[ofi].t[ofj].need[qw]>0):
						Loc[zh][ofi][qw]=1

				#改tneed
				Loct[zh][ofi][ofj]=1





		stage[uu].ftime=maxstageftime




	#打印结果

	for i in range(K):
		for j in range(tn[i]):
			print(Task_Name[i]+str(j+1),"Start Time: %0.2f" % Job[i].t[j].sstime,"Finish Time: %0.2f" % Job[i].t[j].ftime,"Location:", "DataCneter"+str(Job[i].t[j].center+1))


	SStart=[[0 for i in range(tn[i])] for j in range(K)]
	FFinish=[[0 for i in range(tn[i])] for j in range(K)]
	LLoc=[[0 for i in range(tn[i])] for j in range(K)]

	for i in range(K):
		for j in range(tn[i]):
			SStart[i][j]=Job[i].t[j].sstime
			FFinish[i][j]=Job[i].t[j].ftime
			LLoc[i][j]=Job[i].t[j].center
	#N
	#所有任务的子任务的最大完成时间

	max_finish_time=[]

	for k in range(len(FFinish)):
		max_finish_time.append(max(FFinish[k]))

	#print(max_finish_time)
	#the allocation result 


	print("Average Competion Time: ", sum(max_finish_time)/K)
	
	

	#可视化
	Visualized(Task_Name, tn,  SStart, FFinish, LLoc, N, Dslot)



if __name__ == '__main__':


	Task_name=['A','B','C','D','E','F']
	K=6
	N=13
	maxtn=9 #最大子任务数目
	Locnmax=10
	Loctnmax=10
	maxstage=10 #stage个数 读入后需更改
	DataPath='data'

	AllocationGraph( DataPath, Task_name, K, N, maxtn, Locnmax, Loctnmax, maxstage)

	