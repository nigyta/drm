import sys
import os
import re
import gzip
import urllib.request
import django
 
db_url = "https://dfast.nig.ac.jp/dfc/distribution/DFAST-default.ref.gz"
pat_attribute = re.compile(r"\[(.+?)=(.*?)\]")

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","drm_project.settings")
 
django.setup()
 
from drm.models import Protein
Protein.objects.all().delete()
 
# existing_ref_ids = Protein.objects.values_list('ref_id', flat=True)
print('connect ok')
# print(len(existing_ref_ids))
with urllib.request.urlopen(db_url) as rsp:
    f = gzip.open(rsp)
    line = f.readline().decode('utf8').strip()
    assert line.startswith("#") and "[" in line and "]" in line
    attributes = pat_attribute.findall(line)
    # print(dict(attributes))
    line = f.readline().decode('utf8').strip() # second line
    assert line.startswith("#")
    for line in f:
        line = line.decode('utf8').strip().split("\t")
        ref_id = line[0]
        if len(line) != 8:
            continue
        if not Protein.objects.filter(ref_id=ref_id).exists():
        # if ref_id not in existing_ref_ids:
            try:
                Protein.objects.create(
                    ref_id = line[0],
                    description = line[1],
                    gene = line[2],
                    ec_number = line[3],
                    flag = line[4],
                    organism = line[5],
                    source_db = line[6],
                    sequence = line[7])
            # except django.db.utils.DataError as e:
            except Exception as e:
                print(line)
                raise e
# Protein.objects.create(
#     ref_id='Sample_id', 
#     description='Sample title', 
#     gene='Sample gene', 
#     ec_number='Sample ec_number', 
#     flag='Sample flag', 
#     organism='Test organism',
#     source_db='Test source_db',
#     sequence='Test sequence'
#     )

# p=Protein.objects.get_or_create("testid1")

# protein = Protein(
#     ref_id='Sample_id2', 
#     description='Sample title', 
#     gene='Sample gene', 
#     ec_number='Sample ec_number', 
#     flag='Sample flag', 
#     organism='Test organism',
#     source_db='Test source_db',
#     sequence='Test sequence'
#     )
# protein.save()

proteins = Protein.objects.all()
print(proteins)