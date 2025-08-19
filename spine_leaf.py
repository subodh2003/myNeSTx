from nest.topology import *
from nest.topology.address_helper import AddressHelper as ah

#create 2 spines sr1 and sr2
sr1 = Router("sr1")         
sr2 = Router("sr2")

#create 4 leafs l1, l2, l3, l4
lr1 = Router("lr1")
lr2 = Router("lr2")
lr3 = Router("lr3")
lr4 = Router("lr4")

#create 1 node for each leaf lr{1..4} and n{1..4} respectively

n1 = Node("n1")
n2 = Node("n2")
n3 = Node("n3")
n4 = Node("n4")

#connect all four leafs to each spines 
#esr1{a,b,c,d}
#esr2{a,b,c,d}
#elr1{a,b}
#elr2{a,b}
#elr3{a,b}
#elr4{a,b}
#do not connect spines to each other and same for the leafs
try:
    (esr1a,elr1a) = connect(sr1,lr1)
    (esr1b,elr2a) = connect(sr1,lr2)
    (esr1c,elr3a) = connect(sr1,lr3)
    (esr1d,elr4a) = connect(sr1,lr4)

    (esr2a,elr1b) = connect(sr2,lr1)
    (esr2b,elr2b) = connect(sr2,lr2)
    (esr2c,elr3b) = connect(sr2,lr3)
    (esr2d,elr4b) = connect(sr2,lr4)

    #do the same for nodes 
    #connect each node to each leaf elr{1..4}n and en{1..4} respectively
    (elr1n,en1) = connect(lr1,n1)
    (elr2n,en2) = connect(lr2,n2)
    (elr3n,en3) = connect(lr3,n3)
    (elr4n,en4) = connect(lr4,n4)

    #assign IPv4 addresses to all the interfaces in network
    esr1a.set_address("192.168.1.0/24")
    esr1b.set_address("192.168.2.0/24")
    
    elr1a.set_address("192.168.1.1/24")
    elr2a.set_address("192.168.2.1/24")
    
    elr1n.set_address("192.169.1.1/24")
    en1.set_address("192.169.1.2/24")

    elr2n.set_address("192.169.1.1/24")
    en2.set_address("192.169.1.2/24")

    #set the link attributes
    elr1a.set_attributes("5mbit","5ms")
    elr1b.set_attributes("5mbit","5ms")
    elr2a.set_attributes("5mbit","5ms")
    elr2b.set_attributes("5mbit","5ms")
    elr3a.set_attributes("5mbit","5ms")
    elr3b.set_attributes("5mbit","5ms")
    elr4a.set_attributes("5mbit","5ms")
    elr4b.set_attributes("5mbit","5ms")

    esr1a.set_attributes("10mbit","10ms")
    esr1b.set_attributes("10mbit","10ms")
    esr1c.set_attributes("10mbit","10ms")
    esr1d.set_attributes("10mbit","10ms")

    esr2a.set_attributes("10mbit","10ms")
    esr2b.set_attributes("10mbit","10ms")
    esr2c.set_attributes("10mbit","10ms")
    esr2d.set_attributes("10mbit","10ms")

    elr1n.set_attributes("5mbit","5ms")
    elr2n.set_attributes("5mbit","5ms")
    elr3n.set_attributes("5mbit","5ms")
    elr4n.set_attributes("5mbit","5ms")

    n1.add_route("DEFAULT", en1, elr1n.address)
    lr1.add_route("DEFAULT", elr1a, esr1a.address)
    sr1.add_route("DEFAULT", esr1a, elr2a.address)
    lr2.add_route("DEFAULT", elr2n, en2.address)

    n2.add_route("DEFAULT", en2, elr2n.address)
    lr2.add_route("DEFAULT", elr2a, esr1b.address)
    sr1.add_route("DEFAULT", esr1a, elr1a.address)
    lr1.add_route("DEFAULT", elr1n, en1.address)

    n1.ping(en2.address)

finally:
    print("Exiting...")
