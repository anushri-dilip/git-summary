import subprocess
from collections import Counter


def run_git(args, path=None):
    cmd = ["git"]
    if path:
        cmd += ["-C", path]
    cmd += args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def get_repo_name(path=None):
    remote = run_git(["remote", "get-url", "origin"], path)
    if remote:
        return remote.rstrip("/").split("/")[-1].replace(".git", "")
    return run_git(["rev-parse", "--show-toplevel"], path).split("/")[-1]


def get_total_commits(path=None):
    out = run_git(["rev-list", "--count", "HEAD"], path)
    return int(out) if out.isdigit() else 0


def get_contributors(path=None):
    out = run_git(["shortlog", "-sn", "--all"], path)
    contributors = []
    for line in out.splitlines():
        parts = line.strip().split("\t", 1)
        if len(parts) == 2:
            contributors.append({"name": parts[1], "commits": int(parts[0])})
    return contributors


def get_most_active_files(path=None, top_n=5):
    out = run_git(["log", "--pretty=format:", "--name-only"], path)
    files = [f for f in out.splitlines() if f.strip()]
    counter = Counter(files)
    return counter.most_common(top_n)


def get_last_commit(path=None):
    out = run_git(["log", "-1", "--pretty=format:%ar|%an|%s"], path)
    if "|" in out:
        when, author, message = out.split("|", 2)
        return {"when": when, "author": author, "message": message}
    return None


def get_busiest_day(path=None):
    out = run_git(["log", "--pretty=format:%ad", "--date=format:%A"], path)
    days = [d for d in out.splitlines() if d.strip()]
    if not days:
        return None
    return Counter(days).most_common(1)[0][0]


def get_commit_activity(days=30, path=None):
    out = run_git(["log", f"--since={days} days ago", "--pretty=format:%ad", "--date=format:%Y-%m-%d"], path)
    dates = [d for d in out.splitlines() if d.strip()]
    return len(dates)


def get_branch_count(path=None):
    out = run_git(["branch", "-a"], path)
    branches = [b for b in out.splitlines() if b.strip()]
    return len(branches)


def get_summary(path=None):
    return {
        "repo_name": get_repo_name(path),
        "total_commits": get_total_commits(path),
        "contributors": get_contributors(path),
        "most_active_files": get_most_active_files(path),
        "last_commit": get_last_commit(path),
        "busiest_day": get_busiest_day(path),
        "recent_commits": get_commit_activity(30, path),
        "branch_count": get_branch_count(path),
    }
