configurations = {
	"browser_active_window_prioritization": False,
	"flow_groups": {
		"vm2": {
			"apps": ["ip>>192.168.1.149"],
			"weight": 1
		},
		"default": {
			"apps": [],
			"weight": 1
		}
	}
}