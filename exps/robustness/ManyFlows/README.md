This experiment shares a 60Mbps link between 3,6,12 and 24 flows. `config.py` file for each is given in respective directory.

Add `config.py` to `src/` directory, and run crab.

Then run `bottleneck.sh` on other Linux machine.

Run `python3 iperf_servers.py 24` on other Linux machine

Run `python3 iperf3_clients.py n` on end-device to run n flow experiment where n $\in$ {3,6,12,24}.