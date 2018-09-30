from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.coordinates import SkyCoord
from astropy import units as u


def dot(ra, dec, color='k'):
	plt.gca()
	c = SkyCoord(ra, dec, frame='icrs').galactic
	longitude = c.l.wrap_at(180 * u.deg).radian
	dimensionality = c.b.radian
	plt.plot(longitude, dimensionality, linestyle='none', marker=
		'.', markersize=1, color=color)


def circle(ra, dec, ra_error, dec_error):
	plt.gca()
	c = SkyCoord(ra, dec, frame='icrs').galactic
	longitude = c.l.wrap_at(180 * u.deg).radian
	dimensionality = c.b.radian	
	c_error = SkyCoord(ra_error, dec_error, frame='icrs')
	print(c_error.to_string('decimal'))
	longitude_error = c_error.ra.radian
	dimensionality_error = c_error.dec.radian
	print(longitude_error, dimensionality_error)
	ell = Ellipse(xy=(longitude, dimensionality), width=longitude_error * 2, height=dimensionality_error * 2, angle=0.0, facecolor='blue', alpha=0.3)
	ax.add_patch(ell)


if __name__ == '__main__':
	fig, ax = plt.subplots(figsize=(8, 5), subplot_kw={'projection': 'aitoff'})
	ax.set_title("Galactic")
	ax.grid()
	
	circle('17h34m', '-21.5d', '0h20m', '1.5d')
	dot('17h34m', '-21.5d')
	dot('17h54m', '-21.5d')
	dot('17h14m', '-21.5d')
	dot('17h34m', '-23d')
	dot('17h34m', '-20d')
	dot('17h54m', '-23d')
	dot('17h54m', '-20d')
	dot('17h14m', '-23d')
	dot('17h14m', '-20d')
	plt.show()
