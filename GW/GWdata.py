import json, urllib
import h5py
import urllib.request
import os
import numpy
import re
import readligo
import scipy.io.wavfile
from urllib.request import urlretrieve
import pandas as pd


def schedule(a,b,c):
	# 下载进度条
	per = 100.0 * a * b / c
	if per > 100 :
		per = 100
	done = int(per / 5.0)
	# print('进度：%.1f%%' % per, end='\r')
	print("进度：%.1f%% | [%s%s]" % (per, '█' * done, ' ' * (20 - done)), end='\r')


def work_path(directory='/Volumes/gw/'):
	# 检查数据的下载的路径
	if not os.path.exists(directory):
		cmd = '{0} is not exit, choose another directory as work path'.format(directory)
		raise AssertionError(cmd)
	global DataPath, OutputPath
	DataPath = directory + 'data/'
	OutputPath = directory + 'output/'


def split_filename(filename):
	# 将文件名进行切分
	if re.match('.-.\d_LOSC_\d_.\d-\d+-\d+\.hdf5', filename) is None:
		raise AssertionError('filename is wrong: ' + filename)
	return re.split("-|_|\.", filename)


def data_set(gpstime):
	# 获取gpstime所在的dataset,返回S5,S6或O1
	if not isinstance(gpstime, int):
		raise AssertionError('gpstime is not a number: ' + gpstime)
	if 815155213 <= gpstime <= 875232014:
		return 'S5'
	elif 931035615 <= gpstime <= 971622015:
		return 'S6'
	elif 1126051217 <= gpstime <= 1137254417:
		return 'O1'
	else:
		raise AssertionError('The gpstime is out range of dataset: ', gpstime)


def detectors(dataset):
	# 输出dataset有哪些探测器
	if dataset not in ['S5', 'S6', 'O1']:
		raise AssertionError("dataset is wrong ('S5', 'S6', 'O1'): " + dataset)
	if dataset == 'S5':
		return ['H1', 'H2', 'L1']
	else:
		return ['H1', 'L1']


def get_url(filename):
	# 由文件名获取文件对应的下载网址
	# 十六进制数以0x开头 类似于四舍五入
	name = split_filename(filename)
	dataset = data_set(int(name[5]))
	fortnight = int(name[5])&0xFFF00000  # the directory by rounding down to (multiple of 4096*256)
	urlformat = 'https://www.gw-openscience.org/archive/data/{0}/{1}/{2}'
	url = urlformat.format(dataset, fortnight, filename)
	# print("Fetching data file from ", url)
	return url


def download_data(url):
	# 下载引力波数据，单个文件
	if re.match('https://www.gw-openscience.org/archive/data/.\d/\d+/.-.\d_LOSC_\d_.\d-\d+-\d+\.hdf5', url) is None:
		raise AssertionError("Url is wrong: " + url)

	filename = url.strip().split('/')[-1]
	if os.path.exists(DataPath + filename):
		print(filename, ' is exist in ', DataPath)
	else:
		print('Fetching ', filename)
		urlretrieve(url, DataPath + filename, schedule)
		print('File is downloaded in: ', DataPath)


class Event:
	def __init__(self, gpstime, timelineID):
		# 给一个gpstime和周围2 ** level 秒和timeLineID获取数据文件
		self.gpstime = gpstime
		self.dataset = data_set(self.gpstime)
		self.detectors = detectors(self.dataset)      
		self.timelineID = timelineID
		self.filename = {}

		for detector in self.detectors:
			# 十六进制数以0x开头 类似于四舍五入
			hour = self.gpstime&0xFFFFF000  # the filename rounding down to (a multiple of 4096) 
			self.filename[detector] = '{0}-{1}_LOSC_4_V1-{2}-4096.hdf5'.format(detector[0], detector, hour)


	def duty(self, level):
		# statistics available about the proportion of time (duty cycle)
		self.duty = {}
		# 2 ** level seconds surrounding the given time
		# we will want to find out which detetctors were operating when, or more specifically, when are they operating with good data quality. Is There Good Data?
		for detector in self.detectors:
			urlformat = 'https://www.gw-osc.org/timelinejson/{0}/{1}_{2}/{3}/{4}/{5}/'
			url = urlformat.format(self.dataset, detector, self.timelineID, self.gpstime, 0, level)
			r = urllib.request.urlopen(url).read()
			timelines = json.loads(r)
			self.duty[detector] = timelines[0][0][1]
			print("%s %s duty cycle over %d seconds in %s dataset: %3.2f" % (detector, self.timelineID, 2 ** float(level), self.dataset, self.duty[detector]))


	def download(self, detectors=None):
		if detectors is None:
			detectors = self.detectors
		else:
			self.detectors = [detectors]

		for detector in detectors:
			url = get_url(self.filename[detector])
			download_data(url)


	def Inf(self):
		# Another way to look at data quality is through the GWOSC data catalog. For each of the 4096-second data files, there are statistics available about the proportion of time (duty cycle) that the various data quality flags are on.
		for detector in self.detectors:
			urlformat = 'https://www.gw-osc.org/archive/links/{0}/{1}/{2}/{3}/json/'
			url = urlformat.format(self.dataset, detector, self.gpstime, self.gpstime)
			# print("Tile catalog URL is ", url)
			r = urllib.request.urlopen(url).read()
			tiles = json.loads(r)
			print("Detector %s at dataset %s \nGPStime: %d" % (detector, self.dataset, self.gpstime))
			print('--------------')
			try:
				Inf = tiles['strain'][0]
				for key, value in Inf.items():
					print(key + ': ' + str(value))
				print('===============================================')
			except:
				print("Information is Empty!")


class Interval:
	def __init__(self, GPSstart, GPSend):
		self.GPSstart = GPSstart
		self.GPSend = GPSend
		self.dataset = data_set(self.GPSstart)
		self.detectors = detectors(self.dataset)

		self.urllist()


	def Inf(self):
		for detector in self.detectors:
			urlformat = 'https://www.gw-osc.org/archive/links/{0}/{1}/{2}/{3}/json/'
			url = urlformat.format(self.dataset, detector, self.GPSstart, self.GPSend)
			# print("Tile catalog URL is ", url)
			r = urllib.request.urlopen(url).read()
			tiles = json.loads(r)
			print("Detector %s at dataset %s \nGPStime: from %d to %d" % (detector, self.dataset, self.GPSstart, self.GPSend))
			print('--------------')
			try:
				pd.set_option('display.max_columns',50)
				pd.set_option('display.width',1000)
				table = pd.DataFrame(tiles['strain'])
				col = ['GPSstart', 'UTCstart', 'min_strain', 'max_strain', 'mean_strain', 'stdev_strain', 'BLRMS200', 'BLRMS1000', 'BNS', 'duty_cycle']
				print(table.ix[::2, col])
				print('===============================================')
			except:
				print("Information is Empty!")

	def urllist(self):
		self.urlList = {}
		for detector in self.detectors:
			urlformat = 'https://losc.ligo.org/archive/links/{0}/{1}/{2}/{3}/json/'
			url = urlformat.format(self.dataset, detector, self.GPSstart, self.GPSend)

			r = urllib.request.urlopen(url).read()    # get the list of files
			tiles = json.loads(r)             # parse the json
			
			list = []
			for file in tiles['strain']:
			    if file['format'] == 'hdf5':
			        list.append(file['url'])
			self.urlList[detector] = list

	def download(self, detectors=None):
		if detectors is None:
			detectors = self.detectors
		else:
			self.detectors = [detectors]

		for detector in self.detectors:
			for url in self.urlList[detector]:
				download_data(url)


if __name__ == '__main__':
	work_path()
	# event = Event(815976703, 'CBCLOW_CAT2')
	# event.download()
	# interval = Interval(825155213, 825182014)
	# interval.download()
	# interval.Fold()