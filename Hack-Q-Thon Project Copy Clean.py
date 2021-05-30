#!/usr/bin/env python
# coding: utf-8

# In[4]:


from qiskit import *

get_ipython().run_line_magic('matplotlib', 'inline')
from qiskit.tools.visualization import plot_histogram as hist
from qiskit.tools.monitor import job_monitor
import operator

IBMQ.load_account()
provider=IBMQ.get_provider('ibm-q')




def Xrot(circuit, length, amount):

    i=0
    while i<length:
        circuit.rx(-2*amount,[i])
        i+=1




def Zrot(cr, amount, a, b):

    i=0
    while i<6:
        cr.rz(2*amount*a[i],[i])
        i+=1
    i=0
    while i<6:
        j=i+1
        while j<6:
            cr.cx([i],[6])
            cr.cx([j],[6])
            cr.rz(2*amount*b[6*i+j],[6])
            cr.cx([i],[6])
            cr.cx([j],[6])
            j+=1
        i+=1
    cr.barrier()
    cr.reset([6])




def Optimize(penalty,a,b,p,segmentCosts):

    J=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    h=[0,0,0,0,0,0]
     
    i=0
    while i<6:
        h[i]=4*penalty-0.5*segmentCosts[i]
        i+=1
    i=0
    while i<36:
        J[i]=2*penalty
        i+=1
    J[2]=penalty
    J[9]=penalty
    J[29]=penalty
    
    circuit=QuantumCircuit(7,6)
    circuit.h([0,1,2,3,4,5])

    i=0
    
    while i<p:
        Zrot(circuit, b[i], h, J)
        Xrot(circuit, 6, a[i])
        i+=1
    circuit.measure([0,1,2,3,4,5],[0,1,2,3,4,5])
    circuit.reset([0,1,2,3,4,5])
    return circuit




circuita=Optimize(20,[0.619,0.743,0.060,-1.569,-0.045],[3.182,-1.139,0.121,0.538,-0.417],5,[5,9,9,6,8,2])

simulator = Aer.get_backend('qasm_simulator')
result = execute(circuita,backend = simulator, shots=4000).result()

total=result.get_counts(circuita)
datatype=type(total)

totaldict=dict(total)
type(totaldict)
print(totaldict)
maximum=0
bestkey=""

for key in totaldict:

    if totaldict[key]>maximum:
        bestkey=key
        maximum=totaldict[key]

print(bestkey)
print(maximum)

