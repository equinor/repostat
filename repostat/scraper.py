import argparse
import time

from github import Github
from github.GithubException import UnknownObjectException


def scrape(github, org, count=None):
    git_org = github.get_organization(org)
    org_members = get_organization_members(git_org)

    repos = git_org.get_repos(type='public')
    print(f'Number of repositories: {repos.totalCount}')

    if count:
        count = min(count, repos.totalCount)
    else:
        count = repos.totalCount

    for repo in repos[:count]:
        name = repo.name
        contributors = repo.get_stats_contributors()
        internal = 0
        external = 0
        for contributor in contributors:
            if contributor.author in org_members:
                internal += 1
            else:
                external += 1

        updated_at = repo.updated_at
        try:
            license_type = repo.get_license()
            license_type = license_type.license.name
        except UnknownObjectException:
            license_type = 'Unknown'

        print(f'{name}')
        print(f'\tLicense: {license_type}')
        print(f'\tLast updated: {updated_at}')
        print(f'\tContributor ratio (internal/external): {internal}/{external}')


def get_organization_members(git_org):
    members = git_org.get_members()
    org_members = []
    for member in members:
        org_members.append(member)
    return org_members


def check_rate():
    global crate
    rate = github.get_rate_limit()
    crate = rate.core
    print(f'GitHub remaining queries: {crate.remaining} reset at: {crate.reset}')


if __name__ == '__main__':
    now = time.time()
    parser = argparse.ArgumentParser(description='GitHub repository scraper.',
                                     allow_abbrev=True)
    parser.add_argument('organization', type=str, nargs=1,
                        help='name of the organization to scrape')

    parser.add_argument('--count', type=int, nargs=1, default=None,
                        help='only scrape COUNT number of repositories')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--token', dest='token', type=str, nargs=1,
                       help='GitHub access token')

    group.add_argument('--userpass', dest='user_pass', type=str, nargs=2,
                       metavar=('USER', 'PASS'),
                       help='GitHub username and password')

    group.add_argument('--anonymous', dest='user_pass', action='store_const',
                       metavar=('USER', 'PASS'), const=('anon', 'nopass'),
                       help='GitHub username and password')

    args = parser.parse_args()

    org = args.organization[0]

    count = args.count[0] if args.count else None

    if args.token:
        github = Github(args.token[0])
    else:
        user, password = args.user_pass
        github = Github(user, password)

    check_rate()
    scrape(github, org, count=count)
    check_rate()
    print(f'Running time: {time.time() - now:.2f} seconds')
