#
# Memento
# Backend
# IAM Tests
#

from unittest import TestCase

from ...ops.iam import *

class TestIAMOps(TestCase):
    def test_org_ops(self):
        self.assertEqual(query_orgs(), [])
        org_id = create_org("kompany", "http://logo.jpg")

        org = get_org(org_id)
        self.assertEqual(org["name"], "kompany")
        self.assertEqual(query_orgs(), [org_id])
        self.assertEqual(len(query_orgs(skip=1)), 0)
        self.assertEqual(len(query_orgs(limit=0)), 0)

        update_org(org_id, "company", "http://logo.jpg")
        org = get_org(org_id)
        self.assertEqual(org["name"], "company")

        delete_org(org_id)
        self.assertEqual(query_orgs(), [])
