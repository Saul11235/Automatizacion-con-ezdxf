import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# generar puntos de ejemplo
rng = np.random.default_rng(42)
x = rng.uniform(0, 100, 40)
y = rng.uniform(0, 100, 40)
z = 50 * np.exp(-((x-50)**2 + (y-50)**2)/800)

# grid
xi = np.linspace(x.min(), x.max(), 100)
yi = np.linspace(y.min(), y.max(), 100)
XI, YI = np.meshgrid(xi, yi)

# interpolación
ZI = griddata((x, y), z, (XI, YI), method='cubic')

# rellenar NaN
mask = np.isnan(ZI)
ZI[mask] = griddata((x, y), z, (XI, YI), method='nearest')[mask]

# plot
plt.contour(XI, YI, ZI, 10)
plt.scatter(x, y)
plt.show()

print("ok")
