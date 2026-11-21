"""微博 API 示例（Weibo API in Python）。

  python main.py search 露营装备 --out posts.csv                # 按关键词搜微博 / search posts
  python main.py post <微博 ID> --out post.json                 # 单条微博详情 / post detail
  python main.py comments <微博 ID> --out comments.csv          # 微博评论 / comments
  python main.py user <user_id>                                 # 博主资料 / account profile
  python main.py posts <user_id> --pages 2 --out user_posts.csv # 博主的微博 / an account's posts
"""
import argparse

from everyinfra import fetch, report


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜微博 / search posts by keyword")
    s.add_argument("keyword")
    po = sub.add_parser("post", help="单条微博详情 / one post")
    po.add_argument("url")
    c = sub.add_parser("comments", help="微博评论 / comments of one post")
    c.add_argument("url")
    u = sub.add_parser("user", help="博主资料 / account profile")
    u.add_argument("user_id")
    pos = sub.add_parser("posts", help="博主发布的微博 / an account's posts")
    pos.add_argument("user_id")
    pos.add_argument("--pages", type=int, default=1, help="最多翻几页，每页算一次调用 / max pages, one call each")
    for x in (s, po, c, u, pos):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        rows, charged = fetch("search", {"keyword": a.keyword})
    elif a.cmd == "post":
        rows, charged = fetch("post_detail", {"url": a.url})
    elif a.cmd == "comments":
        rows, charged = fetch("comments", {"url": a.url})
    elif a.cmd == "user":
        rows, charged = fetch("profile", {"user_id": a.user_id})
    else:
        rows, charged = fetch("user_posts", {"user_id": a.user_id}, a.pages)
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
