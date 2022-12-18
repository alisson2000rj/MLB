#################################################
#Initial instructions for carrying out the tests#
#################################################

#################### Environment Preparation ###########################

0) open 5 bash terminals or open terminator and split into 5 windows.


1) load opendaylight controller
linux-t1> karaf-0.6.1-Carbon> ./bin/karaf

2) load mininet with topology using the following command
linux-t2> sudo mn -c
linux-t2> sudo python 1-topology-8nos-enl_disj.py

inside the mininet:
mininet> pingall


NOTE: it is necessary to perform a pingall or ping from the source to the destination so that the controller knows the topology and configures flow rules on the switches


3) delete old rules configured in opendaylight controller
linux-t3> ./2-delete.sh

4) insert rules so that the background stream is sent through the default path
linux-t3> source ./2-ff-caminho-padrao.sh

################## Data Collection - IPERF - Flow Rate and Transferred Volume ################

4) load servers

mininet> xterm h5 h6 h7 h8

h5> iperf -s -f bits -p 5001> ./resultado/s5f1t.txt
h6> iperf -s -f bits -p 5002> ./resultado/s6f2t.txt
h7> iperf -s -f bits -p 5003> ./resultado/s7f3t.txt
h8> iperf -s -f bits -p 5004> ./resultado/s8f4t.txt

NOTE: s<server-number>flow<flow-number><flow-type>.txt
stream type can be tcp(t) or udp(u)



5) load load balancing algorithm

linux-t4> python MLB-v17-edge-disjunto.py


6) loads the clean rule, script that allows iperf runs to happen simultaneously. In addition, the script is responsible for sending an email at the end of each simulation
linux-t3> python limpa-regras.py


7) at the mininet prompt, load the clients in parallel and wait for completion
mininet> 
source 3-iperf-tcp.sh
ou
source 3-iperf-udp.sh

NOTE: after finishing stop iperf servers
 
############################### Mining ###########################################################

NOTE: after I finish stopping iperf servers

8) in linux prompt type below command to mine data and present IC
linux> 
source 4-iperf-miner-ic-result-tcp.sh 
ou
source 4-iperf-miner-ic-result-udp.sh 

9) in linux prompt type command below to mine occupancy rate
linux> 
source 9-ocupacao.sh


############################# graphics ############################################


compor arquivos de dados no caminho \resultado\8nos\graficos-2f e \resultado\8nos\graficos-4f
1-8nos-proativo-band.txt
2-8nos-proativo-loss.txt
3-8nos-proativo-justica.txt


10) at the linux prompt run gnuplot
LINUX> 
gnuplot -e "titulo=''" d-gnuplot-iperf-band-proativo.txt
gnuplot -e "titulo=''" e-gnuplot-loss-proativo.txt
gnuplot -e "titulo=''" f-gnuplot-justica-proativo.txt


###################################################################
#################### PING - ICMP ##################################
###################################################################

1) at the mininet prompt 
example:
mininet> 
source 7-icmp.sh

2) in linux prompt
linux> 
source 8-icmp-miner-ic-result.sh


######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
######################################################################


########## Iperf command ####################

server tcp 
iperf -s -f bits > ./resultado/h3.txt

client tcp 
iperf -c 10.0.0.2 -f bits -p 5001 -t 20 >> ./resultado/h1f1.txt

server udp 
iperf -s -f bits -u > ./resultado/h3.txt

client udp
iperf -c 10.0.0.2 -f bits -p 5001 -t 20 -u -b 5m >> ./resultado/h1f1.txt


################ Mininet commands ##########################

## check rules on switch
mininet> sh ovs-ofctl dump-flows s1

## clear garbage in mininet
linux> mn -c
