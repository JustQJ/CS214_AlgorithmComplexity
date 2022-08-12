
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from matplotlib import colors as clr
from queue import PriorityQueue as PriQ


color_s=[]  #color list
#for key,item in clr.BASE_COLORS.items():
#	color_s.append(item)



#select color
color_s.append('gold')
color_s.append('greenyellow')
color_s.append('lightsalmon')
color_s.append('cyan')
color_s.append('lightskyblue')
color_s.append('plum')
color_s.append('pink')
color_s.append('fuchsia')
color_s.append('aquamarine')
color_s.append('darkseagreen')
color_s.append('green')
color_s.append('thistle')





def Visualized(Task_name, N, Start, Finish, Location, Datacenter_Num, DataSlot):
	fig,ax = plt.subplots(figsize=(20,15))

	#设置x轴和y轴的坐标范围

	xLenth=2*sum(DataSlot)
	yLenth=0
	for k in range(len(Finish)):
		if yLenth<max(Finish[k]):
			yLenth=max(Finish[k])

	ax.set_xlim(0,xLenth) #x坐标轴的范围
	ax.set_ylim(0,yLenth) #y坐标轴的范围

	ax.set_xlabel('DataCenter', fontsize=16, fontfamily = 'sans-serif', fontstyle='italic')
	ax.set_ylabel('Time', fontsize=16, fontfamily = 'sans-serif', fontstyle='italic')

	ax.grid(axis='both')  #网格显示
	ax.set_title('The Result of Task Allocating', fontsize=18)



	#define the name and location of the datacenterLocation
	DataSlot_Name=[]
	for i in range(Datacenter_Num):
		for j in range(DataSlot[i]):
			name='DaCen'+str(i+1)+'_'+str(j+1)
			DataSlot_Name.append(name)
	
	DataSlot_location=[]
	for i in range(len(DataSlot_Name)):
		xLocation=2*(i+1)-0.5
		DataSlot_location.append(xLocation)

	
	#在x轴上写上相应刻度上写标签
	plt.xticks(DataSlot_location, DataSlot_Name, rotation=30)


	#开始画图


	#定义数据中心的结构体

	class TaskStruct:
		def __init__(self, Kth, Ith, Jth, Start, Finish):
			self.Kth = Kth
			self.Ith = Ith
			self.Jth = Jth
			self.Start = Start
			self.Finish = Finish
		def __lt__(self, other):
			return self.Start < other.Start  #比较优先级





	DataCneter_Task=[]   #the datacenter task queue
	for i in range(Datacenter_Num):
		#define the datacenter priorityQueue
		Q=PriQ()  
		DataCneter_Task.append(Q)

	#put the task into the datacenter queue
	for k in range(len(Task_name)):
		for i in range(N[k]):
			DataCneter_Task[Location[k][i]].put(TaskStruct(k,i,Location[k][i],Start[k][i],Finish
				[k][i]))







	

	for j in range(len(DataCneter_Task)):
		slot_time=[]
		for x in range(DataSlot[j]):
			slot_time.append(0)
		while not DataCneter_Task[j].empty():
			Task = DataCneter_Task[j].get()
			for i in range(len(slot_time)):
				if Task.Start >= slot_time[i]:
					slot_time[i]=Task.Finish
					rect = mpathes.Rectangle((2*(sum(DataSlot[0:j])+i)+1,Task.Start ), 1 , Task.Finish-Task.Start , color=color_s[Task.Kth])
					ax.add_patch(rect)
					plt.text(2*(sum(DataSlot[0:j])+i)+1.5,  (Task.Finish+Task.Start)/2 , Task_name[Task.Kth]+str(Task.Ith+1), color='black', ha='center',va='center', fontsize=10); # 位置参数是坐标
					break





	plt.savefig('AllocationResult.png', dpi=800)
	plt.show()
		





if __name__ == '__main__':
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


	Visualized(Task_name, N,  Start, Finish, Location, Datacenter_Num, DataSlot)
