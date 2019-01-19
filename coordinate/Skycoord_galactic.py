import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
from pylab import plot


def dot(ra, dec, color='k'):
	plt.gca()
	c = SkyCoord(ra, dec, frame='icrs').galactic
	plt.plot(c.l.wrap_at(180 * u.deg).radian, c.b.radian, linestyle='none', marker='.', markersize=1, color=color)


def area(ra, dec, ra_error, dec_error, color='skyblue', name=None):
	plt.gca()
	theta = np.arange(0, 2*np.pi, np.pi/50)
	c = SkyCoord(ra, dec, frame='icrs')
	c_error = SkyCoord(ra_error, dec_error, frame='icrs')
	x0 = c.ra.wrap_at(180*u.deg).degree
	y0 = c.dec.degree
	radio = np.linspace(0, 1, 100)
	for r in radio:
		a = r * c_error.ra.degree
		b = r * c_error.dec.degree
		x = x0 + a * np.cos(theta)
		y = y0 + b * np.sin(theta)
		g = SkyCoord(x, y, frame='icrs', unit='deg').galactic
		plt.plot(g.l.wrap_at(180 * u.deg).radian, g.b.radian, linestyle='none', marker='.', markersize=0.01, color=color, alpha=0.5)
	if name is not None:
		g0 = SkyCoord(x0, y0, frame='icrs', unit='deg').galactic
		plt.text(g0.l.wrap_at(180 * u.deg).radian, g0.b.radian, name, size=2)


def circle(ra, dec, ra_error, dec_error, color='r', name=None):
	plt.gca()
	theta = np.arange(0, 2*np.pi, np.pi/100)
	c = SkyCoord(ra, dec, frame='icrs')
	c_error = SkyCoord(ra_error, dec_error, frame='icrs')
	x0 = c.ra.wrap_at(180*u.deg).degree
	y0 = c.dec.degree
	a = c_error.ra.degree
	b = c_error.dec.degree
	x = x0 + a * np.cos(theta)
	y = y0 + b * np.sin(theta)
	g = SkyCoord(x, y, frame='icrs', unit='deg').galactic
	# plt.plot(g.l.wrap_at(180 * u.deg).radian, g.b.radian, marker='*', markersize=0.01, color=color)
	plot(g.l.wrap_at(180 * u.deg).radian, g.b.radian, color=color, linewidth=0.3, linestyle='-')
	if name is not None:
		g0 = SkyCoord(x0, y0, frame='icrs', unit='deg').galactic
		plt.text(g0.l.wrap_at(180 * u.deg).radian + 0.03, g0.b.radian + 0.03, name, size=4)


if __name__ == '__main__':
	fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={'projection': 'aitoff'})
	ax.set_title("Galactic")
	ax.grid()
	plt.tick_params(labelsize=4)

	area('18h35.5m', '-34.1d', '0h0.2m', '0.1d')
	# dot('10h0m', '-5d')
	# dot('17h54m', '-21.5d')
	# dot('17h14m', '-21.5d')
	# dot('17h34m', '-23d')
	# dot('17h34m', '-20d')

	plt.show()
