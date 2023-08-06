# Unicat client library

This library is still a work in progress, not all Unicat API options are covered yet.

No documentation yet either, just a few short examples.


First, connect to Unicat (https://unicat.app):

```
import sys
from unicat import Unicat
from .env import server, project_gid, api_key, local_folder

unicat = Unicat(server, project_gid, api_key, local_folder)
if not unicat.connect():
  print("Invalid connection settings")
  sys.exit(1)
```

Download all assets for the project (you can find them in the local_folder):

```
for asset in unicat.walk_asset_tree():
  if asset.is_file:
    asset.download()
```

Or, write an XML product feed:

```
with open("product-feed.xml", "w") as f:
  f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
  f.write('<products>\n')

  for record in unicat.walk_record_tree():
    if record.definition.name != "article":
      continue

    fields = record.fields["nl"]

    artnr = fields["artnr"].value
    price = fields["price"].value
    stock = fields["stock"].value

    f.write(f'  <product artnr="{artnr}" price="{price:%0.02f}" stock="{stock}"/>\n')
  f.write('</products>\n')
```

There's also unicat.mutate, with options to update the Unicat project server-side, like unicat.mutate.create_record, unicat.mutate.modify_field and many more.

