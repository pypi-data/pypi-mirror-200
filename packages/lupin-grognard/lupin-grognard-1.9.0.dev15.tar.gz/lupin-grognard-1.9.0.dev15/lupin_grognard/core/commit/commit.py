import re
from datetime import datetime
from typing import List

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
    def add_additional_commit_info(cls, commit_list: List[str]) -> List["Commit"]:
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
        commits = cls._add_associated_data_to_commit_from_merge(commits=commits)
        return commits

    @classmethod
    def _get_parents_for_commits(cls, commits: List["Commit"]) -> List["Commit"]:
        for commit in commits:
            commit.parents = Git().get_parents(commit_hash=commit.hash)
        return commits

    @classmethod
    def _add_associated_data_to_commit_from_merge(
        cls, commits: List["Commit"]
    ) -> List["Commit"]:
        """
        Returns a list of commits with associated closed issues, merge request approvers, and dates.
        For each commit in the input list, if it is a merge commit with a closed issue,
        the closed issue number, approvers, and date are stored in a dictionary.
        Subsequent non-merge commits that are descendants of the merge commit are then updated with
        these values as associated data. This process continues until the next merge commit is encountered.

        Args:
            commits: A list of Commit objects.

        Returns:
            A new list of Commit objects with associated closed issue numbers, merge request approvers, and dates.
        """
        hash_to_closed_issue_mapping = {}
        commit_parent = None
        for commit in commits:
            if len(commit.parents) > 1:  # is merge commit
                commit_parent = commit.parents[1]
                if commit.closes_issues:
                    hash_to_closed_issue_mapping = {
                        "closed_issue": commit.closes_issues[0],
                        "approvers": commit.approvers,
                        "date": commit.author_date,
                    }
            elif hash_to_closed_issue_mapping and commit.hash == commit_parent:
                commit_parent = commit.parents[0]
                if commit_parent:
                    commit.associated_closed_issue = hash_to_closed_issue_mapping[
                        "closed_issue"
                    ]
                    commit.associated_mr_approvers = hash_to_closed_issue_mapping[
                        "approvers"
                    ]
                    commit.associated_mr_approvers_date = hash_to_closed_issue_mapping[
                        "date"
                    ]
        return commits

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
