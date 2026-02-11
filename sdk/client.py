import requests
import os

class CompetitionClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def submit(self, username, file_path):
        """Submits a zip file to the competition."""
        url = f"{self.base_url}/submit"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'username': username}
            response = requests.post(url, files=files, data=data)
        return response.status_code

    def get_leaderboard(self):
        """Fetches the current leaderboard (HTML or JSON if we added API)."""
        # Note: The current / endpoint returns HTML, needing parsing or a JSON endpoint.
        # For SDK, usually we'd hit a /api/leaderboard endpoint.
        pass

if __name__ == "__main__":
    # Example usage
    client = CompetitionClient()
    # client.submit("test_user", "submission.zip")
