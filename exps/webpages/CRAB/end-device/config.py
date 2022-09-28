
configurations = {
	"browser_active_window_prioritization": False,
	"bw_estimate": 10.0,
	"flow_groups": {
		"web_browsing": {
			"apps": ["gc>>bbc.com", "gc>>cnn.com", "gc>>yahoo.com", "gc>>new.yahoo.com", "gc>>google.com", "gc>>facebook.com", "gc>>github.com", "gc>>netflix.com", "gc>>youtube.com", "gc>>0.0.0.0"],
			"weight": 7
		},
		"default": {
			"apps": [],
			"weight": 3
		}
	}
}