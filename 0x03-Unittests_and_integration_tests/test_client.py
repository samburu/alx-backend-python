#!/usr/bin/env python3
"""
Unit tests for  the module client.py.
"""
import unittest
from unittest.mock import PropertyMock, patch

from client import GithubOrgClient
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org property."""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data and
        calls get_json once with the correct URL."""
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        result = client.org  # property call triggers get_json internally

        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)

        # Assert get_json called once with correct URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert the returned org value is the mocked response
        self.assertEqual(result, {"org": org_name})

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns correct repos_url from org payload
        """
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
        mock_org.assert_called_once()

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Unit-test for GithubOrgClient.public_repos
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    [
        {
            "org_payload": org_payload,
            "repos_payload": repos_payload,
            "expected_repos": expected_repos,
            "apache2_repos": apache2_repos,
        }
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mocks"""
        cls.get_patcher = patch("requests.get")

        mock_get = cls.get_patcher.start()

        # Mock response.json() with side_effect to serve responses in order
        mock_get.return_value.json.side_effect = [
            cls.org_payload,  # first call to get_json() for org
            cls.repos_payload,  # second call for repos_payload
            cls.repos_payload,  # subsequent calls may re-fetch repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop all patches"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method returns expected repos"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method filters by license"""
        client = GithubOrgClient("test_org")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos
        )
