import ipdb
import pandas as pd

from sklearn.metrics import r2_score # remove if not needed
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def random_forest(pd):
    test_percentage = 0.2
    y = pd['score']
    x = pd.drop(columns=['score'])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_percentage, random_state=0)
    model = RandomForestRegressor(max_depth=20, random_state=413)
    print("model.fit...")

    model.fit(x_train, y_train.values.ravel())
    y_pred = model.predict(x_test)
    print("[ii] ENTRENADO! el r2_score={}".format(r2_score(y_test, y_pred)))

    ipdb.set_trace()
