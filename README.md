CRAB allows end-users to shape downlink traffic from devices in end-user's domain (computers, home routers) even if the bottleneck does not naturally occur within end-user's domain. 

See our paper at: 

## Using CRAB

Install some basic libraries listed in requirements.txt:

`pip3 install -r requirements.txt`

Install the chrome extension in `chrome_extension` directory, following instructions [here](https://developer.chrome.com/docs/extensions/mv3/getstarted/)

Populate the `config.py` with flow groups. There are three types of flows defined in CRAB as of now:

- `ip>>`: Source IP address (Remote server's IP)
- `gc>>`: Web domain name (e.g. facebook.com). This is only supported for Google Chrome as of now.
- `app>>`: Application name (e.g. chrome)

Run: `sudo python3 onboot.py`
Run: `sudo python3 crab.py`

## Run Experiments

`exps/` directory includes all the files to setup and run different experiments with CRAB and some other baselines. For this you will need a router that can run OpenWRT. All the experiments in paper are with Linksys WRT3200ACM router running OpenWRT. For experiments in `exps/robustness`, another device running Linux is needed. Details for each individual experiments are in the corresponding subdirectory.

## Data and Plots

To reproduce plots from the paper, run respective figure's python file in `plots` directory. 