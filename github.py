import requests
from config import MY_GITHUB_TOKEN, MY_GITHUB_API_URL

def get_github_issues():
    query = """
    query GetProjectItems {
      organization(login: "{MY_GITHUB_ORG}") {
        projectV2(number: {MY_GITHUB_PROJECT_NUMBER}) {
          items(first: 20) {
            nodes {
              content {
                ... on Issue {
                  title
                  url
                  body
                  state
                  createdAt
                }
              }
              fieldValues(first: 10) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {MY_GITHUB_TOKEN}"}
    response = requests.post(MY_GITHUB_API_URL, json={"query": query}, headers=headers)
    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    issues = []
    for node in data["data"]["organization"]["projectV2"]["items"]["nodes"]:
        content = node["content"]
        field_values = node.get("fieldValues", {}).get("nodes", [])
        status = "Не указан"
        for field in field_values:
            if field.get("field", {}).get("name") == "Status":
                status = field.get("name", "Не указан")
                break

        issues.append({
            "title": content["title"],
            "url": content["url"],
            "body": content.get("body", ""),
            "state": content["state"],
            "status": status,
            "createdAt": content["createdAt"]
        })