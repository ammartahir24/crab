// let color = "#3aa757";


// chrome.runtime.onInstalled.addListener(() => {
// 	chrome.storage.sync.set({ color });
// 	console.log("CRAB: Default Color")
// });

// chrome.webRequest.onBeforeRequest.addListener(
// 	function(details){
// 		console.log("CRAB", details.url, details.initiator, details.ip, details.tabId)
// 	},
// 	{urls: ["<all_urls>"]}
// );

var send = function(m){
	var  k = new XMLHttpRequest();
	k.open("POST", "http://127.0.0.1:8000", 1);
	k.send(JSON.stringify(m));
	// $.ajax({
	// 	url: 'http:127.0.0.1:8000',
	// 	type: 'POST',
	// 	success: sucess,
	// 	data: JSON.stringify(m),
	// 	contentType: 'application/json',
	// 	error: error_handle 
	// });
}

var sucess = function(){
	console.log('Sent');
}

var error_handle = function(){
	console.log('Error sending');
}

// chrome.webRequest.onCompleted.addListener(
// 	function(details){
// 		if (details.url.indexOf("127.0.0.1") == -1){
// 			console.log("CRAB", details.url, details.initiator, details.ip, details.tabId, details.responseHeaders)
// 			console.log(details)
// 			console.log(details.responseHeaders)
// 			var request_size = -1
// 			for (var i=0; i<details.responseHeaders.length; i++){
// 				if (details.responseHeaders[i]["name"] == "content-length"){
// 					request_size = parseInt(details.responseHeaders[i]["value"])
// 					break;
// 				}
// 			}
// 			console.log(request_size)
// 			var m = {
// 				type: "new_request",
// 				url: details.url, 
// 				initiator: details.initiator,
// 				ip: details.ip,
// 				tab: details.tabId,
// 				size: request_size
// 			};
// 			console.log(m)
// 			chrome.tabs.executeScript(null, {file: "jquery.js"}, function(){
// 				send(m)
// 			})
// 		}
// 	},
// 	{urls: ["<all_urls>"]}, ["responseHeaders"]
// );

chrome.webRequest.onResponseStarted.addListener(
	function(details){
		if (details.url.indexOf("127.0.0.1") == -1){
			console.log("Response Started", details.url, details.initiator, details.ip, details.tabId, details.responseHeaders)
			console.log(details)
			console.log(details.responseHeaders)
			var request_size = -1
			for (var i=0; i<details.responseHeaders.length; i++){
				if (details.responseHeaders[i]["name"] == "content-length"){
					request_size = parseInt(details.responseHeaders[i]["value"])
					break;
				}
			}
			console.log(request_size)
			var m = {
				type: "new_request",
				url: details.url, 
				initiator: details.initiator,
				ip: details.ip,
				tab: details.tabId,
				size: request_size
			};
			console.log(m)
			chrome.tabs.executeScript(null, {file: "jquery.js"}, function(){
				send(m)
			})
		}
	},
	{urls: ["<all_urls>"]}, ["responseHeaders"]
);

chrome.tabs.onActivated.addListener(function(activeInfo){
	chrome.tabs.get(activeInfo.tabId, function(tab){
		var m = {
			type: "active_view_change",
			tab: activeInfo.tabId,
			url: tab.url
		};
		chrome.tabs.executeScript(null, {file: "jquery.js"}, function(){
			send(m)
		})
	})
})

chrome.tabs.onUpdated.addListener((tabId, change, tab) => {
	if (change.url){
		console.log("URL Changed")
		var m = {
			type: "url_change",
			tab: tabId,
			url: change.url
		}
		console.log(m)
		chrome.tabs.executeScript(null, {file: "jquery.js"}, function(){
			send(m)
		})
	}
})

chrome.tabs.onRemoved.addListener((tabId, removed) => {
	var m = {
		type: "tab_closed",
		tab: tabId
	};
	chrome.tabs.executeScript(null, {file: "jquery.js"}, function(){
		send(m)
	})
})