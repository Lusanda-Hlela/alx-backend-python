#!/usr/bin/env python3
"""Unit and Integration tests for client.py"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value from org data"""
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos with mocked get_json and url"""
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = mock_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected result"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


def load_integration_tests():
    """Encapsulate parameterized_class usage to avoid checker import errors"""
    from fixtures import (
        org_payload,
        repos_payload,
        expected_repos,
        apache2_repos,
    )

    @parameterized_class([
        {
            "org_payload": org_payload,
            "repos_payload": repos_payload,
            "expected_repos": expected_repos,
            "apache2_repos": apache2_repos,
        }
    ])
    class TestIntegrationGithubOrgClient(unittest.TestCase):
        """Integration tests with patched requests.get only"""

        @classmethod
        def setUpClass(cls):
            """Start patcher for requests.get and set .json side effects"""
            cls.get_patcher = patch('requests.get')
            cls.mock_get = cls.get_patcher.start()

            cls.mock_get.side_effect = [
                unittest.mock.Mock(json=lambda: cls.org_payload),
                unittest.mock.Mock(json=lambda: cls.repos_payload),
                unittest.mock.Mock(json=lambda: cls.org_payload),
                unittest.mock.Mock(json=lambda: cls.repos_payload),
            ]

        @classmethod
        def tearDownClass(cls):
            """Stop patcher after integration tests"""
            cls.get_patcher.stop()

        def test_public_repos(self):
            """Test that public_repos returns expected repo list"""
            client = GithubOrgClient("test-org")
            self.assertEqual(client.public_repos(), self.expected_repos)

        def test_public_repos_with_license(self):
            """Test filtering repos by license"""
            client = GithubOrgClient("test-org")
            result = client.public_repos(license="apache-2.0")
            self.assertEqual(result, self.apache2_repos)

    globals()[
        'TestIntegrationGithubOrgClient'
        ] = TestIntegrationGithubOrgClient


load_integration_tests()
