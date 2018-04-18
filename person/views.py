import operator
import geohash
import logging
import time

from geopy.distance import geodesic

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, viewsets, status

from django.conf import settings

from .models import Person

logger = logging.getLogger(__name__)


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'lon', 'lat', 'geo_hash', 'url')


class PersonSerializerLight(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name', )


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


def get_distance(lat1, lon1, lat2, lon2):
    """Возвращает расстоняние между точками (метрах)"""
    return geodesic((lat1, lon1), (lat2, lon2)).m


def search_person_by_geohash(point, persons_set, limit):
    """
    Производит поиск ближайших пользователей по geohash.
    Данную функцию целосообразно использовать если базе много записей
    """
    start_hash_length = getattr(settings, "START_HASH_LENGTH_SEARCH", 8)
    point_hash = geohash.encode(*point)
    selected_persons = []
    more_need_items = limit
    last_hash_length = 0
    b = time.time()
    for hash_length in range(min(len(point_hash)-1, start_hash_length), -1, -1):
        last_hash_length = hash_length
        if hash_length > 0:
            new_set = persons_set.filter(geo_hash__startswith=point_hash[:hash_length])
        else:
            new_set = persons_set
        new_set = new_set.exclude(pk__in=(p.pk for p in selected_persons))

        if len(new_set) > more_need_items:
            # сортирует польз. из последнего набора по расстоянию, т.к. их больше чем нужно
            new_set_with_distance = ((p, get_distance(point[0], point[1], p.lat, p.lon)) for p in new_set)
            new_set_sorted_by_distance = sorted(new_set_with_distance, key=operator.itemgetter(1))
            new_set = [p[0] for i, p in enumerate(new_set_sorted_by_distance) if i < more_need_items]

        if new_set:
            selected_persons.extend(new_set)
            more_need_items -= len(new_set)
            if not more_need_items:
                break
    logger.debug("got {} items, last_hash_len={}, duration={}".format(len(selected_persons), last_hash_length,
                                                                      time.time()-b))
    return selected_persons


@api_view(['GET'])
def person_search_nearby(request):
    """
    Возвращет список ближайших пользователей от указаных координат
    """
    if request.method == 'GET':
        limit = int(request.GET.get("limit", getattr(settings, 'REST_FRAMEWORK', {}).get('PAGE_SIZE', 100)))
        try:
            point = (float(request.GET["lat"]), float(request.GET["lon"]))
        except (KeyError, ValueError):
            return Response({"msg": "не корректно указаны координаты"}, status.HTTP_400_BAD_REQUEST)  # todo переделать вывод ошибки в стандартном формате
        persons_set = Person.objects.all()
        persons = search_person_by_geohash(point, persons_set, limit)
        serializer = PersonSerializerLight(persons, many=True)
        return Response(serializer.data)
