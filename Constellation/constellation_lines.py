from asterisms import asterisms
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 数据清洗
stars = pd.read_csv('Constellation/hygdata_processed_mag65.csv', usecols=['hip', 'ra', 'dec', 'mag', 'color']).dropna(axis=0,how='any')
stars['hip'] = stars['hip'].apply(np.int64)
stars = stars.set_index('hip')

def hip(hip_numbers):
    return stars.loc[hip_numbers]

def Constellation(ax, name):
    for hip_numbers in asterisms[name]:
        hip_numbers = [int(hip_number) for hip_number in hip_numbers]
        dset = hip(hip_numbers)
        ax.plot(dset.ra, dset.dec, color='g', lw=0.5)
        ax.scatter(dset.ra, dset.dec, s=(6.5-dset.mag)*5, color=dset.color)


if __name__ == "__main__":
    # names = ['Scorpius', 'Lepus', 'SerpensA', 'SerpensB', 'Ophiuchus', 'CoronaAustralis', 'Scutum', 'Sagittarius', 'Aquila', 'Capricornus', 'Microscopium']
    names = ['Scorpius', 'Aquila']

    fig, ax = plt.subplots()
    
    for name in names:
        Constellation(ax, name)
    
    plt.show()