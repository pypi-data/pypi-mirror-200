from collections.abc import Generator
from datetime import datetime, timedelta
import dateutil.tz
import gzip
import json
import logging
import math
import requests

from perceval.backend import Backend, BackendCommand, BackendCommandArgumentParser
from perceval.utils import DEFAULT_LAST_DATETIME

from perceval_gharchive.backends._version import __version__


logger = logging.getLogger(__name__)


DEFAULT_FIRST_DATETIME = datetime(2011, 12, 2, 10, 0, 0, tzinfo=dateutil.tz.tzutc())

# TODO: add default categories that have a default set of events.
CATEGORY_EVENTS = "events"

COMMIT_COMMENT_EVENT = "CommitCommentEvent"
CREATE_EVENT = "CreateEvent"
DELETE_EVENT = "DeleteEvent"
FORK_EVENT = "ForkEvent"
GOLLUM_EVENT = "GollumEvent"
ISSUE_COMMENT_EVENT = "IssueCommentEvent"
ISSUES_EVENT = "IssuesEvent"
MEMBER_EVENT = "MemberEvent"
PUBLIC_EVENT = "PublicEvent"
PULL_REQUEST_EVENT = "PullRequestEvent"
PULL_REQUEST_REVIEW_EVENT = "PullRequestReviewEvent"
PULL_REQUEST_REVIEW_COMMENT_EVENT = "PullRequestReviewCommentEvent"
PULL_REQUEST_REVIEW_THREAD_EVENT = "PullRequestReviewThreadEvent"
PUSH_EVENT = "PushEvent"
RELEASE_EVENT = "ReleaseEvent"
SPONSORSHIP_EVENT = "SponsorshipEvent"
WATCH_EVENT = "WatchEvent"


class GHArchive(Backend):
    version: str = __version__
    CATEGORIES: "list[str]" = [CATEGORY_EVENTS]

    _projects: "list[tuple[str, str]]" = []

    def __init__(
        self,
        owner: str = None,
        repository: str = None,
        projects: "list[tuple[str,str]] | list[str]" = None,
        tag=None,
        archive=None,
    ) -> None:
        """
        :param str owner: GitHub owner.
        :param str repository: GitHub repository.
        :param list[tuple[str, str]] | list[str] projects: List of GitHub owner/repository combinations.
        """

        super().__init__(origin="gharchive.org", tag=tag, archive=archive)

        if not projects is None:
            if len(projects) > 0 and isinstance(projects[0], str):
                projects = list([entry.split("/") for entry in projects])
            self._projects = projects
        elif not (owner is None or repository is None):
            self._projects = [(owner, repository)]
        else:
            logging.warning(
                "No list of projects provided. Collecting all GHArchive data."
            )

    @staticmethod
    def __timestamp_to_url(timestamp: datetime) -> str:
        return f"http://data.gharchive.org/{timestamp.year}-{timestamp.month:02d}-{timestamp.day:02d}-{timestamp.hour:02d}.json.gz"

    def fetch_items(self, category, **kwargs) -> "Generator[dict, None, None]":
        from_date = kwargs["from_date"]
        to_date = kwargs["to_date"]
        events = set(kwargs["events"])

        # Iterates through all hours between now and the specified end date.
        delta_hours = math.floor((to_date - from_date).total_seconds() / 3600)
        for hour in range(1, delta_hours):
            # Retrieves asynchronous HTTP request and starts next one.
            timestamp: datetime = from_date + timedelta(hours=hour)
            url = self.__timestamp_to_url(timestamp)
            response = requests.get(url)

            if response.status_code // 100 != 2:
                if response.status_code != 404:
                    logging.critical(
                        f"Request failed with statuscode {response.status_code} for timestamp {timestamp}."
                    )
                continue

            # Bulk data is unpacked and iterates through all entries.
            data = gzip.decompress(bytearray(response.content)).decode("utf-8")
            for item_str in data.split("\n"):
                item_str = item_str.strip()
                if item_str == "":
                    continue
                item = json.loads(item_str)
                if not item["type"] in events:
                    continue
                yield item

    def fetch(
        self,
        category,
        events: "str | list[str]",
        from_date: datetime = DEFAULT_FIRST_DATETIME,
        to_date: datetime = DEFAULT_LAST_DATETIME,
    ):
        if isinstance(events, str):
            events = [events]

        kwargs = {
            "events": events,
            "from_date": from_date,
            "to_date": to_date,
        }

        return super().fetch(category, **kwargs)

    def fetch_from_archive(self):
        return super().fetch_from_archive()

    @classmethod
    def has_archiving(cls):
        # TODO: Implement this.
        return False

    @classmethod
    def has_resuming(cls):
        return True

    def metadata(self, item, filter_classified=False):
        # TODO: Figure out how to get the used event types in the metadata.
        item = super().metadata(item, filter_classified)
        return item

    @staticmethod
    def metadata_id(item) -> str:
        return f'{item["type"]}_{item["id"]}'

    @staticmethod
    def metadata_updated_on(item):
        updated_on = datetime.strptime(item["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        return updated_on.timestamp()

    @staticmethod
    def metadata_category(item):
        return CATEGORY_EVENTS

    def _init_client(self, from_archive=False):
        return None


class GHArchiveCommand(BackendCommand):
    BACKEND = GHArchive

    @classmethod
    def setup_cmd_parser(cls):
        parser = BackendCommandArgumentParser(
            cls.BACKEND,
            from_date=True,
            to_date=True,
            token_auth=False,
            archive=False,
            ssl_verify=False,
        )

        group = parser.parser.add_argument_group("GHArchive arguments")
        group.add_argument("-o", "--owner", dest="owner", help="GitHub owner")
        group.add_argument(
            "-r", "--repository", dest="repository", help="GitHub repository"
        )
        group.add_argument(
            "-p",
            "--projects",
            dest="projects",
            nargs="+",
            help="List of GitHub owner/repository combinations.",
        )

        return parser
