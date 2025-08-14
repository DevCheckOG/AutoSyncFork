# AutoSync Fork

Simple script in Python that synchronizes actual fork repositories.

### Usage 

1. First, you need to create an Classical Token (PAT) in the gateway of your Github user.
2. Ensure it has valid permissions to interact with all your repositories.
3. Install the dependencies.
4. Put your token at `.env` file with the name 'GITHUB_TOKEN' in hexadecimal encoded string.
5. Execute.
6. Enjoy! 

### Dependencies

- python-dotenv==1.1.1
- requests==2.32.4

### Python compatibility

- 3.10 - X.X.X or X.XX

#### Command

```console
python fork-sync.py
```
