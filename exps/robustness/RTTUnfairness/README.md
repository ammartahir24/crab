This experiment shares a 30Mbps link between 2 flows in 2:1 which are controlled by us. We use different RTTs for both flows. You may modify the `delay.sh` file at line 14-15 for any arbitrary values of delay for flow 1 and 2 respectively.

Add `config.py` to `src/` directory, and run crab.

Then run `delay.sh` on other Linux machine after modifying delay values.

Run `python3 iperf_servers.py 3` on other Linux machine

Run `python3 delay_clients.py 3` on end-device.