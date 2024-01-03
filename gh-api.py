import json
import subprocess

def GetLabelNames(data: json) -> list:
    res = []
    for label in data:
        res.append(label['name'])
    return res

def GetDBMS(issue) -> str:
    
    labels = GetLabelNames(issue["labels"])
    

    if 'PostGIS' in labels:
        return 'postgis'
    elif 'duckdb' in labels:
        return 'duckdb'
    elif 'SQLServer' in labels:
        return 'sqlserver'
    elif 'mysql GIS' in labels:
        return 'mysql'
    elif 'libgeos' in labels:
        return 'libgeos'
    else:
        print(f"Cannot find DBMS: {labels}")
        exit(0)

def GetOracle(issue) -> str:
    labels = GetLabelNames(issue["labels"])

    if 'crash' in labels:
        return 'crash'
    elif 'sytax trans' in labels:
        return 'sytax trans'
    elif 'coordinate trans' in labels:
        return 'coordinate trans'
    elif 'index' in labels:
        return 'index'
    elif 'differential' in labels:
        return 'differential'
    else:
        print(f"Cannot find Oracle: {labels}")
        exit(0)

def GetStatus(issue) -> str:
    labels = GetLabelNames(issue["labels"])

    if 'fixed' in labels:
        return 'fixed'
    elif 'bug-confirm' in labels:
        return 'verified'
    elif 'reported' in labels:
        return 'reported'
    elif 'won\'t fix' in labels:
        return 'verified'
    elif 'duplicate' in labels:
        return 'duplicate'
    else:
        return 'not report yet'
    
def GetLinks(iid: int):
    command = f"gh api repos/cuteDen-ECNU/SpatialDB-testing/issues/{iid}/comments"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode == 0:
        link_dist = {}
        data = json.loads(result.stdout)
        for comment in data:
            body = comment['body']
            if "bugtracker link:" not in body:
                continue
            link_list  = body.split('\n')
            for link in link_list:
                link_dist[link.split(' link:')[0]] = link.split('link:')[1]
        return link_dist
    else:
        print(f"Failed to fetch issue#{iid} comments. Error: {result.stderr}")
        exit(0)

def main():
    command = "gh api repos/cuteDen-ECNU/SpatialDB-testing/issues --paginate"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        data = json.loads(result.stdout)
        issues_data = []

        for issue in data:
            number = issue["number"]
            print(number)
            if len(GetLabelNames(issue["labels"])) < 3: continue
            date = issue["created_at"]
            dbms = GetDBMS(issue)
            oracle = GetOracle(issue)
            if oracle == 'crash':
                type = 'crash'
            else:
                type = 'logic'
            reporter = issue["user"]["login"]
            status = GetStatus(issue)
            test = issue.get("test", "N/A")
            title = issue["title"]

            if issue["comments"] >= 1:
                links = GetLinks(issue["number"])

            issues_data.append({
                "number": number,
                "date": date,
                "dbms": dbms,
                "oracle": oracle,
                "type": type,
                "reporter": reporter,
                "status": status,
                "test": test,
                "title": title,
                "links": links

            })
        with open('bugs.json', 'w') as of:
            json.dump(issues_data, of)
        
    else:
        print(f"Failed to fetch issues. Error: {result.stderr}")

    

main()