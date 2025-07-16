#!/usr/bin/env python3
"""Fixtures used for integration tests"""

org_payload = {
    "login": "test-org",
    "id": 123456,
    "repos_url": "https://api.github.com/orgs/test-org/repos"
}

repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "mit"}},
    {"id": 3, "name": "repo3", "license": {"key": "apache-2.0"}},
]

expected_repos = ["repo1", "repo2", "repo3"]

apache2_repos = ["repo1", "repo3"]

TEST_PAYLOAD = [{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos
}]
