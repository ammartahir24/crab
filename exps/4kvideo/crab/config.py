
configurations = {
	"browser_active_window_prioritization": False,
	"bw_estimate": 30.0,
	"flow_groups": {
		"bulk": {
			"apps": ["ip>>185.125.190.37", "ip>>185.125.190.40", "ip>>91.189.88.248", "ip>>91.189.88.247", "ip>>91.189.91.123", "ip>>91.189.91.124"],
			"weight": 1
		},
		"default": {
			"apps": [],
			"weight": 5
		}
	}
}