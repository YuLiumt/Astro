#!/usr/bin/python

from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import urllib
import re
import pandas as pd
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from matplotlib.patches import Ellipse


def SNR_sample():
	# Looking like a human
	headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-us", "ACCEPT_ENCODING": "br, gzip, deflate"}

	website = 'http://www.mrao.cam.ac.uk/surveys/snrs/snrs.data.html'

	session = requests.Session()
	req = session.get(website, headers=headers)
	bsObj = BeautifulSoup(req.text, "lxml")

	snr_table = pd.DataFrame()
	i = 0
	
	snr_list = bsObj.find("div", {"class":"SUM"}).findAll("a")
	for snr in snr_list:
		snr_name = 'G' + snr.next.replace(' ','')
		coord = snr.next.next.split()
		ra = coord[0] + 'h' + coord[1] + 'm' + coord[2] + 's' 
		dec = coord[3] + 'd' + coord[4] + 'm'  
		
		snr_table.loc[i, 'name'] = snr_name
		snr_table.loc[i, 'ra'] = ra
		snr_table.loc[i, 'dec'] = dec
		i = i + 1
		
	return snr_table


def celestial_sphere(sample):
	plt.gca()
	
	for i in sample.index:
		Ra = sample.loc[i, 'ra'].strip()
		Dec = sample.loc[i, 'dec'].strip()
		c = SkyCoord(Ra, Dec, frame='icrs').galactic
		plt.plot(c.l.wrap_at(180 * u.deg).radian, c.b.radian, linestyle='none', marker='.', markersize=1, color='k')


if __name__ == '__main__':
	fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={'projection': 'aitoff'})
	ax.set_title("Galactic")
	ax.grid()
	
	sample = SNR_sample()
	celestial_sphere(sample)
	
	plt.show()