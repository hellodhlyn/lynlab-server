# -*- coding: utf-8 -*-

import xmltodict

from django.shortcuts import render
from django.template import RequestContext

from .models import BusDashboard
from .helpers import bus_helper

def dashboard(request):
	results = []
	context = {
		'results': results,
	}

	return render(request, 'dashboard.html', context, context_instance=RequestContext(request))

def bus(request):
	def format_time(time):
		time_string = ''
		if time >= 60:
			time_string += str(time/60) + '분 '
		time_string += '%02d' % (time%60) + '초'

		return time_string

	lines_context = []
	lines = BusDashboard.objects.all()
	
	for line in lines:
		response_raw = bus_helper('arrive/getArrInfoByRouteAll', line.bus_id)
		response = xmltodict.parse(response_raw)

		station_list = response['ServiceResult']['msgBody']['itemList']
		station_now = filter(lambda station: station['arsId'] == line.station_id, station_list)[0]
		station_idx = station_list.index(station_now)

		stations_context = []
		notification_context = None
		for i in range(7, -1, -1):
			station = station_list[station_idx - i]

			if not station_now['stationNm1'] == station['stNm'] and not station_now['stationNm2'] == station['stNm']:
				station_context = {
					'before': i,
					'name': station['stNm'],
				}
				stations_context.append(station_context)

			else:
				if station_now['stationNm2'] == station['stNm']:
					station_context = {
						'before': i,
						'name': station['stNm'],
						'active': True,
						'people': station['reride_Num2'],
						'left_time': format_time(int(station_now['exps2'])),
					}
					stations_context.append(station_context)

				elif station_now['stationNm1'] == station['stNm']:
					station_context = {
						'before': i,
						'name': station['stNm'],
						'active': True,
						'people': station['reride_Num1'],
						'left_time': format_time(int(station_now['exps1'])),
					}
					stations_context.append(station_context)

					# For notification
					if int(station_now['exps1']) < 600:
						notification_context = {
							'bus_id': station['vehId1'],
							'left_time': format_time(int(station_now['exps1'])),
							'people': station['reride_Num1'],
						}

			
		line_context = {
			'bus_number': line.bus_number,
			'station_name': line.station_name,
			'terminus': station_now['dir'],
			'stations': stations_context,
			'notification': notification_context,
		}

		lines_context.append(line_context)

	context = {
		'lines': lines_context,
	}

	return render(request, 'bus.html', context, context_instance=RequestContext(request))