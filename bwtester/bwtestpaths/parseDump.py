#!/usr/bin/env python3
import sys
class ScionNode:
	def __init__(self, AS=None, inIF=None, outIF=None):
		self.inIF = inIF
		self.outIF = outIF
		self.AS = AS
	def __str__(self):
		return "AS: "+self.AS+" inIF: " + str(self.inIF) +" outIF: "+str(self.outIF)
	def __repr__(self):
		return self.__str__()
	def equals(self, sn):
		return (self.inIF == sn.inIF and self.outIF == sn.outIF or self.inIF==sn.outIF and self.outIF == sn.inIF) and self.AS == sn.AS
def parsePath(path):
	nodes = path.split(">")
	snodes = []
	for n in nodes:
		inIF = None
		outIF = None
		if len(n.split(" ")) > 2:
			inIF, AS, outIF = n.split(" ")
		else:
			if len(snodes) == 0: #first ode, only has outIF
				AS, outIF = n.split(" ")
			else: #last node
				inIF, AS = n.split(" ")
		snodes.append(ScionNode(AS, inIF, outIF))
	return snodes
def addPath(network, path, up, down):
	for sn in path:
		contained = False
		networkNode = None
		for n in network:
			if n.equals(sn):
				contained=True
				break
		if not contained:
			network.append(sn)
def getAS(network):
	asList = []
	for n in network:
		if n.AS in asList:
			continue
		asList.append(n.AS)
	return asList
def getSinks(paths):
	sinks=[]
	for path in paths:
		if path[-1] in sinks:
			continue
		sinks.append(path[-1])
	return sinks
def toDot(network, paths, linkSpeeds, slowLinkUp=1000, slowLinkDown=1000):
	start = """
	digraph G {
	"""
	end =  "\""+paths[0][0].AS+"_"+paths[0][0].outIF +"\" [shape=Mdiamond];\n"+"}\n"
	asList = getAS(network)
	sgraphs = []
	for a in asList:
		s = "subgraph \"cluster_" + a + "\"{\n label=\""+a+"\";\n"
		s += """graph[style=dotted];
		color=blue;"""
#		node [style=filled,color=white];"""
		for sn in network:
			if sn.AS == a:
				if not sn.inIF is None:
					s += " \"" + sn.AS+"_"+sn.inIF + "\" ->"
				if not sn.outIF is None:
					s += " \"" + sn.AS +"_"+sn.outIF + "\" ->"
		s = s[:-2] + "[color=grey arrowhead=none];\n}\n"
		sgraphs.append(s)
	links = []
	for link,speeds in linkSpeeds.items():
		n1,n2=link
		up, down = speeds
		speedsStr="up/down: {:.2E}/{:.2E}".format(up, down)
		linkColour = "black"
		if up < slowLinkUp or down < slowLinkDown:
			linkColour="red"
		links.append("\"" +n1+"\" -> \"" + n2+ "\" [label=\""+ speedsStr +"\" color=\""+linkColour+"\" dir=\"both\"];\n")
	sinks = getSinks(paths)
	endNodes = []
	for s in sinks:
		endNodes.append("\""+s.AS+"_"+s.inIF+"\" [style=filled, fillcolor=blue];\n")
	#assemble dot
	dot = start
	for g in sgraphs:
		dot += g
	for l in links:
		dot += l
	for e in endNodes:
		dot += e
	return dot + end

if len(sys.argv) != 4:
	print("Usage: $script dumpFile uploadWarn downloadWarn\n")
	exit(1)
with open(sys.argv[1]) as f:
	content = f.readlines()
network = []
paths = []
linkSpeeds = {}
print(content)
for line in content:
	path, rem = line.split("]")
	dummy, path = path.split("[")
	dummy, mtu, down, up = rem.split(":")
	mtu = int(mtu.split(" ")[1])
	down = int(down.split(" ")[1])
	up = int(up)
	path = parsePath(path)
	addPath(network, path, up, down)
	paths.append(path)
	for i in range(0,len(path)-1):
		n1 = path[i]
		n2 = path[i+1]
		linkID = (n1.AS+"_"+n1.outIF, n2.AS+"_"+n2.inIF)
		nwUp, nwDown = (up, down)
		if linkID in linkSpeeds:
			nwUp, nwDown = linkSpeeds[linkID]
			if up > nwUp:
				nwUp = up
			if nwDown < down:
				nwDown = down
		linkSpeeds[linkID]=(nwUp, nwDown)
#print(network)
#print(linkSpeeds)
print(toDot(network, paths, linkSpeeds,int(sys.argv[2]), int(sys.argv[3])))
