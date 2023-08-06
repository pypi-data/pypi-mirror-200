import requests

class GithubAPI:
    def __init__(self, username, token):
        self.username = username
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'User-Agent': 'Python'
        }

    def create_repo(self, name):
        url = f'https://api.github.com/user/repos'
        data = {
            'name': name,
            'private': False
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            return None

    def list_repos(self):
        url = f'https://api.github.com/user/repos'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_repo(self, name):
        url = f'https://api.github.com/repos/{self.username}/{name}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def delete_repo(self, name):
        url = f'https://api.github.com/repos/{self.username}/{name}'
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return True
        else:
            return False
    
    def search_repos(self, keywords):
        url = f'https://api.github.com/search/repositories?q=user:{self.username}+{keywords}'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()['items']
        else:
            return None