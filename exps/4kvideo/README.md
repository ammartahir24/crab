This experiment shares a 30Mbps link between Youtube videos and bulk flows in ratio of 5:1. 

- `video_exp.py`: (runs at end-device) Plays 7 different Youtube videos and runs 2 bulk flows in background. Video quality is recorded with Youtube Developer API, network traffic is also recorded.

For each setting, there are two folders: `end-device` and `router`. `config.py` files needs to be placed in `src` directory before running `src/crab.py` for CRAB experiment. Similarly all shell files need to be executed appropirately at end-device or router before running `python3 video_exp.py` on end-device.

Experiments:

- CRAB: Weighted sharing in ratio of 5:1 between video and bulk flows using CRAB.
- HTB: Weighted sharing in ratio of 5:1 between video and bulk flows using Linux tc's HTB scheduler with bandwidth borrowing enabled which emulates instantaneous reallocation of unused bandwidth.
- PriorityQueue: An artificial bottleneck at 25 Mbps is created at end-point and video is prioritized over bulk flows.
- StatusQuo: No weighted sharing.
- Throttle: Throttles bulk flows to 5 Mbps to leave link empty for video flow.
- WFQ: WFQ done before the bottleneck at the router.