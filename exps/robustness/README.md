These experiments require connecting another Linux machine to the Wifi router over Ethernet. This machine runs iperf3 servers, we introduce arbitrary delays or use different congestion control algorithms at outgoing flows of this machine to test CRAB under different conditions.

- CCUnfairness: We evaluate how CRAB behaves when competing flows use different congestion control algorithms.
- RTTUnfairness: We evaluate how CRAB behaves when competing flows have different end-end RTTs.
- ManyFlows: How CRAB reacts to increasing number of flow groups.

You may need to install `iperf3` on both devices using:

- `sudo apt-get install iperf3`