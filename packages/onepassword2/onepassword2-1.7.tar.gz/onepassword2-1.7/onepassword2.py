#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from subprocess import Popen, PIPE
import os, json
from fuzzywuzzy import fuzz
import shlex


DEBUG = False

def debug(s):
    if DEBUG:
        print(s)

class RunException(Exception):
    pass

class OPException(Exception):
    pass

class MultipleMatchesException(Exception):
    pass

class NoVaultException(Exception):
    pass

class NoSuchVaultException(Exception):
    pass

class NoSuchItemException(Exception):
    pass

def run(cmd, splitlines=False, env=None, raise_exception=False):
    # you had better escape cmd cause it's goin to the shell as is
    if env == None:
        env = os.environ.copy()
    proc = Popen([cmd], stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True, env=env)
    out, err = proc.communicate()
    if splitlines:
        out_split = []
        for line in out.split("\n"):
            line = line.strip()
            if line != '':
                out_split.append(line)
        out = out_split
    exitcode = int(proc.returncode)
    if raise_exception and exitcode != 0:
        raise RunException(err)
    return (out, err, exitcode)

class OP2(object):

    def __init__(self, username: str, password: str, secret_key: str, hostname: str="my.1password.com", session_token = None):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.secret_key = secret_key
        self.session_token = session_token

    def status(self):
        if self.session_token == None:
            debug("status: no token")
            return False
        return True

    def signin(self):
        if self.status():
            return

        env2 = os.environ.copy()
        #env2["HOME"] = os.environ["HOME"]
        #env2["OP_ACCOUNT_ALIAS"] = self.username

        # try:
        #     run('op account forget "$OP_ACCOUNT_ALIAS"', env=env2, raise_exception=True)
        # except:
        #     run('op signout --account "$OP_ACCOUNT_ALIAS" --forget | true', env=env2)

        env2["OP_ACCOUNT"] = self.username
        env2["OP_PASSWORD"] = self.password
        env2["OP_HOSTNAME"] = self.hostname
        env2["OP_SECRET_KEY"] = self.secret_key

        run('echo "$OP_PASSWORD" | op account add --shorthand "$OP_ACCOUNT" --address "$OP_HOSTNAME" --email "$OP_ACCOUNT"', env=env2,  raise_exception=True)
        #run('echo "$OP_PASSWORD" | op account add --address "$OP_HOSTNAME" --email "$OP_ACCOUNT"', env=env2,  raise_exception=True)
        out, err, retcode = run('echo $OP_PASSWORD | op signin --account "$OP_ACCOUNT" -f', splitlines=True, env=env2, raise_exception=True)
        k,v = out[0].split("=",1)
        k = k[7:]
        v = v[1:-1]
        self.session_token = (k,v)
        debug("setting session token")

    def _decode(self, cmd):
        self.signin()

        env2 = os.environ.copy()
        #env2["HOME"] = os.environ["HOME"]

        env2[self.session_token[0]] = self.session_token[1]
        env2["OP_ACCOUNT"] = self.username

        out, err, exitcode = run(cmd, env=env2)

        if exitcode != 0:
            if "ore than one item matches" in err:
                raise MultipleMatchesException(err)
                
            raise OPException(err)
        return json.loads(out)   

    def _delete(self, which, thing):
        cmd = "op {} delete {} ".format(which, shlex.quote(thing))

        env2 = os.environ.copy()
        env2[self.session_token[0]] = self.session_token[1]
        out, err, exitcode = run(cmd, env=env2, raise_exception=True)

    def _list(self, thing, vault=None):
        cmd = "op {} list --format=json".format(thing)
        if vault != None:
            cmd += " --vault {} ".format(shlex.quote(vault))
        return self._decode(cmd)

    def _get(self, which, thing, vault=None):
        id = thing
        if type(thing) is dict:
            id = thing["id"]
        cmd = "op {} get {} --format=json".format(which, shlex.quote(id))
        if vault != None:
            cmd += " --vault {} ".format(shlex.quote(vault))
        debug(cmd)

        return self._decode(cmd)


    def _list_get(self, thing, filter=None, vault=None):
        for l1 in self._list(thing, vault=vault):
            lim = 80

            if filter != None:
                f = filter.lower()
                ratio = fuzz.ratio(f, l1["title"].lower())
                debug("{} fuzzy ratio {}".format(l1["title"], ratio))
                if f in l1["title"].lower():
                    ratio = 90
                if ratio <= lim:
                    continue

            id = l1["id"]

            yield self._get(thing, id)

    def vaults(self, filter=None):
        return self._list_get("vault", filter)

    def documents(self):
        return self._list_get("document")

    def items(self, filter=None, vault=None):
        return self._list_get("item", filter, vault)

    def item(self, item, vault=None):
        try:
            return self._get("item", item, vault=vault)
        except OPException:
            if vault == None:
                raise NoSuchItemException("Item {} does not exist".format(item))
            raise NoSuchItemException("Item {} does not exist in vault {}".format(item, vault))

    def vault(self, vault):
        return self._get("vault", vault)

class OP2Item(OP2):

    def __init__(self, op2: OP2, item = None, vault = None, withtag = None):
        super().__init__(op2.username, op2.password, op2.secret_key, op2.hostname, op2.session_token)
        
        if item == None:
            self.item = {
                "fields" : []
            } 
        else:
            if withtag == None:
                self.item = super().item(item, vault)
            else:
                debug("searching for {} with tag {}".format(item, withtag))

                self.item = None
                for i in super().items(item, vault):
                    if i["title"] != item:
                        continue
                    if withtag in i["tags"]:
                        self.item = i
                        break
                if self.item == None:
                    if vault == None:
                        raise NoSuchItemException("Item {} does not exist with tag {}".format(item, withtag))
                    else:
                        raise NoSuchItemException("Item {} does not exist with tag {} in vault {}".format(item, withtag, vault))

    @property
    def category(self, cat=None):
        # must be one of Reward Program, Server, Crypto Wallet, Medical Record, Outdoor License, Secure Note, SSH Key, Document, Email Account, Passport, Driver License, Password, Wireless Router, Social Security Number, Software License, Bank Account, Credit Card, Database, Membership, API Credential, Identity, Login.
        if "category" in self.item:
            return self.item["category"]
        if "urls" in self.item:
            return 'Login'
        else:
            return 'Secure Note'


    @property
    def fields(self):
        f = {}
        for field in self.item["fields"]:
            if "id" in field:
                f[field["id"]] = field

        return f

    def save(self):

        if 'id' not in self.item:
            cmd = "op item create "
            cmd += " --category {} ".format(shlex.quote(self.category))

            if 'vault' not in self.item:

                count = 0
                for v in self.vaults():
                    count += 1
                if count > 1:
                    raise NoVaultException("No Vault specified for item, cannot save")
            else:
                    cmd += " --vault {}  ".format(shlex.quote(self.item["vault"]))

        else:

            cmd = "op item edit {} ".format(self.item["id"])
    
        cmd += " --title {} ".format(shlex.quote(self.item["title"]))
        if "urls" in self.item:
            cmd += " --url {} ".format(shlex.quote(self.item["urls"][0]["href"]))

        if "tags" in self.item:
            if type(self.item["tags"]) is list:
                cmd += " --tags {} ".format(shlex.quote(",".join(self.item["tags"])))
            else:
                cmd += " --tags {} ".format(shlex.quote(self.item["tags"]))

        for field in self.item["fields"]:
            if "value" in field:
                cmd += " {}={} ".format(shlex.quote(field['id']), shlex.quote(field["value"]))

        self.signin()

        env2 = os.environ.copy()
        env2[self.session_token[0]] = self.session_token[1]
        env2["OP_ACCOUNT"] = self.username

        debug(cmd)
        out, err, exitcode = run(cmd, env=env2, raise_exception=True)

    def delete(self):
        self._delete("item", self.item["id"])

    def set(self, k, v):
        if k in ("tags", "title", "vault"):
            self.item[k] = v
            return True

        if k == "url":
            self.item["urls"] = [{"href" : v}]
            return

        if "fields" not in self.item:
            self.item["fields"] = []

        for f in self.item["fields"]:
            if f["id"] == k:
                f["value"] = v
                return
        self.item["fields"].append(
            {"id": k, "value": v}
        )

    def get(self, k):
        if k in ("tags", "title"):
            try:
                return self.item[k]
            except KeyError:
                return None

        if "fields" in self.item:
            for f in self.item["fields"]:
                if f["id"] == k:
                    return f["value"]

        return None

def op_signin():
    parser = argparse.ArgumentParser()
    parser.add_argument('--account', default=os.getenv('OP_ACCOUNT'), help='onepassword account')
    parser.add_argument('--password', default=os.getenv('OP_PASSWORD'), help='onepassword password')
    parser.add_argument('--secret-key', default=os.getenv('OP_SECRET_KEY'), help='onepassword secret key')
    parser.add_argument('--hostname', default=os.getenv('OP_HOSTNAME'), help='onepassword hostname')

    args = parser.parse_args()

    o = OP2( args.account, args.password, args.secret_key, args.hostname)
    o.signin()

    print('export {}="{}"'.format(o.session_token[0], o.session_token[1]))

class OP2Vault(OP2):

    def __init__(self, op2: OP2, vault = None):
        super().__init__(op2.username, op2.password, op2.secret_key, op2.hostname, op2.session_token)
        
        if vault == None:
            self.vault = {} 
        else:
            try:
                self.vault = super().vault(vault)
            except OPException:
                raise NoSuchVaultException("Vault {} does not exist".format(vault))

    def delete(self):
        self._delete("vault", self.vault["id"])

    def name(self, name):
        self.vault["name"] = name
        
    @property
    def id(self):
        return self.vault["id"]

    def save(self):

        self.signin()

        if "id" in self.vault:
            cmd = "op vault edit {} --name \"{}\"".format(self.vault["id"], self.vault["name"])
        else:
            cmd = "op vault create  \"{}\"".format(self.vault["name"])

        env2 = os.environ.copy()
        env2[self.session_token[0]] = self.session_token[1]
        env2["OP_ACCOUNT"] = self.username

        debug(cmd)
        out, err, exitcode = run(cmd, env=env2, raise_exception=True)

        if "id" not in self.vault:
            self.vault = super().vault(self.vault["name"]) 

if __name__ == '__main__':
    op_signin()