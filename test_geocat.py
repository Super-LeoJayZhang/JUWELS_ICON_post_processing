import numpy as np
import xarray as xr
import geocat.comp

fi_np = np.random.rand(30, 80)  # random 30x80 array

# xi and yi do not have to be equally spaced, but they are
# in this example
xi = np.arange(80)
yi = np.arange(30)

# create target coordinate arrays, in this case use the same
# min/max values as xi and yi, but with different spacing
xo = np.linspace(xi.min(), xi.max(), 100)
yo = np.linspace(yi.min(), yi.max(), 50)

# create :class:`xarray.DataArray` and chunk it using the
# full shape of the original array.
# note that xi and yi are attached as coordinate arrays
fi = xr.DataArray(fi_np,
                  dims=['lat', 'lon'],
                  coords={'lat': yi, 'lon': xi}
                 ).chunk(fi_np.shape)

fo = geocat.comp.linint2(fi, xo, yo, 0)
print(fo.shape)
