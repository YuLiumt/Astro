import matplotlib.pyplot as plt

def plot_1d(ax, data, var, plotname=None):
    ax.plot(data['time'], data[var])
    ax.set_xlabel('Time [M]')
    ax.grid(True)
    ax.set_title(var)
    if plotname == None:
        plt.show()
    else:
        plt.savefig(plotname, transparent=True)

