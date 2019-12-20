
import pickle
with open('model/2048_Model10_exp.txt', 'rb') as f:
    list=[]
    while True:
        try:
            data = pickle.load(f)
        except EOFError:
            break
        list.append(data)
    print(data)