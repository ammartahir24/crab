
configurations = {
	"browser_active_window_prioritization": False,
	"bw_estimate": 30.0,
	"flow_groups": {
		"bulk1": {
			"apps": ["ip>>18.7.29.125", "ip>>128.163.159.62"],
			"weight": 4
		},
		"bulk2": {
			"apps": ["ip>>185.125.190.37", "ip>>185.125.190.40", "ip>>91.189.88.248", "ip>>91.189.88.247", "ip>>91.189.91.123", "ip>>91.189.91.124"],
			"weight": 1
		},
		"bulk3": {
			"apps": ["ip>>130.215.31.13", "ip>>147.75.197.195", "ip>>213.174.147.249"],
			"weight": 3
		},
		"default": {
			"apps": [],
			"weight": 2
		}
	}
}