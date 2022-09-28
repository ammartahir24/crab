
configurations = {
	"browser_active_window_prioritization": False,
	"bw_estimate": 60.0,
	"flow_groups": {
		"f1": {
			"apps": ["ip>>192.168.1.239:3001"],
			"weight": 1
		},
		"f2": {
			"apps": ["ip>>192.168.1.239:3002"],
			"weight": 2
		},
		"f3": {
			"apps": ["ip>>192.168.1.239:3003"],
			"weight": 3
		},
		"f4": {
			"apps": ["ip>>192.168.1.239:3004"],
			"weight": 1
		},
		"f5": {
			"apps": ["ip>>192.168.1.239:3005"],
			"weight": 2
		},
		"default": {
			"apps": [],
			"weight": 3
		}
	}
}