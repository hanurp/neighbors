from django.test import TestCase
from random import shuffle
from .models import Person
from .views import search_person_by_geohash


class PersonSearchTest(TestCase):
    def setUp(self):
        self.limit = 10
        self.start_point = sp = (55.755531, 37.605260)
        inc_func = lambda n, start: start + round(n * 0.003, 5)
        items_set = [("t{}".format(i), min(inc_func(i, sp[0]), 89), min(inc_func(i, sp[1]), 189)) for i in range(10000)]
        self.check_set = items_set[:self.limit]
        shuffle(items_set)
        for i in items_set:
            Person.objects.create(name=i[0], lat=i[1], lon=i[2])

    def test_search_person_by_geohash(self):
        result_set = search_person_by_geohash(self.start_point, Person.objects.all(), self.limit)
        self.assertEqual({i.name for i in result_set} ^ {i[0] for i in self.check_set}, set())