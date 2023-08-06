# OnePassword CLI v2 python wrapper

Simple python wrapper for the [1password cli](https://developer.1password.com/docs/cli) **version 2**.

## Setup

- Install the `op` cli by following [these instructions](https://developer.1password.com/docs/cli/get-started#install). 
- Make sure you have `op` in your PATH and that it is __not version 1__
```
$ op --version
2.12.0
```
- Have your 1password username, password, and signin url handy
- `pip install onepassword2` \
   __or, for a local install__ \
   `make local_install`

If, for some reason python-Levenshtein fails to compile, skip it

- `pip install fuzzywuzzy && pip install --no-deps onepassword2`

## Usage

### CLI

The `op` cli tool has a _lot_ of options for managing multiple accounts, profiles, etc.  Sessions opened with the cli terminate after 10 minutes, requiring the user to re-authenticate interactively.  This is good security.  However, if you need long running, non-interactive usage, it's a hindrance. onepassword2 comes with a handy CLI to automagify the signin process.

```bash
export OP_ACCOUNT='user@example.com'
export OP_PASSWORD="your password"
export OP_HOSTNAME="my.1password.com"
export OP_SECRET_KEY="JA-EKJHGQ-LKIUHG-12345-12345-12345-32154"

eval $(op-signin)

...

$ op vault list

ID                            NAME
naaizerttzertzefzyhjroeqrq    Private


```

### In python scripts

```python

username = "user@example.com"
password = "your password"
hostname = "yourhost.1password.com"
secret_key = "JA-EKJHGQ-LKIUHG-12345-12345-12345-32154"

from onepassword2 import OP2

o = OP2( username, password, secret_key, hostname)
o.signin()

for v in o.vaults():
    print(v)

```

List items

```python
for d in o.items():
    print(d)
```

Get a single item as a python dictionary

```python
item = o.item("my item")
print(item)
```

Get a single item as an `OP2Item` object with handy methods to modify fields

```python
from onepassword2 import OP2, OP2Item

item = OP2Item(o, "my item")
item.set("notesPlain", "new value for notes")
item.save()
```

If more than one item has the same name, you'll get a `MultipleMatchesException`

```python
from onepassword2 import OP2, OP2Item, MultipleMatchesException

item1 = OP2Item(o)
item1.set("title", "my handy item")
item1.set("notesPlain", "new value for notes")
item1.save()

item2 = OP2Item(o)
item2.set("title", "my handy item")
item2.set("notesPlain", "hahaha same title, different content")
item2.save()

try:
    item = OP2Item(o, "my item")
    print(item)
except MultipleMatchesException:
    for i in o.items("my item"):
        item = OP2Item(o, i["id"])
        ...





```

Make a new secure note

```python
from onepassword2 import OP2, OP2Item

item = OP2Item(o)
item.set("title", "my note")
item.set("notesPlain", "new value for notes")
item.save()
```

If you have more than one vault, you'll need to specify which one to save the secure note to:

```python

from onepassword2 import OP2, OP2Item, OP2Vault

v = OP2Vault(o)
v.name("my new vault")
v.save()

item = OP2Item(o)
item.set("title", "my note")
item.set("vault", "my new vault")
item.set("notesPlain", "new value for notes")
item.save()
```

Example username/password combo:

```python

item = OP2Item(o)
item.set("title", "my account")
item.set('url',  "http://example.com")
item.set('username',  "username@example.com")
item.set('password',  "321657PASKJHKUH")

# urls can also have notes
item.set('notesPlain',  "notes here")

# tags can be set as an array
item.set('tags',  ["tags", "go", "here"])

item.save()
```