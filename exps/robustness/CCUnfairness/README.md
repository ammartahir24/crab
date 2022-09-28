This experiment shares a 30Mbps link between 2 flows in 2:1 which are controlled by us. We use different congestion controllers for both flows. Cubic may exist by default but you may need to load BBR module via:

- `sudo modprobe -a tcp_bbr`
- To verify check `/sbin/sysctl net.ipv4.tcp_available_congestion_control`

Add `config.py` to `src/` directory, and run crab.

Then run `bottleneck.sh` on other Linux machine.

Run `python3 iperf_servers.py 3` on other Linux machine

Run `python3 cclients.py bbr cubic` on end-device to run flow 1 with BBR and flow 2 with Cubic.