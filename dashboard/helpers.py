# -*- coding: utf-8 -*-

import urllib2

def bus_helper(api, bus_id):
	base_url = 'http://ws.bus.go.kr/api/rest/'
	service_key = 'Xt8Az7GGhJW6kK3R0Li5ZDSPinelBbM1RJwz4z%2Fc0ixgZ%2FLj6Tg6Nahc48MjQkjm6LVDMWn4dsrYaeNNbPeQMQ%3D%3D'

	req_url = base_url + api + '?ServiceKey=' + service_key + '&busRouteId=' + bus_id + '&numOfRows=999&pageSize=999&pageNo=1&startPage=1'
	
	request = urllib2.Request(req_url)
	response = urllib2.urlopen(request)

	return response.read()