#!/bin/bash
export LOCALADDR="19-ffaa:1:153,[10.0.8.58]"
export BWCONFIG="3,1000,?,30Mbps"
rm networkSpeedMap.scd
go run bwtestpaths.go -c $LOCALADDR:30102 -s 17-ffaa:0:1102,[192.33.93.177]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 17-ffaa:1:13,[192.168.1.111]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 17-ffaa:1:f,[10.0.2.15]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 19-ffaa:1:22,[141.44.25.146]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 17-ffaa:0:1107,[10.0.8.1]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 18-ffaa:0:1202,[10.0.8.1]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 19-ffaa:0:1303,[10.0.8.1]:30100 -cs $BWCONFIG -sc $BWCONFIG
go run bwtestpaths.go -c $LOCALADDR:30102 -s 20-ffaa:0:1404,[10.0.8.1]:30100 -cs $BWCONFIG -sc $BWCONFIG
#go run bwtestpaths.go -c 19-ffaa:1:12d,[10.0.8.21]:30102 -s
./parseDump.py networkSpeedMap.scd 10000000 25000000
dot -Tpng networkSpeedMap.scd.dot -o networkSpeedMap.png
