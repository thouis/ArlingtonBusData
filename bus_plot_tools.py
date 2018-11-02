import numpy as np
from pylab import gca, yticks, xlim, ylim, xlabel, axhline, axvline, text, title
from matplotlib.collections import LineCollection


locs = dict(heights=(42.4250376, -71.1860425),
            center=(42.415539, -71.1535001),
            lake=(42.4057083, -71.142363),
            varnum=(42.4036682, -71.1396169),
            milton=(42.4041378, -71.1402649),
            rt16=(42.400908, -71.1360857),
            carhouse=(42.396706, -71.129125),
            porter=(42.3881714, -71.1196717),
            harvard=(42.373611, -71.118889))


locals().update(locs)  # store waypoints as local variables


def latlon_to_miles(lat, lon):
    # turn into miles north & east of Harvard
    # 69 is the number of miles in one degree of latitude.
    return (lat - harvard[0]) * 69, (lon - harvard[1]) * 69 * np.cos(harvard[0] * np.pi / 180)  # noqa


locs_miles = {k: latlon_to_miles(*v) for k, v in locs.items()}


def num_minutes(t):
    return 60 * t.hour + t.minute


def plot_marey(vehicles, color='gray', alpha=0.5, start="6:30", end="9:30", show_milton=False):
    line_segs = []
    # Loop over individual vehicles and plot them
    for veh, gr in vehicles.between_time(start, end).groupby('vehicle'):
        times = gr.index.time
        for idx in range(len(gr) - 1):
            weekday = gr.index.weekday[idx]
            if weekday >= 5:  # Monday == 0, Saturday = 5, Sunday = 6
                continue

            p1 = gr.dist_from_harvard.iloc[idx]
            p2 = gr.dist_from_harvard.iloc[idx + 1]
            t1 = times[idx]
            t2 = times[idx + 1]

            # drop any locations for the same bus spaced by more than 10 minutes
            if abs(num_minutes(t2) - num_minutes(t1)) > 10:
                continue

            # drop any locations where the bus went backwards
            if p1 - p2 < -0.1:  # values should be decreasing
                continue

            line_segs.append([[p1, num_minutes(t1)], [p2, num_minutes(t2)]])

    # Plot the lines
    line_segs = np.array(line_segs)
    lc = LineCollection(line_segs)
    lc.set_linewidth(1.5)
    lc.set_alpha(0.5)
    lc.set_color(color)
    gca().add_collection(lc)

    # Decorate the plot
    xlabel('approximate distance from Harvard Square')
    xlim(3, 1)

    yticks(np.arange(0, 25 * 60, 60), ["{:02d}:00".format(i) for i in np.arange(25)])
    tks = yticks()
    for minor_tick in np.arange(0, 25 * 60, 15):
        axhline(minor_tick, lw=0.5, c='b')
    tks[1]
    ylim(line_segs[:, :, 1].max() + 5, line_segs[:, :, 1].min() - 5)
    ymax, ymin = ylim()

    for n in locs.keys():
        if (n == 'milton') and (not show_milton):
            continue
        a, b = locs_miles[n]
        dist = np.sqrt(a**2 + b**2)
        if (1 < dist < 3):
            axvline(dist, c='b', lw=0.5)
            text(dist, ymin, n, va="bottom", ha="center", fontsize=30, rotation=90)

    title('Time vs. location for all weekday 77 buses.\n')
