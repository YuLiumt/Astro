"""
在赤道坐标系上喵一个点，画一个圆或者一个区域。
在给误差的时候一定要包括 ‘0h’ 否则会识别为 ‘0d’
记得加上这三行：
fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={'projection': 'aitoff'})
ax.set_title("ICRS")
ax.set_xticklabels(['14h', '16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h'])
ax.grid()
"""

from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np


def dot(ra, dec, color='k', markersize=2):
	plt.gca()
	c = SkyCoord(ra, dec, frame='icrs')
	plt.plot(c.ra.wrap_at(180*u.deg).radian, c.dec.radian, linestyle='none', 
			 marker='.', markersize=markersize, color=color)


def area(ra, dec, ra_error, dec_error, color='blue'):
	ax = plt.gca()
	c = SkyCoord(ra, dec, frame='icrs')
	c_error = SkyCoord(ra_error, dec_error, frame='icrs')
	ell = Ellipse(xy=(c.ra.wrap_at(180*u.deg).radian, c.dec.radian), width=c_error.ra.radian * 2, height=c_error.dec.radian * 2, angle=0.0, facecolor=color, alpha=0.3)
	ax.add_patch(ell)


def circle(ra, dec, ra_error, dec_error, color='r'):
	theta = np.arange(0, 2*np.pi, np.pi/50)
	c = SkyCoord(ra, dec, frame='icrs')
	c_error = SkyCoord(ra_error, dec_error, frame='icrs')
	x0 = c.ra.wrap_at(180*u.deg).radian
	y0 = c.dec.radian
	a = c_error.ra.radian
	b = c_error.dec.radian
	x = x0 + a * np.cos(theta)
	y = y0 + b * np.sin(theta)
	plt.plot(x, y, linestyle='none', 
			 marker='.', markersize=0.05, color=color)


if __name__ == '__main__':
#	fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={'projection': 'aitoff'})
#	ax.set_title("ICRS")
#	ax.set_xticklabels(['14h', '16h', '18h', '20h', '22h', '0h', '2h', '4h', '6h', '8h', '10h'])
#	ax.grid()
	
#	area('17h34m', '-21.5d', '0h20m', '1.5d')
#	circle('17h34m', '-21.5d', '0h20m', '1.5d')
	Galactic_area('17h34m', '-21.5d', '0h20m', '1.5d')
	# dot('17h34m', '-21.5d')
	# dot('17h54m', '-21.5d')
	# dot('17h14m', '-21.5d')
	# dot('17h34m', '-23d')
	# dot('17h34m', '-20d')
	plt.show()