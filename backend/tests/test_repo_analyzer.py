"""Tests for repo URL parsing in repo_analyzer."""

from app.services.repo_analyzer import contains_repo_url, parse_repo_url


# ---------- parse_repo_url ----------

def test_github_https():
    result = parse_repo_url("https://github.com/owner/repo")
    assert result == ("github", "owner", "repo")


def test_github_https_with_git_suffix():
    result = parse_repo_url("https://github.com/owner/repo.git")
    assert result == ("github", "owner", "repo")


def test_github_ssh():
    result = parse_repo_url("git@github.com:owner/repo.git")
    assert result == ("github", "owner", "repo")


def test_huggingface_https():
    result = parse_repo_url("https://huggingface.co/org/model-name")
    assert result == ("huggingface", "org", "model-name")


def test_no_match():
    result = parse_repo_url("just some text with no URLs")
    assert result is None


def test_embedded_in_text():
    text = "Check out https://github.com/facebook/react for the code"
    result = parse_repo_url(text)
    assert result == ("github", "facebook", "react")


# ---------- contains_repo_url ----------

def test_contains_true():
    assert contains_repo_url("see https://github.com/a/b") is True


def test_contains_false():
    assert contains_repo_url("no urls here") is False

