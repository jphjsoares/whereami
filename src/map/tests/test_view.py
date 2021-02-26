from django.test import TestCase

class IndexViewTests(TestCase):
    def test_index_page(self):
        resp = self.client.get('/map/')
        self.assertEqual(resp.status_code, 200)


#TODO: 
"""
test if we can submit a null map
test if we can submit a less than 5 map
Test weird inputs
"""
class CreateCustomViewTests(TestCase):
    def test_create_custom_page(self):
        resp = self.client.get('/map/createcustom')
        self.assertEqual(resp.status_code, 200)

class CreateByRegionTests(TestCase):
    def test_create_by_region_page(self):
        resp = self.client.get('/map/createbyregion')
        self.assertEqual(resp.status_code, 200)

class CreateWorld(TestCase):
    def test_create_world_page(self):
        resp = self.client.get('/map/createworld')
        self.assertEqual(resp.status_code, 200)
    