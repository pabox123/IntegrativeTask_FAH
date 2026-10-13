import re
from typing import List


class DatabaseToolExtractor:
    DATABASES_TOOLS_REGEX = r"""
        \b(?:
            PostgreSQL |
            Postgres |
            MySQL |
            MariaDB |
            MongoDB |
            Redis |
            SQLite |
            Oracle |
            DynamoDB |
            Git |
            GitHub |
            GitLab |
            Docker |
            Kubernetes |
            K8s |
            Jenkins |
            Terraform |
            AWS |
            GCP |
            Azure |
            Linux |
            Bash |
            Postman |
            Jira
        )\b
    """

    @classmethod
    def extract_databases_and_tools(cls, text: str) -> List[str]:
        #compile pattern
        pattern = re.compile(cls.DATABASES_TOOLS_REGEX, re.VERBOSE | re.IGNORECASE)

        # search all matches
        matches = pattern.findall(text)

        # normalize
        found_items = []
        seen = set()
        for item in matches:
            # clean spaces
            clean_item = item.strip()
            # case-insensitive, no duplicate values
            upper_item = clean_item.upper()
            if upper_item not in seen:
                seen.add(upper_item)
                found_items.append(clean_item)

        return found_items