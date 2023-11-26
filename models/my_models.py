from logging import getLogger

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.svm import SVC


class DivarModel:
    cat_attributes = ['business_type', 'district', 'elevator', 'parking', 'depot', 'real_state_agent', 'if_near',
                      'inrange_pm2_dist_cat', 'new_encoded_pm2_dist_cat']
    ordinal_attributes = ['floor_0', 'rooms']
    num_attributes = ['age', 'meter']

    def __init__(self, df, cleaner_object, models_instances: list = None, metrics: list = None, n_jobs=None):
        self.logger = getLogger(name="Divar")
        self.raw_df = df
        self.df = None
        self.cleaner_object = cleaner_object
        self.models_instances = models_instances
        self.metrics = metrics
        self.n_jobs = n_jobs
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_price = None
        self.log = []
        self.pipeline = self._pipeline()
        self.linear_model_class = LinearRegression

    def transform(self, ):
        self.df = self.cleaner_object.transform()

    def fit(self):
        self.x_y_selection()
        self.train_test_split()

    def predict(self):
        # self._linear_regression()
        self._xgb_regression()
        # self._gradient()
        # self._gradiant_boosting()
        # self._stacking()

    def transform_fit_predict(self):
        self.transform()
        self.fit()
        self.predict()
        # self._get_metrics(y_pred, 'transform_fit_predict')
        return self.log

    def _get_metrics(self, y_predict, from_model):
        def rounding(number):
            return round(number, 3)

        self.log.append(
            {
                "from_model": from_model,
                'log': {
                    f'r2 square': rounding(r2_score(self.y_test, y_predict)),
                    f'mean squared error': rounding(mean_squared_error(self.y_test, y_predict, squared=False)),
                    f'mean absolute error': rounding(mean_absolute_error(self.y_test, y_predict)),
                    f'mean absolute percentage error': rounding(mean_absolute_percentage_error(self.y_test, y_predict)),
                }
            }
        )

    def _get_bias(self):
        pass

    def _get_variance(self):
        pass

    def x_y_selection(self):
        self.X = self.df.drop(['price', 'price_m2'], axis=1)
        self.y_price = self.df['price']
        self.y = self.df['price_m2']

    def train_test_split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y)

    def _pipeline(self):
        num_pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
        cat_pipeline = make_pipeline(
            SimpleImputer(strategy="most_frequent"),
            OneHotEncoder(handle_unknown="ignore"))

        return ColumnTransformer([
            ('cat', cat_pipeline, self.cat_attributes),
            ('num', num_pipeline, self.num_attributes),
            ('ord', num_pipeline, self.ordinal_attributes)],
            remainder='drop')

    def _linear_regression(self):
        regressor_pipeline = make_pipeline(self.pipeline, LinearRegression())
        regressor_pipeline.fit(self.X_train, self.y_train)
        y_predict = regressor_pipeline.predict(self.X_test)
        return self._get_metrics(y_predict, from_model='LinearRegression')

    def _xgb_regression(self):
        regressor_pipeline = make_pipeline(self.pipeline, xgb.XGBRegressor(objective="reg:squarederror"))
        regressor_pipeline.fit(self.X_train, self.y_train)
        y_predict = regressor_pipeline.predict(self.X_test)
        return self._get_metrics(y_predict, from_model='XGBRegressor')

    def _gradient(self):
        clf2 = RandomForestRegressor(n_estimators=50, random_state=42, )
        clf3 = xgb.XGBRegressor(objective="reg:squarederror")
        # clf4 = SVR()
        # clf5 = MLPRegressor()
        clf6 = KNeighborsRegressor()
        clf7 = GradientBoostingRegressor(max_depth=10, learning_rate=0.01, n_estimators=1000, n_iter_no_change=10,
                                         random_state=42, )

        voting_reg = VotingRegressor(estimators=[
            # ('rf', clf2),
            ('xgb', clf3),
            # ('svr', clf4),
            # ('mlp', clf5),
            ('knn', clf6),
            # ('gbrt', clf7)
        ],
            n_jobs=self.n_jobs)  # weights=None, verbose=False
        vote_reg = make_pipeline(self.pipeline, voting_reg)
        vote_reg.fit(self.X_train, self.y_train)
        y_predict = vote_reg.predict(self.X_test)
        self._get_metrics(y_predict, 'VotingRegressor')

    def _gradiant_boosting(self):
        gbrt = make_pipeline(self.pipeline,
                             GradientBoostingRegressor(
                                 max_depth=3, learning_rate=0.01, n_estimators=500,
                                 n_iter_no_change=10, random_state=42,
                             ))

        gbrt.fit(self.X_train, self.y_train)
        y_predict = gbrt.predict(self.X_test)

        self._get_metrics(y_predict, 'GradientBoostingRegressor')

    def _stacking(self):
        clf6 = KNeighborsClassifier()

        stacking = StackingClassifier(estimators=[
            ('knn', clf6),
        ],
            final_estimator=SVC(random_state=43),
            cv=3,
            n_jobs=self.n_jobs)
        model = Pipeline([('stack', stacking)])
        hyper = {"stack__knn__n_neighbors": [1, 3, 5, 7], 'stack__final_estimator__C': [1.0, 0.75, 0.5, 0.25],
                 'stack__final_estimator__kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']}

        clf = GridSearchCV(model, param_grid=hyper, cv=3, scoring='f1_micro')
        clf.fit(self.X_train, self.y_train)
        predict = clf.best_estimator_.predict(self.X_test)
        self._get_metrics(predict, 'Stacking')


if __name__ == '__main__':
    import pandas as pd
    from preprocess import cleaner

    raw_df = pd.read_csv('../data/Post-2023-11-21.csv')
    housing = cleaner.Cleaner(raw_df)
    model = DivarModel(df=raw_df, cleaner_object=housing, )
    model_prediction = model.transform_fit_predict()
    print(model_prediction)
r = [
    {
        'from_model': 'LinearRegression',
        'log': {
            'r2 square': 0.344,
            'mean squared error': 72502523.012,
            'mean absolute error': 21758329.293,
            'mean absolute percentage error': 2.4680
        }},

    {
        'from_model': 'XGBRegressor',
        'log': {
            'r2 square': 0.346,
            'mean squared error': 72397075.047,

            'mean absolute error': 21033478.848,

            'mean absolute percentage error': 2.806
        }},

    {
        'from_model': 'GradientBoostingRegressor Voting',
        'log': {
            'r2 square': 0.253,
            'mean squared error': 77354782.854,

            'mean absolute error': 29413807.04,
            'mean absolute percentage error': 2.461
        }},

    {
        'from_model': 'GradientBoostingRegressor',
        'log': {
            'r2 square': 0.243,
            'mean squared error': 77905437.786,
            'mean absolute error': 31538853.271,
            'mean absolute percentage error': 2.545
        }}
]
r2 = [{'from_model': 'LinearRegression',
       'log': {'r2 square': 0.073, 'mean squared error': 182583305.077, 'mean absolute error': 22931329.17,
               'mean absolute percentage error': 1.94041160175748e+20}},
      {'from_model': 'XGBRegressor',
       'log': {'r2 square': 0.079,
               'mean squared error': 181950567.616,
               'mean absolute error': 22201836.69,
               'mean absolute percentage error': 2.127134970722769e+20}},

      {'from_model': 'GradientBoostingRegressor Voting',
       'log': {'r2 square': 0.073, 'mean squared error': 182581139.301, 'mean absolute error': 26788189.398,
               'mean absolute percentage error': 2.2041540260331284e+20}},
      {'from_model': 'GradientBoostingRegressor',
       'log': {'r2 square': 0.082,
               'mean squared error': 181696807.987,
               'mean absolute error': 30655051.535,
               'mean absolute percentage error': 2.0913086237584068e+20}}]

r3 = [{'from_model': 'LinearRegression',
       'log': {'r2 square': 0.372, 'mean squared error': 68050303.35, 'mean absolute error': 21727150.09,
               'mean absolute percentage error': 1.4192467219656088e+20}},
      {'from_model': 'XGBRegressor',
       'log': {'r2 square': 0.349,
               'mean squared error': 69233444.766,
               'mean absolute error': 20988998.155,
               'mean absolute percentage error': 2.1153037313168602e+20}},

      {'from_model': 'GradientBoostingRegressor Voting',
       'log': {'r2 square': 0.313, 'mean squared error': 71125382.759, 'mean absolute error': 22523115.476,
               'mean absolute percentage error': 1.50726140241712e+20}},
      {'from_model': 'GradientBoostingRegressor',
       'log': {'r2 square': 0.337,
               'mean squared error': 69875990.828,
               'mean absolute error': 29645653.454,
               'mean absolute percentage error': 1.513843249980077e+20}}]
