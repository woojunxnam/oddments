exec(open(__file__.replace('retrieve-extra.py','retrieve.py')).read().split('with concurrent.futures')[0].split('urls=sorted')[0])
extra=[('48','https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=8a5edcf9-828c-4f97-b671-268ab13a8ecd'),('49','https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=57583c1d-9c44-4503-917d-68dba7377bd1')]
source=open(__file__.replace('retrieve-extra.py','retrieve.py')).read();exec(source[source.index('def fetch'):source.index('with concurrent.futures')])
for stem,url in extra:print(fetch((int(stem),url)))
