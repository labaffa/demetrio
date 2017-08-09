import pickle

'''
def load_data(file_name):
    try:
        with open(file_name) as f:
            x = pickle.load(f)
    except:
        x = []
    return x



def save_data(data, file_name):
    with open(file_name, "wb") as f:
		for datum in data: pickle.dump(datum, f)
'''

# write list of cls objects to a file named after class 
# (name of the file to be fixed, chiedere a Stefano)
def write(cls_list):
	try:
		with open(cls_list[0].file, 'wb') as f:
			pickle.dump(cls_list,f)
		f.close()

	except:
		cls_list=[]
	
# read list of cls objects from a file named after class	
# (name of the file to be fixed, chiedere a Stefano)
def read(cls_list):
	with open(cls_list[0].file, 'rb') as f:
		data_list=pickle.load(f)
	f.close()
	return data_list



#def read(cls):
#	with open('%s.pickle' %cls, 'rb') as f:
#		cls_list=pickle.load(f)
#	return cls_list
