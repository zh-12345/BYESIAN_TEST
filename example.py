import numpy as np
import pandas as pd
import pymc3 as pm
import sys

def main(argv = None):
    niter = 10000  # 10000
    tune = 5000  # 5000

    model = pm.Model()

    with model:
        tv = [1]
        rain = pm.Bernoulli('rain', 0.2, shape=1, testval=tv)
        sprinkler_p = pm.Deterministic('sprinkler_p', pm.math.switch(rain, 0.01, 0.40))
        sprinkler = pm.Bernoulli('sprinkler', sprinkler_p, shape=1, testval=tv)
        grass_wet_p = pm.Deterministic('grass_wet_p', pm.math.switch(rain, pm.math.switch(sprinkler, 0.99, 0.80),
                                                                     pm.math.switch(sprinkler, 0.90, 0.0)))
        grass_wet = pm.Bernoulli('grass_wet', grass_wet_p, observed=np.array([1]), shape=1)

        trace = pm.sample(20000, step=[pm.BinaryGibbsMetropolis([rain, sprinkler])], tune=tune, random_seed=124)

    # pm.traceplot(trace)

    dictionary = {
        'Rain': [1 if ii[0] else 0 for ii in trace['rain'].tolist()],
        'Sprinkler': [1 if ii[0] else 0 for ii in trace['sprinkler'].tolist()],
        'Sprinkler Probability': [ii[0] for ii in trace['sprinkler_p'].tolist()],
        'Grass Wet Probability': [ii[0] for ii in trace['grass_wet_p'].tolist()],
    }
    df = pd.DataFrame(dictionary)

    p_rain = df[(df['Rain'] == 1)].shape[0] / df.shape[0]
    print(p_rain)

    p_sprinkler = df[(df['Sprinkler'] == 1)].shape[0] / df.shape[0]
    print(p_sprinkler)

if __name__ == '__main__':
     sys.exit(main())