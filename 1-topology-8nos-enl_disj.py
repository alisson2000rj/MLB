#!/usr/bin/python
# coding: utf-8

# libraries used for interrupt handling - signal and sys
import signal
import sys

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel


def terminateProcess(signalNumber, frame):
    #print ('(SIGTERM) terminating the process')
    print('\n Interrupção manual provocada pelo usuário, Ctrl + c. \n')
    #print('Received:', signalNumber)
    sys.exit()

def receiveSignal(signalNumber, frame):
    print('\n Para interromper execução do Mininet execute o comando "exit". \n')
    return


def remoteControllerNet():
    
    ## interrupt handling
    # SIGINT = Ctrl + c
    signal.signal(signal.SIGINT, receiveSignal)
    # SIGINT = Ctrl + \
    signal.signal(signal.SIGQUIT, receiveSignal)
    # SIGINT = Ctrl + z
    signal.signal(signal.SIGTSTP, receiveSignal)
    
    
    
    
    "Create a network from semi-scratch with multiple controllers."
	
    net = Mininet( controller=None, switch=OVSSwitch, link=TCLink )
    #net = Mininet( controller=None, switch=OVSKernelSwitch, link=TCLink )
    
    
    print "*** Creating (reference) controllers, which is listening on port 6633"
    #c1 = net.addController( 'c1', controller=RemoteController, ip='192.168.15.209', port=6633 )
    c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=6633 )
    
    print "*** Creating switches"
    
    
    s1 = net.addSwitch( 's1', protocols='OpenFlow10' )
    s2 = net.addSwitch( 's2', protocols='OpenFlow10' )
    s3 = net.addSwitch( 's3', protocols='OpenFlow10' )
    s4 = net.addSwitch( 's4', protocols='OpenFlow10' )
    s5 = net.addSwitch( 's5', protocols='OpenFlow10' )
    s6 = net.addSwitch( 's6', protocols='OpenFlow10' )
    s7 = net.addSwitch( 's7', protocols='OpenFlow10' )
    s8 = net.addSwitch( 's8', protocols='OpenFlow10' )
    '''
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    s7 = net.addSwitch('s7')
    s8 = net.addSwitch('s8')
    '''
    h1 = net.addHost( 'h1', ip='10.0.0.1', mac='00:00:00:00:00:01' )
    h2 = net.addHost( 'h2', ip='10.0.0.2', mac='00:00:00:00:00:02' )
    h3 = net.addHost( 'h3', ip='10.0.0.3', mac='00:00:00:00:00:03' ) 
    h4 = net.addHost( 'h4', ip='10.0.0.4', mac='00:00:00:00:00:04' )
    
    
    h5 = net.addHost( 'h5', ip='10.0.0.5', mac='00:00:00:00:00:05' )
    h6 = net.addHost( 'h6', ip='10.0.0.6', mac='00:00:00:00:00:06' )
    h7 = net.addHost( 'h7', ip='10.0.0.7', mac='00:00:00:00:00:07' )
    h8 = net.addHost( 'h8', ip='10.0.0.8', mac='00:00:00:00:00:08' )
    
    
    print "*** Creating links"
    
 
    # Source
    net.addLink( s1, h1, bw=10, delay='0ms', loss=0, use_htb=True )
    net.addLink( s1, h2, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s1, h3, bw=10, delay='0ms', loss=0, use_htb=True ) 
    
    # destiny
    net.addLink( s8, h5, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s8, h6, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s8, h7, bw=10, delay='0ms', loss=0, use_htb=True )  
    
    # Level 1
    net.addLink( s1, s2, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s1, s3, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s1, s4, bw=10, delay='0ms', loss=0, use_htb=True ) 
    
    # Level 2
    net.addLink( s2, s5, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s2, s6, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s3, s6, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s4, s6, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s4, s7, bw=10, delay='0ms', loss=0, use_htb=True ) 
    
    # Level 3
    net.addLink( s5, s8, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s6, s8, bw=10, delay='0ms', loss=0, use_htb=True ) 
    net.addLink( s7, s8, bw=10, delay='0ms', loss=0, use_htb=True ) 
    
    # Source
    net.addLink( s1, h4, bw=10, delay='0ms', loss=0, use_htb=True ) 
	# destiny
    net.addLink( s8, h8, bw=10, delay='0ms', loss=0, use_htb=True ) 
    '''
    
    # Origem
    net.addLink( s1, h1, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    net.addLink( s1, h2, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    net.addLink( s1, h3, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    
    # destino
    net.addLink( s8, h5, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s8, h6, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    net.addLink( s8, h7, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    
    # Nível 1
    net.addLink( s1, s2, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    net.addLink( s1, s3, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False )
    net.addLink( s1, s4, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    
    # Nível 2 
    net.addLink( s2, s5, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s2, s6, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s3, s6, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s4, s6, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s4, s7, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    
    # Nível 3
    net.addLink( s5, s8, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s6, s8, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s7, s8, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    
    
    net.addLink( s1, h4, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    net.addLink( s8, h8, bw=10, delay='0ms', loss=0, use_htb=True, gro = False, txo = False, rxo = False ) 
    '''
    
    s1 = net.get( 's1' )
    s1.intf( 's1-eth1' ).setMAC( '00:00:00:01:00:01' )
    s1.intf( 's1-eth2' ).setMAC( '00:00:00:01:00:02' )
    s1.intf( 's1-eth3' ).setMAC( '00:00:00:01:00:03' )
    s1.intf( 's1-eth4' ).setMAC( '00:00:00:01:00:04' )
    s1.intf( 's1-eth5' ).setMAC( '00:00:00:01:00:05' )
    s1.intf( 's1-eth6' ).setMAC( '00:00:00:01:00:06' )
    s1.intf( 's1-eth7' ).setMAC( '00:00:00:01:00:07' )
    
    
    s2 = net.get( 's2' )
    s2.intf( 's2-eth1' ).setMAC( '00:00:00:02:00:01' )
    s2.intf( 's2-eth2' ).setMAC( '00:00:00:02:00:02' )
    s2.intf( 's2-eth3' ).setMAC( '00:00:00:02:00:03' )
    
    s3 = net.get( 's3' )
    s3.intf( 's3-eth1' ).setMAC( '00:00:00:03:00:01' )
    s3.intf( 's3-eth2' ).setMAC( '00:00:00:03:00:02' )
    
    s4 = net.get( 's4' )
    s4.intf( 's4-eth1' ).setMAC( '00:00:00:04:00:01' )
    s4.intf( 's4-eth2' ).setMAC( '00:00:00:04:00:02' )
    s4.intf( 's4-eth3' ).setMAC( '00:00:00:04:00:03' )
    
    s5 = net.get( 's5' )
    s5.intf( 's5-eth1' ).setMAC( '00:00:00:05:00:01' )
    s5.intf( 's5-eth2' ).setMAC( '00:00:00:05:00:02' )
    
    
    s6 = net.get( 's6' )
    s6.intf( 's6-eth1' ).setMAC( '00:00:00:06:00:01' )
    s6.intf( 's6-eth2' ).setMAC( '00:00:00:06:00:02' )
    s6.intf( 's6-eth3' ).setMAC( '00:00:00:06:00:03' )
    s6.intf( 's6-eth4' ).setMAC( '00:00:00:06:00:04' )
  
    
    s7 = net.get( 's7' )
    s7.intf( 's7-eth1' ).setMAC( '00:00:00:07:00:01' )
    s7.intf( 's7-eth2' ).setMAC( '00:00:00:07:00:02' )
    
    s8 = net.get( 's8' )
    s8.intf( 's8-eth1' ).setMAC( '00:00:00:08:00:01' )
    s8.intf( 's8-eth2' ).setMAC( '00:00:00:08:00:02' )
    s8.intf( 's8-eth3' ).setMAC( '00:00:00:08:00:03' )
    s8.intf( 's8-eth4' ).setMAC( '00:00:00:08:00:04' )
    s8.intf( 's8-eth5' ).setMAC( '00:00:00:08:00:05' )
    s8.intf( 's8-eth6' ).setMAC( '00:00:00:08:00:06' )
    s8.intf( 's8-eth7' ).setMAC( '00:00:00:08:00:07' )
    
        
    print "*** Iniciando a rede"
    '''
    net.build()
    c1.start()
    s1.start( [ c1 ] )
    s2.start( [ c1 ] )
    s3.start( [ c1 ] )
    s4.start( [ c1 ] )
    s5.start( [ c1 ] )
	'''
    print "*** Iniciando rede \n"
    net.start()
    
    #h2.cmd("iperf -s -u &")
    #h2.cmd("iperf -s &")
    
    
    print "*** Running CLI"
    CLI( net )
    
    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    remoteControllerNet()

