import re
import gzip
import urllib.request

db_url = "https://dfast.nig.ac.jp/dfc/distribution/DFAST-default.ref.gz"
pat_attribute = re.compile(r"\[(.+?)=(.*?)\]")

with urllib.request.urlopen(db_url) as rsp:
    f = gzip.open(rsp)
    line = f.readline().decode('utf8').strip()
    assert line.startswith("#") and "[" in line and "]" in line:
    attributes = pat_attribute.findall(line)
    # print(dict(attributes))
    line = f.readline().decode('utf8').strip() # second line
    assert line.startswith("#")
    for line in f:
        