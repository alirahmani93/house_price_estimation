import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import utils


# import sys
# sys.path.append('..')

class BaseCleaner:
    pass


class Cleaner:
    def __init__(self, df: pd.DataFrame = None, ):
        self.raw_df = df
        self.df = self.raw_df.copy()
        self.cols_number = ['meter', 'rooms', 'total_price', 'price_per_meter', 'year', 'rent', ]
        self.cols_bool = ['balcony', 'elevator', 'depot', 'parking']
        self.cols_need_to_fill = ['real_state_agency', 'floor']
        self.cols_drop = [
            'city_rel', 'top_description_text', 'middle_description_text', 'bottom_description_text', 'red_text',
            'checkable', 'label', 'label_color', 'is_checked', 'has_chat', 'last_post_date', 'first_post_date',
            'brand_model',
            'gender', 'originality', 'status', 'not_elevator', 'not_parking', 'not_depot', 'map_type', 'latitude',
            'longitude',
            'radius', 'map_image_url', 'not_balcony', 'check_cost_limit', 'check_cost', 'pricing_cost',
            'land_meter', 'house_status',
        ]
        self.route = {'func_number': self.cols_number, 'func_bool': self.cols_bool, 'func_cols_drop': self.cols_drop,
                      'func_need_cat_fill': self.cols_need_to_fill, 'func_floor': ['floor']}
        self.pipe_order = [
            'func_cols_drop',
            'func_bool',
            'func_number',
            'func_need_cat_fill',
            'func_floor'
        ]

    def fit(self, X):
        pass

    def transform(self):
        for pipe in self.pipe_order:
            exec(f'self.{pipe}()')
        return self.df

    def func_number(self):
        func_name = 'func_number'
        for field in self.route[func_name]:
            self.df[field] = self.df[field].map(self.convart_persion_number)

    def func_bool(self):
        func_name = 'func_bool'

    def func_need_cat_fill(self):
        func_name = 'func_need_cat_fill'
        for field in self.route[func_name]:
            if field == 'real_state_agency':
                self.df[field] = self.df[field].fillna('personal')
            elif field == 'floor':
                self.df[field] = self.df[field].fillna(0)

    def func_cols_drop(self):
        func_name = 'func_cols_drop'
        self.df = self.df.drop(self.route[func_name], axis=1)

    def func_floor(self):
        field_name = 'floor'
        self.df[field_name] = self.df.floor.str.replace('زیر همکف', '−۱').str.replace('زیرهمکف', '−۱'). \
            str.replace('همکف', '۰').str.replace('از بیشتر از', ' '). \
            str.replace('+۳۰', '۳۰').str.replace('از', '_').str.replace(' ', '_').str.replace('___', '_')

        not_nan_values = self.df.loc[self.df[field_name].isna() == False, field_name]
        self.df.loc[self.df[field_name].isna() == False, field_name] = not_nan_values.map(
            utils.convert_fa_number_to_en)

        # self.df['home_floor'] = 30
        # self.df['all_floor'] = 30
        self.df[field_name] = self.df[field_name].map(self.floor_and_all)

    def floor_and_all(self, value):
        try:
            if np.isnan(value):
                return None
        except Exception:
            pass
        return value.split('_')[:2] if '_' in value else (value, None)

    def convart_persion_number(self, value):
        if not value:  # Return empty string if value is empty
            return value

        n = None
        if isinstance(value, str):
            n = utils.convert_fa_number_to_en(value)
        return n


# if __name__ == '__main__':
#     raw_df = pd.read_csv('../data/Post-2023-11-13.csv')  # ../data/Post-2023-11-13.csv')
#     df = Cleaner(raw_df).transform()
#     print(df.head())
