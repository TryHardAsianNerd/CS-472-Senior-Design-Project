import json
import requests
import csv

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, allTouches, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    counter = 0
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson =  shaDetails['files']
                authorjson = shaDetails['commit']
                authorname = authorjson['author']['name']
                accessdate = authorjson['author']['date']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    for x in files:
                        if filename == x:
                            date = accessdate.split('T')
                            commitdata = [authorname, str(filenums.get(x)), date[0]]
                            allTouches.append(commitdata)

            ipage += 1

    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = ["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"]

dictfiles = dict()
filenums = dict()
filenum = 0

filename = 'data.csv'
files = []

with open(filename, 'r') as csvfile:
    datareader = csv.DictReader(csvfile)
    for row in datareader:
        files.append(row['Filename'])

for currfile in files:
    filenums[currfile] = filenums.get(currfile, filenum)
    filenum += 1

allTouches = []

countfiles(dictfiles, allTouches, lstTokens, repo)

file = 'authors' + repo.split('/')[1]
# change this to the path of your file
fileOutput = 'jr_file_' + file + '.csv'

fileCSV = open(fileOutput, 'w', newline = '')
writer = csv.writer(fileCSV)
rows = ["Author", "File-ID", "Date"]
writer.writerow(rows)

for x in allTouches:
    writer.writerow(x)

fileCSV.close()
print('The file ' + fileOutput + ' has been created.')