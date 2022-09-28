This experiment shares a 10Mbps link between web browsing traffic and bulk flows in ratio of 7:3. 

- `browsing.py`: (runs at end-device) Emulates browsing session with more than 100 webpage loads, measures page load times and records traffic.


For each setting, there are two folders: `end-device` and `router`. `config.py` files needs to be placed in `src` directory before running `src/crab.py` for CRAB experiment. Similarly all shell files need to be executed appropirately at end-device or router before running `python3 browsing.py` on end-device.

Experiments:

- CRAB: Weighted sharing using CRAB at the end-host.
- StatusQuo: No weighted sharing.
- WFQ: WFQ done before the bottleneck at the router.