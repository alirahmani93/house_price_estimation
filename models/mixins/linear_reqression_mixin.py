from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from sklearn.pipeline import make_pipeline


class LinearRegression:

    def __init__(self, ):
        self.pipeline = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.lin_reg = None

    def fit(self):
        self.lin_reg = make_pipeline(self.pipeline, LinearRegression())
        self.lin_reg.fit(self.X_train, self.y_train)

    def predict(self):
        y_predict = self.lin_reg.predict(self.X_test)
        return y_predict, self._log_metrics(y_predict)

    def _log_metrics(self, y_predict):
        return {
            f'r2 square': r2_score(self.y_test, y_predict),
            f'mean squared error': mean_squared_error(self.y_test, y_predict, squared=False),
            f'mean absolute error': mean_absolute_error(self.y_test, y_predict),
            f'mean absolute percentage error': mean_absolute_percentage_error(self.y_test, y_predict),
        }
