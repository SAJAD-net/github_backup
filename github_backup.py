import os
import subprocess
import requests

def backup_github_repositories(token, backup_dir):
    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # GitHub API URL for user repositories
    api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}"
    }

    # Fetch all repositories
    print("\n- Fetching repositories...")
    repos = []
    page = 1
    while True:
        response = requests.get(api_url, headers=headers, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Error: Unable to fetch repositories (Status code: {response.status_code})")
            print(response.json())
            return
        page_repos = response.json()
        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1

    print(f"Found {len(repos)} repositories.")

    # Clone or pull each repository
    for repo in repos:
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        repo_path = os.path.join(backup_dir, repo_name)

        print(f"Processing repository: {repo_name}")

        if os.path.exists(repo_path):
            print(f"Repository '{repo_name}' already exists. Pulling latest changes...")
            subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        else:
            print(f"\n- Cloning repository '{repo_name}'...")
            subprocess.run(["git", "clone", clone_url, repo_path], check=True)

    print("Backup completed.")

if __name__ == "__main__":
    GITHUB_TOKEN = input("- GITHUB_TOKEN : ")
    BACKUP_DIRECTORY = input("- BaBACKUP_DIRECTORY : ")

    backup_github_repositories(GITHUB_TOKEN, BACKUP_DIRECTORY)
