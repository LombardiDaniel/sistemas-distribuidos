import rpyc

c = rpyc.connect("localhost", 18861)

print(c.root.add(6, 9))
