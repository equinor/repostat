import argparse
from github import Github
from github.GithubException import UnknownObjectException


def scrape(github, org):
    git_org = github.get_organization(org)
    repos = git_org.get_repos()
    print(repos.totalCount)
    for repo in repos:
        name = repo.full_name
        try:
            license = repo.get_license()
        except UnknownObjectException:
            license = 'Unknown'
        print(f'{name} {license}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GitHub repository scraper.',
                                     allow_abbrev=True)
    parser.add_argument('organization', type=str, nargs=1,
                        help='name of the organization to scrape')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--token', dest='token', type=str, nargs=1,
                       help='GitHub access token')

    group.add_argument('--userpass', dest='user_pass', type=str, nargs=2,
                       metavar=('USER', 'PASS'),
                       help='GitHub username and password')

    args = parser.parse_args()

    org = args.organization[0]
    if args.token[0]:
        github = Github(args.token[0])
    else:
        user, password = args.user_pass[0]
        github = Github(user, password)

    rate = github.get_rate_limit()
    crate = rate.core
    print(f'GitHub remaining queries: {crate.remaining} reset at: {crate.reset}')
    scrape(github, org)
    print(f'GitHub remaining queries: {crate.remaining} reset at: {crate.reset}')
