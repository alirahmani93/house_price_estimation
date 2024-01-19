import requests
from logging import getLogger

from sqlalchemy import select

from .crud import CityQuery, CategoryQuery, PostTokenQuery, PostQuery
from .database import get_db
from .models import Post
from .schemas import PostCreateSchema


class DivarCrawler:
    crawler_name = 'Divar'
    url = 'https://api.divar.ir/v8/web-search/tehran/buy-residential'

    base_url = 'https://api.divar.ir/v8/web-search/tehran/buy-residential?{0}'
    post_url = "https://api.divar.ir/v8/posts-v2/web/{0}"

    def __init__(self, city_id, category_id, min_page: int = 0, max_page: int = 10, db=get_db(), *args, **kwargs):
        self.logger = getLogger(name=self.crawler_name)
        self.city_id = city_id
        self.category_id = category_id
        self._db = db
        self._max_page, self._min_page = max_page, min_page
        self._city_query = CityQuery(db=db)
        self._category_query = CategoryQuery(db=db)
        self._post_token_query = PostTokenQuery(db=db)
        self._post_query = PostQuery(db=db)
        self._token = None
        self.post_count = 0
        self.post_detail_count = 0
        self.post_data: dict = dict()
        self.normal_fields = {
            'webengage': (
                'brand_model', 'business_ref', 'business_type', 'cat_1', 'cat_2', 'cat_3', 'category', 'city', 'credit',
                'district', 'gender', 'image_count', 'originality', 'price', 'rent', 'status', 'token',),
            'share': ('image_url', 'title', 'web_url'),
            'seo': ('unavailable_after', 'title', 'description'),
            'contact': ('chat_enabled',),
        }
        self.post_detail_section_list_data_fields = {
            'section_name': 'LIST_DATA',

        }
        self.columns_name = Post.columns_name()

    def validation(self):
        self._city_query.get(target_id=self.city_id)
        self._category_query.get(target_id=self.category_id)

    def _make_list_url(self, format_str: str) -> str:
        return self.base_url.format(format_str)

    def make_detail_url(self, format_str: str) -> str:
        return self.post_url.format(format_str)

    def iterate_page(self, page: int = 0):
        print(page)
        return self._make_list_url(f'page={page}')

    def _range_page(self):
        return range(self._min_page, self._max_page + 1)

    def _get_token_from_server_info(self, elm):
        return elm['action_log']['server_side_info']['info']['post_token']

    def _get_all_tokens(self):
        return self._post_token_query.get_all_active()

    def _is_new_token(self, token):
        return not self._post_token_query.exists(target_code=token)

    def crawl(self):
        # new_tokens = self.get_tokens()
        new_tokens = 0
        post_detail_count = self.get_tokens_detail()
        return {'post_count': self.post_count, 'new_tokens': new_tokens, 'post_detail_count': post_detail_count}

    def get_tokens(self):
        all_home = []
        for p in self._range_page():
            url = self.iterate_page(page=p)
            r = requests.get(url)
            data = r.json().get('web_widgets').get('post_list')
            for i in data:
                self.post_count += 1
                try:
                    post_token = None
                    if i['widget_type'] == 'POST_ROW':
                        post_token = self._get_token_from_server_info(i)
                        # post_token = i['data']['action']['payload']['token']
                    elif i['widget_type'] == 'SELECTOR_ROW':
                        widget_list = i['data']['action']['payload']['modal_page']['widget_list']
                        for elm in widget_list:
                            post_token = self._get_token_from_server_info(elm)
                    else:  # SECTION_DIVIDER_ROW
                        pass

                    if post_token is not None and self._is_new_token(token=post_token):
                        self._post_token_query.create(**{'code': post_token})
                        all_home.append(post_token)
                    else:
                        self.logger.warning(f'OLD TOKEN: {post_token}')

                except Exception as e:
                    self.logger.warning(str(e))
                    continue
        return len(all_home)

    def get_tokens_detail(self):
        all_active_token = self._post_token_query.get_all_active()
        for token in all_active_token:
            self._token = token
            url = self.make_detail_url(token.code)
            print(f'POST DETAIL URL: {url}')
            r = requests.get(url)
            if r.status_code != 200:
                self.logger.error(f'status_code:{r.status_code},token: {token}')
                break
            data = r.json()
            self._get_one_token_detail(data)
            self.post_detail_count += 1
            # break
        return self.post_detail_count

    def _get_one_token_detail(self, data: dict) -> dict:
        self.post_data = {}
        for key in self.normal_fields.keys():
            for item in self.normal_fields[key]:
                self.post_data[item] = self._get_item(data.get(key), item)
        for elm in data.get('sections'):
            self.route_section(section=elm)

        seo_web_info = data['seo'].get('web_info')
        self.post_data['district_persian'] = seo_web_info['district_persian']  # elm['district_persian']
        self.post_data['city_persian'] = seo_web_info['city_persian']
        self.post_data['category_slug_persian'] = seo_web_info['category_slug_persian']
        # post_data = {**post_data, **{z['title']: z['value'] for z in data['seo'].get('web_info')}}
        # print(self.post_data)
        self.clear()
        self.write_post()
        return self.post_data

    def write_post(self):
        # post = self._post_query.get(**{'token': self.post_data['token'], })
        # post = self._post_query.get_by_token(token=self.post_data['token']))
        # if post is None:
        # selected = self._db.execute("SELECT * FROM post WHERE post.token='QZOpBIcE' ")
        # self._post_query.create(post=self.post_data)
        # if selected is None:
        # stmt = select(Post).where(Post.token == self._token)
        # self._db.execute(stmt)
        self._db.execute(
            "INSERT INTO post {0} VALUES {1}".format(tuple(self.post_data.keys()), tuple(self.post_data.values())))
        self._db.execute("UPDATE post_token SET is_active=False WHERE code={0}".format(self._token))
        # Post.update().values(**self.post_data).where(token=self.post_data['token']).execute()
        # for k, v in self.post_data.items():
        #     if hasattr(post, k):
        #         post.k = v
        # post.title = self.post_data['title']
        # self._db.commit()
        # self._db.close()
        # self._post_query.update(tartget=post, **self.post_data)

    def clear(self):
        diff = list(set(self.post_data) - set(self.columns_name))
        for d in diff:
            fake_name_data = self.post_data.pop(d)
            real_name = list(self.columns_name.keys())[list(self.columns_name.values()).index(d)]
            self.post_data[real_name] = fake_name_data
        diff2 = list(set(self.columns_name) - set(self.post_data))
        if diff2:
            self.logger.critical(f'new column founded: {diff2}')

    def _get_item(self, data, item):
        result = data.get(item)
        return result

    def route_section(self, section):
        # data = exec(f'self._section_{section["section_name"]}(section)')
        # return data if data is not None else {}
        if section["section_name"] == "IMAGE":
            self._section_IMAGE(section)
        elif section["section_name"] == "BUSINESS_SECTION":
            self._section_BUSINESS_SECTION(section)
        elif section["section_name"] == "TITLE":
            self._section_TITLE(section)
        elif section["section_name"] == "NOTE":
            self._section_NOTE(section)
        elif section["section_name"] == "DESCRIPTION":
            self._section_DESCRIPTION(section)
        elif section["section_name"] == "STATIC":
            self._section_STATIC(section)
        elif section["section_name"] == "TAGS":
            self._section_TAGS(section)
        elif section["section_name"] == "BREADCRUMB":
            self._section_BREADCRUMB(section)
        elif section["section_name"] == "INSPECTION":
            self._section_INSPECTION(section)
        elif section["section_name"] == "SUGGESTION":
            self._section_SUGGESTION(section)
        elif section["section_name"] == "MAP":
            self._section_MAP(section)
        elif section["section_name"] == "LIST_DATA":
            self._section_LIST_DATA(section)

    def _section_IMAGE(self, section):
        pass

    def _section_BUSINESS_SECTION(self, section):
        pass

    def _section_TITLE(self, section):
        pass

    def _section_NOTE(self, section):
        pass

    def _section_DESCRIPTION(self, section):
        pass

    def _section_STATIC(self, section):
        pass

    def _section_TAGS(self, section):
        pass

    def _section_BREADCRUMB(self, section):
        pass

    def _section_INSPECTION(self, section):
        result = {}
        for widget in section['widgets'][0]['data']['widget_list']:
            if widget['widget_type'] == 'GROUP_INFO_ROW':
                for item in widget['data']['items']:
                    result[item['title']] = item['value']
        self.post_data = {**self.post_data, **result}

    def _section_SUGGESTION(self, section):
        suggestion_tokens: list = []
        widgets = section.get('widgets')
        if widgets is None:
            return None
        for data in section.get('widgets'):
            if data.get('action_log') is not None:
                suggestion_tokens.extend(data['action_log']['server_side_info']['info']['tokens'])
            else:
                suggestion_tokens.extend(data['items'][0]['action']['payload']['suggested_tokens'])

        self.post_data['suggestion_tokens'] = list(set(suggestion_tokens))

    def _section_MAP(self, section):
        data = section['widgets'][0]['data']
        location = data['location']
        self.post_data = {**self.post_data, **{
            'map_type': location.get('type'),
            'latitude': location.get('fuzzy_data', {}).get('point', {}).get('latitude'),
            'longitude': location.get('fuzzy_data', {}).get('point', {}).get('longitude'),
            'radius': location.get('fuzzy_data', {}).get('radius'),
            'map_image_url': data['image_url']
        }}

    def _section_LIST_DATA(self, section: dict):
        result, main_item, ef = {}, {}, {}
        widgets = section['widgets']

        for widget in widgets:
            if widget['widget_type'] in ["GROUP_INFO_ROW", 'UNEXPANDABLE_ROW']:
                if widget.get('data', {}).get('items') is not None:
                    for item in widget['data']['items']:
                        result[item['title']] = item['value']
                else:
                    result[widget['data']['title']] = widget['data']['value']
            elif widget['widget_type'] == 'GROUP_FEATURE_ROW':
                features = widget['data']
                main_item = {z['title']: z['value'] if z.get('value') else True for z in features['items']}
                extra_features = features.get('actions')
                ef = {}
                if extra_features is not None:
                    ef = {z['title']: z['value'] if z.get('value') else True for z in extra_features}

        # meter = widgets[0]['data']['items'][0]['value']
        # construction_year = widgets[0]['data']['items'][1]['value']
        # room = widgets[0]['data']['items'][2]['value']
        # total_price = widgets[1]['data']['value']
        # price_per_meter = widgets[2]['data']['value']
        #
        # widgets_3 = widgets[3]['data']
        # real_state_agency_title = widgets_3['value']
        # real_state_agency_business_ref = widgets_3.get('action', {}).get('payload', {}).get('business_ref',
        #                                                                                     None)
        # real_state_agency_slug = widgets_3.get('action', {}).get('payload', {}).get('slug', None)
        #
        # real_state_agent = widgets[4]['data']['value']
        # real_state_agent_slug = widgets[4]['data']['action']['payload']['slug']
        #
        # ceil = widgets[5]['data']['value']
        print('********' * 5)
        print(main_item)
        print(ef)
        self.post_data = {**self.post_data, **main_item, **ef, }
        # post_data = {**post_data, **{z['title']: z['value'] for z in data['seo'].get('web_info')}}
