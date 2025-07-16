#!/usr/bin/env python3
"""Unit and Integration tests for client.py"""

import unittest
from typing import Dict
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from requests import HTTPError

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, resp: Dict, mock_get_json: MagicMock) -> None:
        """Test that GithubOrgClient.org returns expected org data."""
        mock_get_json.return_value = resp
        client = GithubOrgClient(org)
        self.assertEqual(client.org(), resp)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}"
        )

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the correct repos URL."""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/users/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Test that public_repos returns repo names correctly."""
        test_payload = [
            {"name": "episodes.dart"},
            {"name": "kratu"}
        ]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/users/google/repos"
            client = GithubOrgClient("google")
            self.assertEqual(
                client.public_repos(),
                ["episodes.dart", "kratu"]
            )
            mock_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "bsd-3-clause"}}, "bsd-3-clause", True),
        ({"license": {"key": "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Test that has_license returns expected boolean."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with mocked requests."""

    @classmethod
    def setUpClass(cls) -> None:
        """Patch requests.get and return payloads based on URL."""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def mock_get(url):
            if url in route_payload:
                return Mock(**{"json.return_value": route_payload[url]})
            raise HTTPError(f"404: {url} not found")

        cls.get_patcher = patch("requests.get", side_effect=mock_get)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Test public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test filtering public_repos by apache-2.0 license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patcher after all tests."""
        cls.get_patcher.stop()
