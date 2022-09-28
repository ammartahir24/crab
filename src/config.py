
'''
Interface to set CRAB flow groups and their weights.
Each flow group can have multiple flows defined in terms of source IP address (ip>>), application (app>>), webpage (gc>>).
'''

configurations = {
	"browser_active_window_prioritization": False,
	"bw_estimate": 30.0,
	"flow_groups": {
		"video_stream": {
			"apps": ["app>>youtube", "app>>netflix", "app>>zoom"],
			"weight": 7	
		},
		"web_browsing": {
			"apps": ["gc>>bbc.com", "gc>>cnn.com", "gc>>yahoo.com", "gc>>new.yahoo.com", "gc>>google.com", "gc>>facebook.com", "gc>>github.com", "gc>>netflix.com", "gc>>youtube.com", "gc>>0.0.0.0"],
			"weight": 5
		},
		"download1": {
			"apps": ["ip>>104.52.23.121"],
			"weight": 2
		},
		"default": {
			"apps": [],
			"weight": 1
		}
	}
}