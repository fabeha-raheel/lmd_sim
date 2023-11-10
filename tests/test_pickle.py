import pickle

obj = [(72, (-35.3632888, 149.1652929)), (125, (-35.3632687, 149.1652037)), (166, (-35.363247, 149.1652589))]
f = open('store.pckl', 'wb')
pickle.dump(obj, f)
f.close()

f = open('/home/ugv/lmd_ws/src/lmd_sim/logs/lmd_data.pickle', 'rb')
obj1 = pickle.load(f)
print(obj1)
f.close()