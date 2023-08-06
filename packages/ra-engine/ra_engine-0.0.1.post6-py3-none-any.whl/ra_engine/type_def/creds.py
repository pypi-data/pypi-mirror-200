class Credentials:
    def __init__(self, host, email, password, project=None, apiKey=None):
        self.host = host
        self.email = email
        self.password = password
        self.project = project
        self.apiKey = apiKey
