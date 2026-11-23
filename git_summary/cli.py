import argparse
from .core import get_summary


def render_bar(count, max_count, width=20):
    filled = int((count / max_count) * width) if max_count else 0
    return "█" * filled + "░" * (width - filled)


def main():
    parser = argparse.ArgumentParser(
        description="git-summary: human-readable summary of a Git repository"
    )
    parser.add_argument(
        "--top", type=int, default=5,
        help="Number of top contributors and files to show (default: 5)"
    )
    parser.add_argument(
        "--path", type=str, default=None,
        help="Path to a Git repository (default: current directory)"
    )
    args = parser.parse_args()

    data = get_summary(path=args.path)

    print(f"\n{'='*50}")
    print(f"  Repository : {data['repo_name']}")
    print(f"  Commits    : {data['total_commits']}")
    print(f"  Branches   : {data['branch_count']}")
    print(f"  Recent (30d): {data['recent_commits']} commits")
    print(f"  Busiest day: {data['busiest_day'] or 'N/A'}")

    if data["last_commit"]:
        lc = data["last_commit"]
        print(f"  Last commit: {lc['when']} by {lc['author']}")
        print(f"               \"{lc['message']}\"")

    print(f"\n  Top Contributors:")
    contributors = data["contributors"][: args.top]
    max_commits = contributors[0]["commits"] if contributors else 1
    for c in contributors:
        bar = render_bar(c["commits"], max_commits)
        print(f"    {bar} {c['commits']:>5}  {c['name']}")

    print(f"\n  Most Active Files:")
    if data["most_active_files"]:
        max_file_commits = data["most_active_files"][0][1]
        for filepath, count in data["most_active_files"][: args.top]:
            bar = render_bar(count, max_file_commits)
            print(f"    {bar} {count:>5}  {filepath}")

    print(f"{'='*50}\n")
