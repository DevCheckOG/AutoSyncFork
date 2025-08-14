import requests
import dotenv
import os
import sys

from typing import Dict, List, Any

dotenv.load_dotenv(encoding= "utf-8")

GITHUB_BASE_URL: str = "https://api.github.com"
GITHUB_TOKEN: str = bytes.fromhex(os.environ["GITHUB_TOKEN"]).decode("utf-8")

REQUEST_HEADERS: Dict[str, str] = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_forked_repos() -> List[Dict[str, Any]]:
    url: str = f"{GITHUB_BASE_URL}/user/repos"
    repos: List[Dict[str, Any]] = []
    page: int = 1

    while True:
        response = requests.get(url, headers= REQUEST_HEADERS, params= {"page": page, "per_page": 100})

        if response.status_code != 200:
            print(f"Repository couldn't be obtained, because: '{response.json().get('message')}'.")
            continue

        data = response.json()

        if not data:
            break

        forks = [repo for repo in data if repo["fork"]]
        repos.extend(forks)
        page += 1

    return repos

def sync_fork(repo) -> None:
    repo_name: str = repo["full_name"]
    branch: Any = repo["default_branch"]

    url: str = f"{GITHUB_BASE_URL}/repos/{repo_name}/merge-upstream"
    payload: Dict[str, Any] = {"branch": branch}

    response = requests.post(url, headers= REQUEST_HEADERS, json= payload)

    if response.status_code == 200:
        print(f"'{repo_name}' repository synchronized.")
    elif response.status_code == 409:
        print(f"\nRepository '{repo_name}' couldn't be synchronized due a merge conflict.\n")
    else:
        print(f"\nFailure to synchronize '{repo_name}' repository.\n")

def start_sync() -> None:
    forked_repos: List[Dict[str, Any]] = get_forked_repos()

    if not forked_repos:
        print("Forked repositories not found in the current user.")
        return
    
    for repo in forked_repos:
        print(f"Synchronizing '{repo['full_name']}' repository...")
        sync_fork(repo)

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("GITHUB TOKEN aren't setup correctly. Visualize the dotenv environment, first.")
        sys.exit(1)

    start_sync()
