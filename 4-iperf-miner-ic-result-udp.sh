rm -rf ./resultado/IC_iperf_band_rslt.txt
rm -rf ./resultado/IC_iperf_vol_rslt.txt
rm -rf ./resultado/IC_iperf_jitter_rslt.txt
rm -rf ./resultado/IC_iperf_loss_rslt.txt
rm -rf ./resultado/IC_iperf_loss_percet_rslt.txt
rm -rf ./resultado/IC_justica_rslt.txt
#
#
#
#
# mine host and server data
python 4-iperf-miner-ic-result.py h1f1u
python 4-iperf-miner-ic-result.py s5f1u
python 4-iperf-miner-ic-result.py h2f2u
python 4-iperf-miner-ic-result.py s6f2u
python 4-iperf-miner-ic-result.py h3f3u
python 4-iperf-miner-ic-result.py s7f3u
python 4-iperf-miner-ic-result.py h4f4u
python 4-iperf-miner-ic-result.py s8f4u
#
#
# sum for the servers
python 4-iperf-soma-server.py s5f1u,s6f2u,s7f3u,s8f4u
#python 4-iperf-soma-server.py s5f1u,s6f2u
#
python 5-ic-justica.py s5f1u,s6f2u,s7f3u,s8f4u
#python 5-ic-justica.py s5f1u,s6f2u

