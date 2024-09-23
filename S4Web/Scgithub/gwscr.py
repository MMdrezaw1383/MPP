import requests
from pprint import pprint


def get_trending_repos(lang,num_repos):
    repos = []
    page = 1

    while len(repos) < num_repos:
        url = f"https://github.com/search?q={lang}&type=repositories&s=stars&o=desc&p={page}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            page_repo = data['payload']['results'][:num_repos]
            repos.extend(page_repo)
            # pprint(page_repo)
            page += 1
        else:
            print('Error!')
            return []
        return repos
    
lang = input("enter language: ")
num_repos= int(input("number of repos: "))

repos = get_trending_repos(lang,num_repos)

if repos:
    output = f"trending_{lang}_repos.txt"
    with open(output,mode="w",encoding='utf-8') as file:
        file.write(f"Top {num_repos} {lang} repositories on GitHub:\n")
        file.write(50* "*")
        file.write("\n")
        for i, repo in enumerate(repos,start=1):
            file.write(f"#{i}- {repo['repo']['repository']['name']} - {repo['hl_trunc_description']}\n"
                       f"URL:https://github.com/{repo['repo']['repository']['owner_login']}"
                       f"/{repo['repo']['repository']['name']}\n")
            file.write(50*"-")
            file.write("\n")

        print(f"Results saved to {output}")
else:
    print("No repositories found")
            