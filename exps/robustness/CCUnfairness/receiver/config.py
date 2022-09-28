
configurations = {
	"browser_active_window_prioritization": False,
	"bw_estimate": 30.0,
	"flow_groups": {
		"f1": {
			"apps": ["ip>>192.168.1.239:3001"],
			"weight": 1
		},
		"f2": {
			"apps": ["ip>>192.168.1.239:3002"],
			"weight": 2
		},
		"default": {
			"apps": [],
			"weight": 3
		}
	}
}