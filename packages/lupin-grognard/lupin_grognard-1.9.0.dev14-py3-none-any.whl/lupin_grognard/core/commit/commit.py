import re
from datetime import datetime
from typing import List, Dict

from lupin_grognard.core.config import PATTERN
from lupin_grognard.core.git import Git


class Commit:
    def __init__(self, commit: str):
        self.commit = commit
        self.associated_closed_issue = None
        self.associated_mr_approvers = None
        self.associated_mr_approvers_date = None
        self.parents = None

    @classmethod
    def get_additional_commit_info(cls, commit_list: List[str]) -> List["Commit"]:
        """
        Returns a list of Commit objects with additional information such as closed issues, approvers,
        and date it was approved for each commit from associated merge request

        :param commit_list: List of commits
        :return: List of Commit objects with additional information

        additional information:
            self.associated_closed_issue = None if merge commit else "1"
            self.associated_mr_approvers = None if merge commit else "John Doe"
            self.associated_mr_approvers_date = None if merge commit else "10/03/23 06:48 PM"
            self.parrents = ["hash1", "hash2"] if merge commit else ["hash1"]
        """
        commits = [cls(commit) for commit in commit_list]
        commits = cls._get_parents_for_commits(commits=commits)
        commits = cls._get_closed_issues_approvers_and_date_for_commits(commits=commits)
        return commits

    @classmethod
    def _get_parents_for_commits(cls, commits: List["Commit"]) -> List["Commit"]:
        for commit in commits:
            commit.parents = Git().get_parents(commit_hash=commit.hash)
        return commits

    @classmethod
    def _get_closed_issues_approvers_and_date_for_commits(
        cls, commits: List["Commit"]
    ) -> List["Commit"]:
        """Assign closed issue number, approvers, and date it was approved for commits"""
        hash_to_closed_issue_mapping = {}
        for commit in commits:
            if len(commit.parents) > 1:  # is merge commit
                if commit.closes_issues:
                    for parent, associated_closed_issue in zip(
                        commit.parents[
                            1:
                        ],  # We skip the first parent because it's the merge commit
                        commit.closes_issues,
                    ):
                        hash_to_closed_issue_mapping[parent] = [
                            associated_closed_issue,
                            commit.approvers,
                            commit.author_date,
                        ]
        cls._associate_closed_issues_and_approvers_with_commits(
            hash_to_closed_issue_mapping=hash_to_closed_issue_mapping, commits=commits
        )
        return commits

    @classmethod
    def _associate_closed_issues_and_approvers_with_commits(
        cls, hash_to_closed_issue_mapping: Dict[str, str], commits: List["Commit"]
    ):
        for key, value in hash_to_closed_issue_mapping.items():
            for commit in commits:
                if commit.hash == key:
                    commit.associated_closed_issue = value[0]
                    commit.associated_mr_approvers = value[1]
                    commit.associated_mr_approvers_date = value[2]

    @property
    def hash(self) -> str:
        return self._extract(start="hash>>")

    @property
    def author(self) -> str:
        return self._extract(start="author>>")

    @property
    def author_mail(self) -> str:
        return self._extract(start="author_mail>>")

    @property
    def author_date(self) -> str:
        timestamp = self._extract(start="author_date>>")
        date_object = datetime.fromtimestamp(int(timestamp))
        return date_object.strftime("%d/%m/%y %I:%M %p")

    @property
    def title(self) -> str:
        return self._extract(start="title>>")

    @property
    def title_without_type_scope(self) -> str:
        """Returns commit title without type and scope"""
        start = self.title.find(":") + 1
        return self.title[start:].strip().capitalize()

    @property
    def type(self) -> str | None:
        """Returns the conventional commit type if present"""
        match = re.match(PATTERN, self.title)
        return match.groups()[0] if match else None

    @property
    def scope(self) -> str | None:
        """Returns the conventional commit scope if present"""
        match = re.match(PATTERN, self.title)
        return match.groups()[1] if match else None

    @property
    def body(self) -> List[str] | None:
        body = self._extract(start="body>>", end="<<body")
        if body == "":
            return None
        return [message for message in body.split("\n") if len(message) > 0]

    @property
    def closes_issues(self) -> List | None:
        """Returns the list of issues closed by the commit"""
        if self.body:
            for line in self.body:
                if line.startswith("Closes #"):  # Closes #465, #190 and #400
                    return re.findall(r"#(\d+)", line)  # ['465', '190', '400']
        return None

    @property
    def approvers(self) -> List[str]:
        approvers = []
        if self.body:
            for line in self.body:
                if line.startswith("Approved-by: "):
                    approvers.append(line.split("Approved-by: ")[1])
            return approvers
        return list()

    def _extract(self, start: str, end: str = "\n") -> str:
        start_index = self.commit.find(start) + len(start)
        return self.commit[start_index : self.commit.find(end, start_index)]
