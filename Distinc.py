import os
f1=open('E:'+os.sep+'paindatabase'+os.sep+'creawl_drugbank'+os.sep+'drugbank_link.txt','r')
f2=open('E:'+os.sep+'paindatabase'+os.sep+'creawl_drugbank'+os.sep+'drugbank_id.txt','r')
list1=[]
list2=[]

for line in f1.readlines():
    #print(line.strip())
    list1.append(line.strip())
print(len(list1))
list1=list(set(list1))
print(len(list1))

for line in f2.readlines():

    list2.append(line.strip())
print(len(list2))
list2=list(set(list2))
print(len(list2))
f2.close()
f1.close()

f1=open('E:'+os.sep+'paindatabase'+os.sep+'creawl_drugbank'+os.sep+'drugbank_link_distinc.txt','w+')
f2=open('E:'+os.sep+'paindatabase'+os.sep+'creawl_drugbank'+os.sep+'drugbank_id_distinc.txt','w+')
for line in list1:
    f1.writelines(line+'\n')
for line in list2:
    f2.writelines(line+'\n')
f1.close()
f2.close()
