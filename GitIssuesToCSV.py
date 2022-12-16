# TASK
"""
- Migrate Issues from a Github repository to a CSV file; 
    using basic authentication (Github username & password) 
    to retrieve Issues from a repository the username has access to. 
- Supports Github API v3
"""

import csv, requests


# Initializing necessary variables 
    # auth details
GITHUB_USER = ''
GITHUB_PASSWORD = ''
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
    # repository Name (username/repository), issues url
REPO = ''  
ISSUES_FOR_REPO_URL = f"https://api.github.com/repos/{REPO}/issues"
    # for all issues, not just open
ARGS = "?state=all" 


# Getting issues via requests and setting up writer & write file
    # response from get requests
res = requests.get(ISSUES_FOR_REPO_URL + ARGS, auth=AUTH)
    # csv file name
csvfile = f"{REPO.replace('/', '-')}-issues.csv"
    # csv writer
pen = csv.writer(open(csvfile, 'w', newline=''))
    # create column headers in csv file
pen.writerow(('id', 'Title', 'Body', 'Created At', 'Updated At'));


# write function
def write_issues(response):
    """
        outputs list of issues to csv, 
        if status code is 200 & issue is not a pull request (PR)
    """ 
    if not res.status_code == 200:
        raise Exception(res.status_code)

    for issue in res.json():
        print (issue['number'])

        if 'pull_request' not in issue:
            pen.writerow([
                issue['number'], 
                issue['title'].encode('utf-8'), 
                issue['body'].encode('utf-8'), 
                issue['created_at'], 
                issue['updated_at']
            ]);

        else:
            print (f"{issue['number']} is PR")


# writing issues into CSV file
write_issues(res)


# writing issues from multiple pages
"""
    Via the Github API, issues(data) may be returned across multiple pages of results; 
    if this is the case, examine the 'link' header returned for page 'url' and 'rel' (handles pagination e.g rel="next")
    extracting both into a dictionary (pages) and scraping the issues contained, into the csv file.
""" 
if 'link' in res.headers:
    # page dictionary (url, rel)
    pages = dict([
        (rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in res.headers['link'].split(',')]
    ])

    while 'last' in pages and 'next' in pages:
        print (pages['next'])
        res = requests.get(pages['next'], auth=AUTH)
        write_issues(res)
        
        if pages['next'] == pages['last']:
            break


# closing csvfile after writing
csvfile.close()
