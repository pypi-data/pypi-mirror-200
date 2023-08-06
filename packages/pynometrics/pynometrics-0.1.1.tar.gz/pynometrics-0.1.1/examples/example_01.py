
import warnings
import pandas as pd
import numpy as np
import random
import statsmodels.api as sm
warnings.filterwarnings('ignore')

data = pd.DataFrame({'feature1':np.random.randn(12),
                     'feature2':np.random.randn(12), 
                     'target':[random.randint(0,1) for i in range(12)]
                    })

X = data[["feature1", ]]
X = sm.add_constant(X)

y=data['target']

model_logit = sm.Logit(y,X).fit()

import pynometrics as ec

results = ec.get_marginal_effects(model_logit)

model_logit_margins = results.get_margins()

print(model_logit_margins.summary())

results.plot_coeff_margins()
