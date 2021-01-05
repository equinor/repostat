RepoStat
====

A tool to scrape open GitHub repositories.

## How to use

With a personal access token:
```
python -m repostat.scrape ORGANIZATION --token ACCESS_TOKEN
```

Username and password:
```
python -m repostat.scrape ORGANIZATION --userpass USER PASS
```

Run anonymous:
```
python -m repostat.scrape ORGANIZATION --anonymous
```

The anonymous mode is highly rate limited.

It is also possible to only scrape the N first repositories:

```
python -m repostat.scrape ORGANIZATION --count N --token ACCESS_TOKEN
```

