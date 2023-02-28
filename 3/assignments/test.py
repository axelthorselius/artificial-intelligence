import numpy as np

stat_fr = np.array([[36961, 2503],
                      [43621, 2992],
                      [15694, 1042],
                      [36231, 2487],
                      [29945, 2014],
                      [40588, 2805],
                      [75255, 5062],
                      [37709, 2643],
                      [30899, 2126],
                      [25486, 1784],
                      [37497, 2641],
                      [40398, 2766],
                      [74105, 5047],
                      [76725, 5312],
                      [18317, 1215]])

stat_en = np.array([[35680, 2217],
                      [42514, 2761],
                      [15162, 990],
                      [35298, 2274],
                      [29800, 1865],
                      [40255, 2606],
                      [74532, 4805],
                      [37464, 2396],
                      [31030, 1993],
                      [24843, 1627],
                      [36172, 2375],
                      [39552, 2560],
                      [72545, 4597],
                      [75352, 4871],
                      [18031, 1119]])


def normalize(observations):
    maxima = [max([obs[i] for obs in observations]) for i in range(len(observations[0]))]
    return ([[obs[i] / maxima[i]
              for i in range(len(observations[0]))] for obs in observations],
            maxima)

X_fr = np.ones((stat_fr.shape[0],2), dtype=float)
X_fr[:, 1] = stat_fr[:,1]
y_fr = stat_fr[:, 0]

X_fr = np.array([[1, x] for x in stat_fr[:,0]])
y_fr = np.array([stat_fr[:,1]]).T


X_en = np.ones((stat_en.shape[0],2), dtype=float)
X_en[:, 1] = stat_en[:,1]
y_en = stat_en[:, 0]

X_en = np.array([[1, x] for x in stat_en[:,0]])
y_en = np.array([stat_en[:,1]]).T

print(X_fr)
print(y_fr)
print(X_fr.shape)

X_fr, _ = normalize(X_fr)

print(X_fr)
print(X_fr.shape)