This experiment shares a 30Mbps link between 4 flows in ratio of 4:3:2:1. As flows start and stop, or their demand varies, CRAB tries to estimate these demands and enforce weighted sharing.

- `bulk4.py`: (runs at end-device) Starts 4 flows at different times and also records traffic trace.
- `vary_flow_demands.sh`: (runs at wifi router) Varies the flow demands over time by throttling them at emulated sender.

For each setting, there are two folders: `end-device` and `router`. `config.py` files needs to be placed in `src` directory before running `src/crab.py` for CRAB experiment. Similarly all shell files need to be executed appropirately at end-device or router before running `python3 bulk4.py` on end-device and `vary_flow_demands.sh` on router simultaneously.

Experiments:

- CRAB: Weighted sharing using CRAB at the end-host.
- StatusQuo: No weighted sharing.
- WFQ: WFQ done before the bottleneck at the router.