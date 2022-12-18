#!/bin/bash
#
# stream number is tied to port, so stream 1 = 5001, stream 2 = 5002, ...
#
# syntax: <source-node> <destination-IP> <stream-id/port>
#
# '&' used at the end of the command to run a process in the background. So it is possible to start more than one flow per execution
# Examples: 
#
#
#
#
py h1.cmd('python 3-iperf.py h1 10.0.0.5 1 udp &')
py h2.cmd('python 3-iperf.py h2 10.0.0.6 2 udp &')
py h3.cmd('python 3-iperf.py h3 10.0.0.7 3 udp &')
py h4.cmd('python 3-iperf.py h4 10.0.0.8 4 udp &')

