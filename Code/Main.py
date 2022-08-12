import copy
import pulp
import numpy
from AllocGraph import AllocationGraph



def main(judge):
	
	if judge:
		Job_name=['A','B','C','D','E','F','G','H','J','S'] #the name of the Job

		Job_Number=10 #the number 

		DC_Number=11 #the number of the datacenter

		MaxChildTask_Num=6 #the max number of children task of some job

		MaxDataDC_Num=6  #the max data srouce number  coming from the datacenter

		MaxDataJB_Num=6  #the max data srouce number coming from the other task 

		MaxStage=7 #stage个数

		DataPath='TestData'

		AllocationGraph( DataPath, Job_name, Job_Number, DC_Number, MaxChildTask_Num, MaxDataDC_Num, MaxDataJB_Num, MaxStage)
	else:
		Job_name=['A','B','C','D','E','F'] #the name of the Job

		Job_Number=6 #the number 

		DC_Number=13 #the number of the datacenter

		MaxChildTask_Num=10 #the max number of children task of some job

		MaxDataDC_Num=10  #the max data srouce number  coming from the datacenter

		MaxDataJB_Num=10  #the max data srouce number coming from the other task 

		MaxStage=10 #stage个数

		DataPath='OriginalData'

		AllocationGraph( DataPath, Job_name, Job_Number, DC_Number, MaxChildTask_Num, MaxDataDC_Num, MaxDataJB_Num, MaxStage)






if __name__ == '__main__':

	# if true ,run the new data test
	# if false ,run the oruginal data test
	
	main(True)

	main(False)

