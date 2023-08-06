# GitConnect

GitConnect is a Python library that provides an interface for interacting with the GitHub API. It allows you to easily search for repositories by user and keyword, get details about a specific repository, and more.

## Installation
To install GitConnect, simply run:
    
        pip install gitconnect

## Usage
First, you'll need a personal access token for the GitHub API. You can create one by following these steps:
1. Go to https://github.com/settings/tokens and click "Generate new token".
2. Give your token a name and select the scopes that it needs.
3. Click "Generate token" and copy the token value.

Next, create a GitWrapper object with your access token:
```python
from gitconnect import GitWrapper

access_token = 'your_access_token_here'

wrapper = GitWrapper(access_token)
```

Now, you can use the GitWrapper methods to interact with the GitHub API.

## Example 1: Search for repositories by user and keyword
```python
from gitconnect import GitWrapper

access_token = 'your_access_token_here'

wrapper = GitWrapper(access_token)
user_name ="the_git_user_name_here"
repos = wrapper.search_repos_by_user(user_name, "python")
for repo in repos:
    print(repo.name)
```

## Example 2: Get details about a specific repository
```python

from gitconnect import GitWrapper

access_token = 'your_access_token_here'

wrapper = GitWrapper(access_token)
user_name ="the_git_user_name_here"
repo = wrapper.get_repo(user_name, "hello-world")
print(repo.name)
print(repo.description)
```

For more information on how to use GitConnect, please refer to the documentation.

## Contributing

If you would like to contribute to GitConnect, please follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your feature or bug fix.
3. Write code and tests for your feature or bug fix.
4. Run tests using pytest to make sure everything works.
5. Push your changes to your forked repository.
6. Create a pull request to the original repository.

## License

GitConnect is licensed under the MIT License. See LICENSE for more information.

