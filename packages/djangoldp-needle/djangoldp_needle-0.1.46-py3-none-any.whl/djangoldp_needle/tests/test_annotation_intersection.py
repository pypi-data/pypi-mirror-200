import requests_mock
from django.db import transaction
from djangoldp_account.models import LDPUser
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase
import json
from pkg_resources import resource_string

from ..models import Annotation
from ..models import AnnotationTarget
from ..models import NeedleActivity
import time
import base64

@requests_mock.Mocker(real_http=True)
class TestAnnotationTargetIntersection(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def buildUser(self, username):
        user = LDPUser(email=username + '@test.startinblox.com', first_name='Test', last_name='Mactest',
                       username=username,
                       password='glass onion')
        user.save()
        return user

    def test_annotation_no_match_url_after(self, m):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/annotationintersections/after/" + base64.b64encode('invalid'.encode('UTF-8')).decode('UTF-8') + "/2000-01-01T00:00:00.000Z",
            content_type='application/ld+json'
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        response_value_content = response_value['ldp:contains'];
        response_length = len(response_value_content)
        self.assertEqual(response_length, 0)

    def test_annotation_no_match_url_before(self, m):
        user1 = self.buildUser('user1')
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/annotationintersections/before/" + base64.b64encode('invalid'.encode('UTF-8')).decode(
                'UTF-8') + "/2000-01-01T00:00:00.000Z",
            content_type='application/ld+json'
        )
        response_value = response.json()
        self.assertEqual(response.status_code, 200)
        response_value_content = response_value['ldp:contains'];
        response_length = len(response_value_content)
        self.assertEqual(response_length, 0)

    # 2 users with each 1  annotations with the same target

    def test_annotation_one_intersection_after(self, m):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target_a_id = 'target_a'
        target_a = self.buildAnnotationTarget(target_a_id)

        self.client.force_authenticate(user1)
        response = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response.json()
        target_url = response_value['target']['@id']
        annotation_date = response_value['annotation_date']

        self.client.force_authenticate(user2)
        response_user_2 = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_2.json()
        response_user_2_annotation_id = response_value['@id']
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/annotationintersections/after/" + base64.b64encode(target_a_id.encode('UTF-8')).decode('UTF-8') + "/" + annotation_date,
            content_type='application/ld+json'
        )
        response_value = response.json()

        self.assertEqual(response.status_code, 200)
        response_value_content = response_value['ldp:contains'];
        response_length = len(response_value_content)
        self.assertEqual(response_length, 1)
        response_first_id = response_value['ldp:contains'][0]['@id']
        self.assertEqual(response_first_id, response_user_2_annotation_id)

    def test_annotation_one_intersection_before(self, m):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target_a_id = 'target_a'
        target_a = self.buildAnnotationTarget(target_a_id)

        self.client.force_authenticate(user1)
        response_user_1 = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_1.json()
        response_user_1_annotation_id = response_value['@id']
        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response.json()
        target_url = response_value['target']['@id']
        annotation_date = response_value['annotation_date']
        response = self.client.get(
            "/annotationintersections/before/" + base64.b64encode(target_a_id.encode('UTF-8')).decode('UTF-8') + "/" + annotation_date,
            content_type='application/ld+json'
        )
        response_value = response.json()

        self.assertEqual(response.status_code, 200)
        response_length = len(response_value['ldp:contains'])
        self.assertEqual(response_length, 1)
        response_first_id = response_value['ldp:contains'][0]['@id']
        self.assertEqual(response_first_id, response_user_1_annotation_id)

    # 2 users with each 1  annotations with a different target
    def test_annotation_no_intersection_after(self, m):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target_a_id = 'target_a'
        target_a = self.buildAnnotationTarget(target_a_id)
        target_b_id = 'target_b'
        target_b = self.buildAnnotationTarget(target_b_id)

        self.client.force_authenticate(user1)
        response = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response.json()
        target_url = response_value['target']['@id']
        annotation_date = response_value['annotation_date']

        self.client.force_authenticate(user2)
        response_user_2 = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_b)
        )
        response_value = response_user_2.json()
        response_user_2_annotation_id = response_value['@id']
        self.client.force_authenticate(user1)

        response = self.client.get(
            "/annotationintersections/after/" + base64.b64encode(target_a_id.encode('UTF-8')).decode('UTF-8') + "/" + annotation_date,
            content_type='application/ld+json'
        )
        response_value = response.json()

        self.assertEqual(response.status_code, 200)
        response_value_content = response_value['ldp:contains'];
        response_length = len(response_value_content)
        self.assertEqual(response_length, 0)

    def test_annotation_no_intersection_before(self, m):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        target_a_id = 'target_a'
        target_a = self.buildAnnotationTarget(target_a_id)
        target_b_id = 'target_b'
        target_b = self.buildAnnotationTarget(target_b_id)

        self.client.force_authenticate(user1)
        response_user_1 = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_1.json()
        response_user_1_annotation_id = response_value['@id']
        self.client.force_authenticate(user2)
        response = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_b)
        )
        response_value = response.json()
        target_url = response_value['target']['@id']
        annotation_date = response_value['annotation_date']
        response = self.client.get(
            "/annotationintersections/before/" +  base64.b64encode(target_b_id.encode('UTF-8')).decode('UTF-8') + "/" + annotation_date,
            content_type='application/ld+json'
        )
        response_value = response.json()

        self.assertEqual(response.status_code, 200)
        response_length = len(response_value['ldp:contains'])
        self.assertEqual(response_length, 0)

    # 5 users with each 1  annotations with the same target - test the order.
    def test_annotation_intersection_after_order(self, m):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        user3 = self.buildUser('user3')
        user4 = self.buildUser('user4')
        user5 = self.buildUser('user5')
        target_a_id = 'target_a'
        target_a = self.buildAnnotationTarget(target_a_id)

        self.client.force_authenticate(user1)
        response_user_1 = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_1.json()
        response_user_1_annotation_id = response_value['@id']
        self.client.force_authenticate(user2)
        response_user_2 = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_2.json()
        response_user_2_annotation_id = response_value['@id']
        self.client.force_authenticate(user3)
        response_user_3 = self.client.post(
            "/users/user3/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_3.json()
        response_user_3_annotation_id = response_value['@id']
        annotation_date = response_value['annotation_date']
        self.client.force_authenticate(user4)
        response_user_4 = self.client.post(
            "/users/user4/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_4.json()
        response_user_4_annotation_id = response_value['@id']
        self.client.force_authenticate(user5)
        response_user_5 = self.client.post(
            "/users/user5/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_5.json()
        response_user_5_annotation_id = response_value['@id']
        self.client.force_authenticate(user3)

        response = self.client.get(
            "/annotationintersections/after/" + base64.b64encode(target_a_id.encode('UTF-8')).decode('UTF-8') + "/" + annotation_date,
            content_type='application/ld+json'
        )
        response_value = response.json()

        self.assertEqual(response.status_code, 200)
        response_value_content = response_value['ldp:contains'];
        response_length = len(response_value_content)
        self.assertEqual(response_length, 2)
        response_first_id = response_value['ldp:contains'][0]['@id']
        self.assertEqual(response_first_id, response_user_4_annotation_id)
        response_second_id = response_value['ldp:contains'][1]['@id']
        self.assertEqual(response_second_id, response_user_5_annotation_id)

    def test_annotation_intersection_before_order(self, m):
        user1 = self.buildUser('user1')
        user2 = self.buildUser('user2')
        user3 = self.buildUser('user3')
        user4 = self.buildUser('user4')
        user5 = self.buildUser('user5')
        target_a_id = 'target_a'
        target_a = self.buildAnnotationTarget(target_a_id)

        self.client.force_authenticate(user1)
        response_user_1 = self.client.post(
            "/users/user1/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_1.json()
        response_user_1_annotation_id = response_value['@id']
        self.client.force_authenticate(user2)
        response_user_2 = self.client.post(
            "/users/user2/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_2.json()
        response_user_2_annotation_id = response_value['@id']
        self.client.force_authenticate(user3)
        response_user_3 = self.client.post(
            "/users/user3/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_3.json()
        response_user_3_annotation_id = response_value['@id']
        annotation_date = response_value['annotation_date']
        self.client.force_authenticate(user4)
        response_user_4 = self.client.post(
            "/users/user4/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_4.json()
        response_user_4_annotation_id = response_value['@id']
        self.client.force_authenticate(user5)
        response_user_5 = self.client.post(
            "/users/user5/yarn/",
            content_type='application/ld+json',
            data=self._create_annotation_create(target_a)
        )
        response_value = response_user_5.json()
        response_user_5_annotation_id = response_value['@id']
        self.client.force_authenticate(user3)

        response = self.client.get(
            "/annotationintersections/before/" + base64.b64encode(target_a_id.encode('UTF-8')).decode('UTF-8') + "/" + annotation_date,
            content_type='application/ld+json'
        )
        response_value = response.json()

        self.assertEqual(response.status_code, 200)
        response_value_content = response_value['ldp:contains'];
        response_length = len(response_value_content)
        self.assertEqual(response_length, 2)
        response_first_id = response_value['ldp:contains'][0]['@id']
        self.assertEqual(response_first_id, response_user_2_annotation_id)
        response_second_id = response_value['ldp:contains'][1]['@id']
        self.assertEqual(response_second_id, response_user_1_annotation_id)

    def _create_annotation_create(self, target):
        return json.dumps({
            "@context": {"@vocab": "http://happy-dev.fr/owl/#",
                         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "rdfs": "http://www.w3.org/2000/01/rdf-schema#", "ldp": "http://www.w3.org/ns/ldp#",
                         "foaf": "http://xmlns.com/foaf/0.1/", "name": "rdfs:label",
                         "acl": "http://www.w3.org/ns/auth/acl#", "permissions": "acl:accessControl",
                         "mode": "acl:mode", "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#", "lat": "geo:lat",
                         "lng": "geo:long", "entrepreneurProfile": "http://happy-dev.fr/owl/#entrepreneur_profile",
                         "mentorProfile": "http://happy-dev.fr/owl/#mentor_profile", "account": "hd:account",
                         "messageSet": "http://happy-dev.fr/owl/#message_set",
                         "author": "http://happy-dev.fr/owl/#author_user",
                         "title": "http://happy-dev.fr/owl/#title"},
            "target": {
                "@id": target.urlid
            }
        })

    def buildAnnotationTarget(self, target):
        target = AnnotationTarget(target=target)
        target.save()
        return target

    def _create_annotation_parse_request(self):
        return json.dumps({
            "@context": {"@vocab": "http://happy-dev.fr/owl/#",
                         "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "rdfs": "http://www.w3.org/2000/01/rdf-schema#", "ldp": "http://www.w3.org/ns/ldp#",
                         "foaf": "http://xmlns.com/foaf/0.1/", "name": "rdfs:label",
                         "acl": "http://www.w3.org/ns/auth/acl#", "permissions": "acl:accessControl",
                         "mode": "acl:mode", "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#", "lat": "geo:lat",
                         "lng": "geo:long", "entrepreneurProfile": "http://happy-dev.fr/owl/#entrepreneur_profile",
                         "mentorProfile": "http://happy-dev.fr/owl/#mentor_profile", "account": "hd:account",
                         "messageSet": "http://happy-dev.fr/owl/#message_set",
                         "author": "http://happy-dev.fr/owl/#author_user",
                         "title": "http://happy-dev.fr/owl/#title"},
            "target": "http://test.startinblox.com"
        })
