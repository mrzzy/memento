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

        update_org(org_id, "company", "http://logo.jpg")
        org = get_org(org_id)
        self.assertEqual(org["name"], "company")

        delete_org(org_id)
        self.assertEqual(query_orgs(), [])

    def test_team_ops(self):
        self.assertEqual(query_teams(), [])
        org_id = create_org("kompany", "http://logo.jpg")
        team_id = create_team(org_id, "designer")

        team = get_team(team_id)
        self.assertEqual(team["name"], "designer")
        self.assertEqual(query_teams(), [team_id])
        self.assertEqual(query_teams(org_id=org_id), [team_id])
        self.assertEqual(query_teams(org_id=-1), [])

        update_team(team_id, name="ui/ux")
        team = get_team(team_id)
        self.assertEqual(team["name"], "ui/ux")

        delete_team(team_id)
        self.assertEqual(query_teams(), [])
        delete_org(org_id)
