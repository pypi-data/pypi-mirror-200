
import crocodile.toolbox as tb
import argparse
import platform
from machineconfig.utils.utils import print_programming_script, CONFIG_PATH
# import sys
# import subprocess


def args_parser():
    parser = argparse.ArgumentParser(description="Secure Repo CLI.")

    parser.add_argument("repo", help="repo root")

    parser.add_argument("--cloud", "-c", help="rclone cloud profile name.", default=None)
    parser.add_argument("--message", "-m", help="Commit Message", default=f"new message {tb.randstr()}")
    parser.add_argument("--key", "-k", help="Key for encryption", default=None)
    parser.add_argument("--pwd", "-p", help="Password for encryption", default=None)
    parser.add_argument("--push", "-u", help="Zip before sending.", action="store_true")  # default is False

    args = parser.parse_args()

    if args.cloud is None:
        _path = tb.P.home().joinpath("dotfiles/config/setup/rclone_remote")
        try: cloud = _path.read_text().replace("\n", "")
        except FileNotFoundError:
            print(f"No cloud profile found @ {_path}, please set one up or provide one via the --cloud flag.")
            return ""
    else: cloud = args.cloud
    # if args.repo is None:
    #     repo_root = tb.P(".").absolute()
    # else:
    repo_root = tb.P(args.repo).expanduser().absolute()
    repo = tb.install_n_import("git", "gitpython").Repo(repo_root)
    CONFIG_PATH.joinpath("remote").create()
    repo_sync = CONFIG_PATH.joinpath("remote", repo_root.rel2home())
    try:
        print("\n", "=============================== Downloading Remote Repo ====================================")
        repo_root.from_cloud(cloud=cloud, localpath=repo_sync, unzip=True, decrypt=True, rel2home=True, key=args.key, pwd=args.pwd, os_specific=False)
    except AssertionError:
        print("Remote does not exist, creating it and exiting ... ")
        repo_root.to_cloud(cloud=cloud, zip=True, encrypt=True, rel2home=True, key=args.key, pwd=args.pwd, os_specific=False)
        return ""
    script = f"""
echo ""
echo "=============================== Committing Local Changes ==================================="
cd {repo_root}
git status
git add .
git commit -am "{args.message}"
echo ""
echo ""
echo "=============================== Pulling Latest From Remote ================================"
cd {repo_root}
echo 'trying to removing originEnc remote if it exists.'
git remote remove originEnc
echo 'adding originEnc remote.'
git remote add originEnc {repo_sync}
echo 'fetching originEnc remote.'
git pull originEnc master

"""
    suffix = '.ps1' if platform.system() == 'Windows' else '.sh'
    res = tb.Terminal().run(f". {tb.P.tmpfile(suffix=suffix).write_text(script)}", shell="powershell").capture().print()
    if res.is_successful(strict_err=True, strict_returcode=True):
        print("\n", "Pull succeeded, removing originEnc, the local copy of remote & pushing merged repo_root to remote ... ")
        repo_sync.delete(sure=True)
        from git.remote import Remote
        Remote.remove(repo, "originEnc")
        if args.push:
            repo_root.to_cloud(cloud=cloud, zip=True, encrypt=True, rel2home=True, key=args.key, pwd=args.pwd, os_specific=False)
    else:
        print(f"Failed to pull, keeping local copy of remote at {repo_sync} ... ")
        program = f"""
# Finalizing syncing of `{repo_root}` to `{cloud}` by pushing local changes to remote and deleting local copy of remote.
repo_sync = tb.P(r'{repo_sync}')
repo_root = tb.P(r'{repo_root}')
repo_sync.delete(sure=True)
from git.remote import Remote
from git import Repo
try: Remote.remove(Repo(repo_root), "originEnc")
except: pass
repo_root.to_cloud(cloud={cloud}, zip=True, encrypt=True, rel2home=True, os_specific=False)
"""
        print_programming_script(program, lexer="py", desc="Abstaining from running the following autmomatically:")
        resp = input("Would you like to run the above commands? [y]/n ") or "y"
        if resp.lower() == "y":
            repo_sync.delete(sure=True)
            from git.remote import Remote
            from git import Repo
            try: Remote.remove(Repo(repo_root), "originEnc")
            except: pass
            repo_root.to_cloud(cloud=cloud, zip=True, encrypt=True, rel2home=True, os_specific=False)
        else:
            print(f"When ready, use this snippet: \n{program}")


if __name__ == "__main__":
    args_parser()
