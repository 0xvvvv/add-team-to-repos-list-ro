import json
import csv
from github import Github
from github.GithubException import GithubException


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def read_csv(file_path):
    repos = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            repos.append(row[0])
    return repos


def grant_read_access_to_team(github_token, organization_name, team_slug, repo_name):
    try:
        g = Github(github_token)
        org = g.get_organization(organization_name)
        team = org.get_team_by_slug(team_slug)
        repo = org.get_repo(repo_name)

        team.set_repo_permission(repo, "pull")
        print(f"Read access granted to team '{team_slug}' for repository '{repo_name}'")
    except GithubException as e:
        print(f"Error: {e}")
        print(f"Failed to grant read access to team '{team_slug}' for repository '{repo_name}'")


def main():
    try:
        credentials = read_json('github_config.json')
        github_token = credentials['token']
        organization_name = credentials['organization']
        team_slug = credentials['team_slug']

        repos = read_csv('repo_list.csv')

        for repo_name in repos:
            grant_read_access_to_team(github_token, organization_name, team_slug, repo_name)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
