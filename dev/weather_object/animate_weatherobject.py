import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

import xarray as xr
import numpy as np

import matplotlib.animation as animation
from IPython.display import HTML

def animate_weatherobject(ds, var_name, title, nframes=24):
    mapcrs  = ccrs.PlateCarree(central_longitude=120)
    datacrs = ccrs.PlateCarree()

    fig, ax = plt.subplots(
        figsize=(7, 3.5),
        dpi=150,
        facecolor="w",
        subplot_kw={"projection": mapcrs},
    )
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), edgecolor="k", lw=0.6)
    ax.set_extent([-180, 180, -90, 90], crs=datacrs)

    gl = ax.gridlines(
        crs=datacrs,
        draw_labels=True,
        linewidth=0.4,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )

    # t0
    da0 = ds[var_name].isel(time=0)

    ma = da0.plot(
        ax=ax,
        transform=datacrs,
        vmin=0,
        vmax=1,
        add_colorbar=False,
    )

    figtitle = ax.set_title(f"{title} | {str(da0.time.values)[0:13]}")

    def update(i):
        for coll in list(ax.collections):
            coll.remove()
        da_i = ds[var_name].isel(time=i)
        ma = da_i.plot(
            ax=ax,
            transform=datacrs,
            vmin=0,
            vmax=1,
            add_colorbar=False,
        )
        figtitle.set_text(f"{str(da_i.time.values)[0:13]}")
        ax.add_feature(cfeature.COASTLINE.with_scale("50m"), edgecolor="k", lw=0.6)
        ax.set_extent([-180, 180, -90, 90], crs=datacrs)
        return ma, figtitle

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=nframes,
        interval=300,
    )
    plt.close(fig)

    # show animation on jupyter lab
    HTML(ani.to_jshtml())

    return ani