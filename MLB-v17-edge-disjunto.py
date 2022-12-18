#!/usr/bin/python
# coding: utf-8
'''
necessary packages:

	pip install networkx==2.2
	pip install requests
	apt-get install python-requests



##############################################################################################
Course	    : Master's Degree in Electronic Engineering
Student	    : Alisson Cavalcante e Silva
discipline  : Dissertation
Teacher     : Marcelo Rubinstein
Date        : 12/08/2019
Description : Algorithm based on the work of Nayan Seth adapted by Alisson Cavalcante.
            1- performs selection of paths with shorter disjoint links taking into account the weight equal to 1 for all edges (maximum flow theory);
            2- uses switch control;
            3- Uses openflow 1.0 (configure in mininet add switch topology).


##############################################################################################
'''

import requests
from requests.auth import HTTPBasicAuth
import json
import unicodedata

import sys
import time
from sys import exit
from datetime import datetime

# library that allows dictionary sorting
from operator import itemgetter

# library that allows working with graphs
import networkx as nx

# import library that allows calculation with time
from bib.diftime import DiferencaTempo

# import library that allows executing commands on the operating system from within python
from bib.command import systemCommand

# Method To Get REST Data In JSON Format
# Function responsible for requesting topology and switch status information from the controller
# Performs a GET on the URL, data is retrieved in .json format and later converted to python's dictionary structure format
def getResponse(url,choice):
    # Make a request via the northbound restconf API and retrieve data in json format
    response = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'))
    if(response.ok):
        # convert json data to dictionary format
        jData = json.loads(response.content)
        # Conditional to invoke a function that will handle information about topology or switch status 
        if(choice=="topology"):
            topologyInformation(jData)
        elif(choice=="statistics"):
            getStats(jData)
    else:
        response.raise_for_status()

# Function that processes data provided by the Northbound API about the topology. It also builds the "G" graph instance of the "nx.Graph()" class from the networkx library
def topologyInformation(data):
    global switch
    global deviceMAC
    global deviceIP
    global hostPorts
    global linkPorts
    global G
    global cost

    for i in data["network-topology"]["topology"]:
        for j in i["node"]:
            # Device MAC and IP
            # Retrieve IP and MAC data from existing hosts in the topology
            if "host-tracker-service:addresses" in j:
                for k in j["host-tracker-service:addresses"]:
                    ip = k["ip"].encode('ascii','ignore')
                    mac = k["mac"].encode('ascii','ignore')
                    deviceMAC[ip] = mac
                    deviceIP[mac] = ip

            # Device Switch Connection and Port
            # Retrieve the ID of the switches where the hosts (identified by IP) are connected
            if "host-tracker-service:attachment-points" in j:
                for k in j["host-tracker-service:attachment-points"]:
                    mac = k["corresponding-tp"].encode('ascii','ignore')
                    mac = mac.split(":",1)[1]
                    ip = deviceIP[mac]
                    temp = k["tp-id"].encode('ascii','ignore')
                    switchID = temp.split(":")
                    port = switchID[2]
                    hostPorts[ip] = port
                    switchID = switchID[0] + ":" + switchID[1]
                    # stores the host IP and the switch to which it is connected in the dictionary
                    switch[ip] = switchID

    # Link Port Mapping
    # Identifies links through switch:switch and port:port connection information. In the last instruction of the loop, the information of the links is loaded into the graph 
    for i in data["network-topology"]["topology"]:
        for j in i["link"]:
            if "host" not in j['link-id']:
                src = j["link-id"].encode('ascii','ignore').split(":")
                srcPort = src[2]
                dst = j["destination"]["dest-tp"].encode('ascii','ignore').split(":")
                dstPort = dst[2]
                srcToDst = src[1] + "::" + dst[1]
                linkPorts[srcToDst] = srcPort + "::" + dstPort
                # load the graph "G" with connection information between switches (information that allows identifying the edges of the graph)
                G.add_edge((int)(src[1]),(int)(dst[1]))


# Function responsible for requesting transmission and reception statistical data from the controller
def getStats(data):
    ##print "\nCost Computation....\n"
    global cost
    txRateA = 0
    txRateB = 0
	
	# traverse all nodes in the path 
    # path is passed from destination to source. Ex.: origin=1 destination=6 path = [6,5,4,3,2,1]
    # values are collected from the egress interfaces of the analyzed switches
    for i in data["node-connector"]:
        tx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["bytes"]["transmitted"])
        rx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["bytes"]["received"])
        txRateA = tx + rx
        
    time.sleep(3)
    response = requests.get(stats, auth=HTTPBasicAuth('admin', 'admin'))
    tempJSON = ""
    if(response.ok):
        tempJSON = json.loads(response.content)
    
    # traverse all nodes in the path 
    # path is passed from destination to source. Ex.: origin=1 destination=6 path = [6,5,4,3,2,1]
    # values are collected from the egress interfaces of the analyzed switches
    for i in tempJSON["node-connector"]:
        tx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["bytes"]["transmitted"])
        rx = int(i["opendaylight-port-statistics:flow-capable-node-connector-statistics"]["bytes"]["received"])
        txRateB = tx + rx
    #print('cost: {} '.format(cost))
    
    # receive the first cost collection
    # for the other collections, the one with the highest data transmission is checked. The larger one will be used to calculate the leak.
    if cost == 0: 
        cost = txRateB - txRateA
        #print('A')
    elif cost < (txRateB - txRateA):
        #print('B')
        cost = txRateB - txRateA
    
## Function for TCP and UDP streams
# function that applies flows to switches. It takes as parameters: path address, the number assigned to the path, and the flow number.  
def pushFlowRules(bestPath, f, origem, destino):
    # Configures the time in seconds that a NO usage flow rule will be active on the switch.
    # After this time, the rule will be removed from the switch, if it does not match.  
    idle_timeout = 0
    
    # get the path. The path is passed from destination to source. Ex.: origin=1 destination=6 path = [6,5,4,3,2,1]
    bestPath = bestPath.split("::")
    
    # loop configure path switches flow. Except the last switch of the path.
    for currentNode in range(0, len(bestPath)-1):
        
        # execute only once for the last node of the path
        if (currentNode==0):
            
            # port on the target switch to which the target host is connected
            inport = int(hostPorts[destino])
            # at each round it receives the identification of the current node
            srcNode = bestPath[currentNode]
            # at each round receive the identification of the next node
            dstNode = bestPath[currentNode+1]
            # get ports from the existing link between the current node and the next node
            # (format 'node::node':'port::port' e.g. '2::3':'1::2')
            outport = linkPorts[srcNode + "::" + dstNode]
            outport = outport.split("::")[0]
            
        # execute every round except the first round for the last node
        else:
            # get node before the current node
            prevNode = bestPath[currentNode-1]
            # get current node
            srcNode = bestPath[currentNode]
            dstNode = bestPath[currentNode+1]
            inport = linkPorts[prevNode + "::" + srcNode]
            inport = inport.split("::")[1]
            outport = linkPorts[srcNode + "::" + dstNode]
            outport = outport.split("::")[0]
        
        
        #
        ## TCP - ether-type (IP) = 2048 (decimal) = 0x0800 (hexadecimal)
        # upper layer protocol - 6 = TCP
        xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBTCP2' + str(f) + '</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-source>' + str(origem) + '/32</ipv4-source><ipv4-destination>' + str(destino) + '/32</ipv4-destination><ip-match><ip-protocol>6</ip-protocol></ip-match><tcp-destination-port>' + str(fluxo[f]) + '</tcp-destination-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>2' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
        xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBTCP3' + str(f) + '</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-source>' + str(destino) + '/32</ipv4-source><ipv4-destination>' + str(origem) + '/32</ipv4-destination><ip-match><ip-protocol>6</ip-protocol></ip-match><tcp-source-port>' + str(fluxo[f]) + '</tcp-source-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>3' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
        flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[currentNode] +"/table/0/flow/2" + str(f) + ""
        command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst
        systemCommand(command)
        flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[currentNode] +"/table/0/flow/3" + str(f) + ""
        command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc
        systemCommand(command)
        #
        ## UDP - ether-type (IP) = 2048 (decimal) = 0x0800 (hexadecimal)
        # upper layer protocol - 17 = UDP
        xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBUDP4' + str(f) + '</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-source>' + str(origem) + '/32</ipv4-source><ipv4-destination>' + str(destino) + '/32</ipv4-destination><ip-match><ip-protocol>17</ip-protocol></ip-match><udp-destination-port>' + str(fluxo[f]) + '</udp-destination-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>4' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
        
        xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBUDP5' + str(f) + '</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-source>' + str(destino) + '/32</ipv4-source><ipv4-destination>' + str(origem) + '/32</ipv4-destination><ip-match><ip-protocol>17</ip-protocol></ip-match><udp-source-port>' + str(fluxo[f]) + '</udp-source-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>5' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
        flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[currentNode] +"/table/0/flow/4" + str(f) + ""
        command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst
        systemCommand(command)
        flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[currentNode] +"/table/0/flow/5" + str(f) + ""
        command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc
        systemCommand(command)
        
       
    srcNode = bestPath[-1]
    prevNode = bestPath[-2]
    inport = linkPorts[prevNode + "::" + srcNode]
    inport = inport.split("::")[1]
    outport = int(hostPorts[origem])
    
    # Configure the last switch in the path
    ## TCP - ether-type (IP) = 2048 (decimal) = 0x0800 (hexadecimal)
    # upper layer protocol - 6 = TCP
    xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBTCP2' + str(f) + '</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-source>' + str(origem) + '/32</ipv4-source><ipv4-destination>' + str(destino) + '/32</ipv4-destination><ip-match><ip-protocol>6</ip-protocol></ip-match><tcp-destination-port>' + str(fluxo[f]) + '</tcp-destination-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>2' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
    
    xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBTCP3' + str(f) + '</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-source>' + str(destino) + '/32</ipv4-source><ipv4-destination>' + str(origem) + '/32</ipv4-destination><ip-match><ip-protocol>6</ip-protocol></ip-match><tcp-source-port>' + str(fluxo[f]) + '</tcp-source-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>3' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
    flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/2" + str(f) + ""
    command = 'curl --user \"admin\":\"admin\" -H \"Accept: application/xml\" -H \"Content-type: application/xml\" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst
    systemCommand(command)
    flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/3" + str(f) + ""
    command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc
    systemCommand(command)
    #
    ## UDP - ether-type (IP) = 2048 (decimal) = 0x0800 (hexadecimal)
    # upper layer protocol - 17 = UDP
    xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBUDP4' + str(f) + '</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-source>' + str(origem) + '/32</ipv4-source><ipv4-destination>' + str(destino) + '/32</ipv4-destination><ip-match><ip-protocol>17</ip-protocol></ip-match><udp-destination-port>' + str(fluxo[f]) + '</udp-destination-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>4' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
    
    xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBUDP5' + str(f) + '</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-source>' + str(destino) + '/32</ipv4-source><ipv4-destination>' + str(origem) + '/32</ipv4-destination><ip-match><ip-protocol>17</ip-protocol></ip-match><udp-source-port>' + str(fluxo[f]) + '</udp-source-port><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>5' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
    flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/4" + str(f) + ""
    command = 'curl --user \"admin\":\"admin\" -H \"Accept: application/xml\" -H \"Content-type: application/xml\" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst
    systemCommand(command)
    flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/5" + str(f) + ""
    command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc
    systemCommand(command)

## Function for ICMP streams
# function that applies flows to switches. It takes as parameters: path address, the number assigned to the path, and the flow number. 
def pushFlowRulesICMP(bestPath, f, origem, destino):
    # Configures the time in seconds that a NO usage flow rule will be active on the switch.
    # After this time, the rule will be removed from the switch, if it does not match. 
    idle_timeout = 0
    
    # get the path. The path is passed from destination to source. Ex.: origin=1 destination=6 path = [6,5,4,3,2,1]
    bestPath = bestPath.split("::")
    
    # loop configure path switches flow. Except the last switch of the path.
    for currentNode in range(0, len(bestPath)-1):
        
        # execute only once for the last node of the path
        if (currentNode==0):
            
            # port on the target switch to which the target host is connected
            inport = int(hostPorts[destino])
            # at each round it receives the identification of the current node
            srcNode = bestPath[currentNode]
            # at each round receive the identification of the next node
            dstNode = bestPath[currentNode+1]
            # get ports from the existing link between the current node and the next node
            # (format 'node::node':'port::port' e.g. '2::3':'1::2')
            outport = linkPorts[srcNode + "::" + dstNode]
            outport = outport.split("::")[0]
            
        # execute every round except the first round for the last node
        else:
            # get node before the current node
            prevNode = bestPath[currentNode-1]
            # get current node
            srcNode = bestPath[currentNode]
            dstNode = bestPath[currentNode+1]
            inport = linkPorts[prevNode + "::" + srcNode]
            inport = inport.split("::")[1]
            outport = linkPorts[srcNode + "::" + dstNode]
            outport = outport.split("::")[0]
        
        
        #
        ## TCP - ether-type (IP) = 2048 (decimal) = 0x0800 (hexadecimal)
        # upper layer protocol - 0 = ICMP - echo request = 8 - echo reply = 0
        xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBTCP6' + str(f) + '</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-source>' + str(origem) + '/32</ipv4-source><ipv4-destination>' + str(destino) + '/32</ipv4-destination><ip-match><ip-protocol>1</ip-protocol></ip-match><icmpv4-match><icmpv4-type>8</icmpv4-type></icmpv4-match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>6' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
        xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBTCP7' + str(f) + '</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-source>' + str(destino) + '/32</ipv4-source><ipv4-destination>' + str(origem) + '/32</ipv4-destination><ip-match><ip-protocol>1</ip-protocol></ip-match><icmpv4-match><icmpv4-type>0</icmpv4-type></icmpv4-match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>7' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
        flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[currentNode] +"/table/0/flow/6" + str(f) + ""
        command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst
        systemCommand(command)
        flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[currentNode] +"/table/0/flow/7" + str(f) + ""
        command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc
        systemCommand(command)
       
       
    srcNode = bestPath[-1]
    prevNode = bestPath[-2]
    inport = linkPorts[prevNode + "::" + srcNode]
    inport = inport.split("::")[1]
    outport = int(hostPorts[origem])
    
    #
    ## TCP - ether-type (IP) = 2048 (decimal) = 0x0800 (hexadecimal)
    # upper layer protocol - 0 = ICMP - echo request = 8 - echo reply = 0 
    xmlSrcToDst = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBICMP6' + str(f) + '</flow-name><match><in-port>' + str(outport) +'</in-port><ipv4-source>' + str(origem) + '/32</ipv4-source><ipv4-destination>' + str(destino) + '/32</ipv4-destination><ip-match><ip-protocol>1</ip-protocol></ip-match><icmpv4-match><icmpv4-type>8</icmpv4-type></icmpv4-match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>6' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(inport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
    xmlDstToSrc = '\'<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?><flow xmlns=\"urn:opendaylight:flow:inventory\"><priority>200</priority><flow-name>LBICMP7' + str(f) + '</flow-name><match><in-port>' + str(inport) +'</in-port><ipv4-source>' + str(destino) + '/32</ipv4-source><ipv4-destination>' + str(origem) + '/32</ipv4-destination><ip-match><ip-protocol>1</ip-protocol></ip-match><icmpv4-match><icmpv4-type>0</icmpv4-type></icmpv4-match><ethernet-match><ethernet-type><type>2048</type></ethernet-type></ethernet-match></match><id>7' + str(f) + '</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>0</order><output-action><output-node-connector>' + str(outport) +'</output-node-connector></output-action></action></apply-actions></instruction></instructions><idle-timeout>' + str(idle_timeout) + '</idle-timeout></flow>\''
    flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/6" + str(f) + ""
    command = 'curl --user \"admin\":\"admin\" -H \"Accept: application/xml\" -H \"Content-type: application/xml\" -X PUT ' + flowURL + ' -d ' + xmlSrcToDst
    systemCommand(command)
    flowURL = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ bestPath[-1] +"/table/0/flow/7" + str(f) + ""
    command = 'curl --user "admin":"admin" -H "Accept: application/xml" -H "Content-type: application/xml" -X PUT ' + flowURL + ' -d ' + xmlDstToSrc
    systemCommand(command)
    
    
# function that takes all disjoint paths computed by the edge_disjoint function from the networkx library and returns the shortest disjoint paths of equal cost.
def shortest(lista):
    dis1 = []
    dis2 = []
    dis3 = []
    for i in lista:
        dis1.append(i)
        # find length of each path
        dis2.append(len(i)) 
    # sort by length of found paths
    dis2.sort()
    # compare path lengths with the smallest path length found
    for i in dis1:
        if len(i) == dis2[0]:
            dis3.append(i)
    return dis3


################################################################################################################################## 
################################################################# Main ###########################################################
##################################################################################################################################

def main():
    
    command = './2-do_curl-delete.sh'
    #command = 'source 2-do_curl-delete.sh'
    #systemCommand(command)
        
    # Global variables used to store the source (sw1) and destination (sw2) host identification.
    global sw1, sw2, G, switch, deviceMAC, deviceIP, hostPorts, linkPorts, fluxo
    
    # source switch
	sw1 = 1
    
	# target switch
	sw2 = 8
    
    # number of streams
	qtd_fluxos = 3
    
    fluxo = {0: "5001", 1: "5002", 2: "5003", 3:"5004"}
    origem = {0: "10.0.0.1", 1: "10.0.0.2", 2:"10.0.0.3", 3:"10.0.0.4"}
    destino = {0: "10.0.0.5", 1: "10.0.0.6", 2: "10.0.0.7", 3:"10.0.0.8"}
    
    db={0: '', 1: '', 2: ''}
    
    flag = True
    
    while flag:
        # record the start time
        t_inicial = time.time()
        
        # Create the graph G from the Graph class of the networkx library
        G = nx.Graph()
    
        # Declare dictionary structure that will receive IP from hosts that are connected to topology switches - IP Hosts:switch
        switch = {}
    
        # Declare dictionary structure that will receive MAC addresses from topology hosts - IP:MAC
        deviceMAC = {}
    
        # Declare the structure of the dictionary that will receive IP addresses from the topology hosts - MAC:IP
        deviceIP = {}
    
        # Declare the structure of the dictionary that will receive
        switchLinks = {}
        
        # Declare the dictionary structure that will receive the port to which the host is connected on the switch - IP:port
        hostPorts = {}
    
        # Declare the dictionary structure that will receive the existing paths in the topology
        path = {}
        
        # Declare the structure of the dictionary that will receive the port of the links - 'switch:switch':'port:port'
        linkPorts = {}
        
        # Stores Final Link Rates
        finalLinkTX = {}
        
        # Store Port Key For Finding Link Rates
        portKey = ""
        
        # Statistics
        global stats
        stats = ""
        
        # Global variable used to store the cost of the path (it stores the cost of each link belonging to the path)
        global cost
        cost = 0
    
        try:
            # URL for accessing the controller that will be used in the request via the northbound restconf API and that will return topology information 
            topology = "http://127.0.0.1:8181/restconf/operational/network-topology:network-topology"
            # Calls the function responsible for requesting information about the topology from the controller. receives as a parameter the URL and the type of information that will be requested
            getResponse(topology,"topology")
            
            tmp = ""
            
			# Sequential distribution of flows in the paths (ordered by the used data band). The amount of flows is distributed by the number of paths.
            for f in range(0,qtd_fluxos):
                
                #for currentPath in nx.all_shortest_paths(G, int(sw2), int(sw1), weight=1, method='dijkstra'):
                for currentPath in nx.edge_disjoint_paths(G, int(sw2), int(sw1), flow_func=None):
                    #qtd_caminhos = qtd_caminhos + 1
                    for node in range(0,len(currentPath)-1):
                        #print('\nnode posicao : {}' .format(str(node)))
                        #print('node : {}' .format(str(currentPath[node])))
                        tmp = tmp + str(currentPath[node]) + "::"
                        #print('tmp : {}' .format(tmp))
                        key = str(currentPath[node])+ "::" + str(currentPath[node+1])
                        #print('key: {}' .format(key))
                        port = linkPorts[key]
                        #print('port : {}' .format(port))
                        port = port.split(":",1)[0]
                        port = int(port)
                        #print('port : {}' .format(port))
                        #print('node-conector {}:{}' .format(str(currentPath[node]),port))
                        stats = "http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:"+str(currentPath[node])+"/node-connector/openflow:"+str(currentPath[node])+":"+str(port)
                        getResponse(stats,"statistics")
                    tmp = tmp + str(currentPath[len(currentPath)-1])
                    #print('tmp : {}' .format(tmp))
                    tmp = tmp.strip("::")
                    #print('tmp : {}' .format(tmp))
                    
                    # uses the value stored in the cost variable (which has the total cost, sum of TX and RX of all links in the path) and divides it by the number of nodes in the path.
                    # Takes an average of the cost value (TX + RX). The average value returned is in bytes, so multiply by 8 bits to have the value expressed in bits. And after,
                    # is divided by the time interval referring to data collection, in this case 3 seconds.
                    vazao = int((cost * 8 ) / float(3))
                    
                    # cost metric will be: bandwidth nominal value divided by available bandwidth (nominal value minus throughput)
                    custo = (10100000 / float(10100000 - vazao))
                    print('caminho:{} - vazao:{}bps - custo:{}'.format(currentPath, vazao, custo))
                    
                    finalLinkTX[tmp] = vazao
                    #print('finalLinkTX : {}' .format(finalLinkTX))
                    cost = 0
                    tmp = ""
            
                print('\n\033[1;31m Custo final: {} \033[m' .format(sorted(finalLinkTX.items(), key=itemgetter(1))))
            
                # Block that performs switching control
                if (db[f]==''):
                    db[f] = sorted(finalLinkTX, key=finalLinkTX.get)[0]
                    print (db)
                    # call function that configures flow in switches starting from the lowest cost path to the highest cost path
                    pushFlowRules(sorted(finalLinkTX, key=finalLinkTX.get)[0], f, origem[f], destino[f])
                    pushFlowRulesICMP(sorted(finalLinkTX, key=finalLinkTX.get)[0], 0, origem[f], destino[f])
                    print('\nPrimeiro Cadastro de fluxo!!!!! \n')
				elif (sorted(finalLinkTX, key=finalLinkTX.get)[0] != db[f]   and  finalLinkTX[sorted(finalLinkTX, key=finalLinkTX.get)[0]] <  finalLinkTX[db[f]]   and  (finalLinkTX[sorted(finalLinkTX, key=finalLinkTX.get)[0]] / float(finalLinkTX[db[f]])) * 100 < 90  and (float(finalLinkTX[db[f]])/float(10100000)) * 100 > 50 ):
                    print('\n### Caminho Mudou !!! ###\n')
                    db[f] = sorted(finalLinkTX, key=finalLinkTX.get)[0]
                    # call function that configures flow in switches starting from the lowest cost path to the highest cost path
                    pushFlowRules(sorted(finalLinkTX, key=finalLinkTX.get)[0], f, origem[f], destino[f])
                    pushFlowRulesICMP(sorted(finalLinkTX, key=finalLinkTX.get)[0], 0, origem[f], destino[f])
                    
                else:
                    print('\n### Manteve caminho !!! ####################################\n')
                
                
                now = datetime.now()
                command = 'echo ' + str(now.hour)+ ':' + str(now.minute) + ':' + str(now.second) + ' - Fluxo: ' + str(sorted(finalLinkTX, key=finalLinkTX.get)[0]) + ' - ' + str(f)+ ' >> ./resultado/reg-fluxo.txt'
                systemCommand(command)
                            
            # record the end time
            t_final = time.time()
            # returns total time of each round performed by the loop (while flag), subtracts between final time and initial time calculation 
            diftempo = DiferencaTempo(t_final, t_inicial)
            print('\033[1;31m \n### Final da Rodada do algoritmo: {} ms ou {} s\033[m\n'.format(diftempo.getMilisegundos(), diftempo.getSegundos()))
            
        except KeyboardInterrupt:
            break
            exit

if __name__ == '__main__':
    main()
    
