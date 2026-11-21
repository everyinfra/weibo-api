#!/usr/bin/env bash
# 微博 API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Weibo API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search 露营装备
#   bash examples/curl.sh post_detail <post_id> # search 结果里的 id / the id from a search result
#   bash examples/curl.sh comments <post_id>
#   bash examples/curl.sh profile <user_id>     # search 结果里的 author_id / the author_id from a search result
#   bash examples/curl.sh user_posts <user_id>
#
# 翻页：把响应里的 next_page_token 放进 params.page_token 再调一次，每页算一次调用。
# Next page: send the response's next_page_token back as params.page_token. Each page is one call.
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|post_detail|comments|profile|user_posts> <value>"}
value=${2:?"value: a keyword, a post id or a user_id"}

case "$action" in
  search)                 params="{\"keyword\":\"$value\"}" ;;
  post_detail | comments) params="{\"url\":\"$value\"}" ;;
  profile | user_posts)   params="{\"user_id\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, post_detail, comments, profile or user_posts)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"weibo\",\"action\":\"$action\",\"params\":$params}"
echo
