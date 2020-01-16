import click
import requests

HOST = "http://localhost:3000"


class SDK:
    s: requests.Session

    def __init__(self):
        self.s = requests.Session()

    def login(self, phone, password):
        path = "/login/cellphone"
        r = self.s.get("{host}{path}?phone={phone}&password={password}".format(host=HOST,
                                                                               path=path,
                                                                               phone=phone,
                                                                               password=password))
        # todo add check status code
        r.raise_for_status()
        self.self = r.json()

    def follow(self, uid=None):
        if uid is None:
            uid = self.self["account"]["id"]

        path = "/user/followeds"
        r = self.s.get("{host}{path}?uid={uid}".format(host=HOST,
                                                       path=path,
                                                       uid=uid))
        r.raise_for_status()
        print(self.self["profile"]["nickname"], self.self["profile"]["userId"])
        print("-------")
        for user in r.json()["followeds"]:
            print(user["nickname"], user["userId"])

    def create_playlist(self, name, is_privacy=True):
        params = "name=" + name
        if is_privacy:
            params += "&privacy=10"
        path = "/playlist/create"
        r = self.s.get("{host}{path}?{params}".format(host=HOST,
                                                      path=path,
                                                      params=params))
        r.raise_for_status()
        return r.json()

    def record(self, uid=None, week=False, all=False):
        if uid is None:
            uid = self.self["account"]["id"]
        params = "uid={}".format(uid)
        if week:
            params += "&type=1"
        if all:
            params += "&type=2"
        path = "/user/record"
        r = self.s.get("{host}{path}?{params}".format(host=HOST,
                                                      path=path,
                                                      params=params))
        r.raise_for_status()
        return r.json()

    def add2list(self, pid, tracks):
        params = "op=add&pid={pid}&tracks={tracks}".format(pid=pid, tracks=tracks)
        path = "/playlist/tracks"
        r = self.s.get("{host}{path}?{params}".format(host=HOST,
                                                      path=path,
                                                      params=params))
        print(r.text)
        r.raise_for_status()


@click.group()
@click.option('-u', '--user', required=True, help='user')
@click.option('-p', '--password', required=True, help='password.')
def cli(user, password):
    sdk.login(user, password)


@cli.command("follow")
def follow():
    sdk.follow()


@cli.command("union")
@click.argument('uid')
@click.option("--debug", default=False, is_flag=True, help='DEBUG')
def union_cmd(uid, debug=False, create=True):
    union = []
    record_self = sdk.record(week=True)
    song_set = set()
    if debug:
        print("record_self")
    for m in record_self["weekData"]:
        song_set.add(m["song"]["id"])
        if debug:
            print(m["song"]["id"], m["song"]["name"], "@" + ",".join(map(lambda x: x["name"], m["song"]["ar"])),
                  "   >>[" + m["song"]["al"]["name"] + "]<<")

    record_other = sdk.record(uid, week=True)
    if debug:
        print("record_other")
    for m in record_other["weekData"]:
        if m["song"]["id"] in song_set:
            union.append(m)
        if debug:
            print(m["song"]["id"], m["song"]["name"], "@" + ",".join(map(lambda x: x["name"], m["song"]["ar"])),
                  "   >>[" + m["song"]["al"]["name"] + "]<<")

    print("union")
    for m in union:
        print(m["song"]["id"], m["song"]["name"], "@" + ",".join(map(lambda x: x["name"], m["song"]["ar"])),
              "   >>[" + m["song"]["al"]["name"] + "]<<")

    if create:
        pid = sdk.create_playlist("union" + uid)["id"]
        sdk.add2list(pid, ",".join(map(lambda x: str(x["song"]["id"]), union)))


if __name__ == "__main__":
    sdk = SDK()
    cli()
