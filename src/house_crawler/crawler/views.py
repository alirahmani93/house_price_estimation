from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from modules.divar import DivarCrawler


# Create your views here.
def index(request, *args, **kwargs):
    images_link = DivarCrawler(city_id=1, category_id=1).get_image_random()
    state = kwargs.get('state')
    if not state:
        return render(request, 'crawling.html', context={'images_link': images_link})
    return render(request, 'crawling.html',
                  context={'images_link': images_link, 'kwargs': kwargs})


def crawl(request, *args, **kwargs):
    query_params = request.GET
    city_id = query_params.get('city_id')
    category_id = query_params.get('category_id')
    min_page = query_params.get('min_page')
    max_page = query_params.get('max_page')
    ans = DivarCrawler(
        city_id=city_id,
        category_id=category_id,
        min_page=min_page,
        max_page=max_page,
    ).crawl()
    result = {
        'city_id': city_id,
        'category_id': category_id,
        'result': ans,
        'state': True
    }
    return index(request, *args, **result)


def crawl_new_tokens(request, *args, **kwargs):
    query_params = request.GET
    city_id = query_params.get('city_id')
    category_id = query_params.get('category_id')

    ans = DivarCrawler(
        city_id=city_id,
        category_id=category_id,
    ).crawl_new_tokens()
    result = {
        'city_id': city_id,
        'category_id': category_id,
        'result': ans,
        'state': True
    }
    return index(request, *args, **result)


def crawl_related_tokens(request, *args, **kwargs):
    query_params = request.GET
    city_id = query_params.get('city_id')
    category_id = query_params.get('category_id')
    ans = DivarCrawler(
        city_id=city_id,
        category_id=category_id,
    ).craw_related_tokens()

    result = {
        'city_id': city_id,
        'category_id': category_id,
        'result': ans,
        'state': True
    }
    return index(request, *args, **result)
