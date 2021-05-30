#!/usr/bin/env python
# coding: utf-8


from qiskit import *

get_ipython().run_line_magic('matplotlib', 'inline')
from qiskit.tools.visualization import plot_histogram as hist
from qiskit.tools.monitor import job_monitor

IBMQ.load_account()
provider=IBMQ.get_provider('ibm-q')



adderb=QuantumCircuit(14,14)



def FullAdder(circuit,ina,inb,carryin,out,carryout):
    circuit.cx([ina],[out])
    circuit.cx([inb],[out])
    circuit.cx([carryin],[out])
    circuit.ccx([ina],[inb],[carryout])
    circuit.ccx([ina],[carryin],[carryout])
    circuit.ccx([inb],[carryin],[carryout])



def HalfAdder(circuit, ina, inb, out, carryout):
    circuit.cx([ina],[out])
    circuit.cx([inb],[out])
    circuit.ccx([ina],[inb],[carryout])



adderb.h([0,1,2,3,4,5])

FullAdder(adderb,0,1,2,6,7)
adderb.barrier()

FullAdder(adderb,3,4,5,8,9)
adderb.barrier()

HalfAdder(adderb,6,8,10,11)
adderb.barrier()54

FullAdder(adderb,7,9,11,12,13)
adderb.barrier()

adderb.cx([0],[14])
adderb.cx([5],[14])
adderb.cx([1],[15])
adderb.cx([4],[15])
adderb.cx([2],[16])
adderb.cx([3],[16])
adderb.barrier()

adderb.measure([0,1,2,3,4,5],[0,1,2,3,4,5])
adderb.measure([14,15,16],[6,7,8])
adderb.barrier()

adderb.x([10,12,17])
adderb.mcx([10,12,13],[17])
adderb.x([10,12])
adderb.measure([17],[9])



simulator=Aer.get_backend('qasm_simulator')
resulta=execute(adderb, backend=simulator,shots=100).result()
hist(resulta.get_counts(adderb))



resultlist=[]



for i in resulta.get_counts(adderb):
    resultlist.append(i)



resultlist.sort()



resultt=[]

for val in resultlist:

    if int(val)<1000000:
        resultt.append(val)

resultt
