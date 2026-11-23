# Weibo API（微博 API）

[English](#english) · [中文](#中文)

## English

This repo reads public Weibo data with Python or curl. You can search posts by keyword, read a single post and its comments, and look up an account's profile and posts. You need one EveryInfra API key. You do not need a Weibo account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $0.56 to $0.81 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra Weibo API has 17 capabilities, all listed on the platform page: <https://everyinfra.com/en/weibo-api?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### Quick start

```bash
git clone https://github.com/everyinfra/weibo-api.git
cd weibo-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search 露营装备 --out posts.csv
python main.py post <post_id> --out post.json
python main.py comments <post_id> --out comments.csv
python main.py user <user_id>
python main.py posts <user_id> --pages 2 --out user_posts.csv
```

- For `post` and `comments`, pass the `id` from a `search` result. It is the numeric post ID.
- For `user` and `posts`, use the numeric `author_id` from a `search` result as `user_id`. Nicknames do not work.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- `--pages N` follows `next_page_token` for N pages. Each page counts as one call.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"weibo","action":"search","params":{"keyword":"露营装备"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `post_detail`, `comments`, `profile`, and `user_posts` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $0.81 |
| `post_detail` | $0.81 |
| `comments` | $0.56 |
| `profile` | $0.56 |
| `user_posts` | $0.81 |

- Billing is per call, about $0.00056 to $0.00081 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- Each page fetched with `--pages` counts as one call.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>
- Prices for the other 12 Weibo capabilities are on the platform page: <https://everyinfra.com/en/weibo-api?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### Fields

These are the fields that the 5 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `device` | Client the post was published from (such as an iPhone client). |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `is_repost` | Whether the post is a repost. |
| `author_id` | Author's unique ID on the platform. |
| `author_name` | Author's display name. |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `video_url` | Video link of the post. |

All parameters and fields: <https://everyinfra.com/en/weibo-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `post_detail` (post details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `device` | Client the post was published from (such as an iPhone client). |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `is_repost` | Whether the post is a repost. |
| `is_long_text` | Whether the post is a long post (post_detail / user_posts). |
| `author_id` | Author's unique ID on the platform. |
| `author_name` | Author's display name. |
| `author_bio` | Author bio. |
| `author_follower_count` | Number of followers the author has. |
| `author_following_count` | Number of accounts the author follows. |
| `author_verified` | Whether the author carries Weibo verification (the V badge). |
| `author_verified_reason` | Verification description (such as a company role); use it to tell what a verified account represents. |
| `author_avatar_url` | Author avatar URL. |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/weibo-api/post_detail?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `comments` (comments)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `author_id` | Author's unique ID on the platform. |
| `author_name` | Author's display name. |
| `author_avatar_url` | Author avatar URL. |
| `post_id` | Post ID. |
| `post_url` | Post link. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/weibo-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `profile` (profile or object details)

| Field | Meaning |
|---|---|
| `user_id` | User's unique ID on the platform. |
| `display_name` | Display name; can differ from username. |
| `url` | Link to the record on the platform. |
| `bio` | Profile bio written by the account; may contain line breaks and emoji. |
| `gender` | Gender. |
| `follower_count` | Followers. null means not disclosed, not 0. |
| `following_count` | Accounts followed. null means not disclosed, not 0. |
| `post_count` | Total posts. null means not disclosed, not 0. |
| `is_verified` | Whether the platform verified the account. null means it cannot be determined. |
| `avatar_url` | Avatar image link. |
| `cover_image_url` | Cover image. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/weibo-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `user_posts` (user content)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `device` | Client the post was published from (such as an iPhone client). |
| `repost_count` | Reposts (as distinct from quote posts). null means not disclosed. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `is_repost` | Whether the post is a repost. |
| `is_long_text` | Whether the post is a long post (post_detail / user_posts). |
| `author_id` | Author's unique ID on the platform. |
| `author_name` | Author's display name. |
| `author_verified` | Whether the author carries Weibo verification (the V badge). |
| `author_avatar_url` | Author avatar URL. |
| `image_urls` | Array of image links in the platform's display order; absent when there are no images. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `next_page_token` | Page token (user_search, user_posts, topic_search, user_post_search, user_album, collection_videos): pass it back unchanged as page_token for the next page. |
| `original_post_id` | For a repost, the ID of the original post (post_detail / user_posts); pass it as `url` to post_detail to read the original. |
| `video_url` | Video link of the post. |
| `duration_sec` | Video length in seconds (video posts on post_detail / user_posts, and video / collection_videos). |
| `duration_seconds` | Duration in seconds. null for content that is not video or audio. |

All parameters and fields: <https://everyinfra.com/en/weibo-api/user_posts?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### FAQ

**Do I need a Weibo account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

**Can I connect the Weibo API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>. An agent can then search Weibo content, read comments, and look up accounts by itself.

**What legal points apply when I use Weibo data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Weibo data can I get?**

The EveryInfra Weibo API has 17 capabilities:

- keyword search
- profile or object details
- comments
- trending list
- post details
- user content
- account search
- reposts
- comment replies
- topic search
- user post search
- video details
- user album
- collection videos
- video collections
- region codes
- trending boards

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/weibo-api?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search 露营装备 --out posts.csv` | 2026-11-21 09:29 | 20 | $0.000806 |
| `python main.py post <post_id> --out post.json` | 2026-11-21 09:29 | 1 | $0.000806 |
| `python main.py comments <post_id> --out comments.csv` | 2026-11-21 09:29 | 20 | $0.000556 |
| `python main.py user <user_id>` | 2026-11-21 09:30 | 1 | $0.000556 |
| `python main.py posts <user_id> --pages 2 --out user_posts.csv` | 2026-11-21 09:41 | 42 | $0.001612 |

## 中文

本仓库用 Python 或 curl 读微博公开数据：按关键词搜微博，读单条微博详情和评论，查博主资料和他发布的微博。只需一把 EveryInfra API Key，不用微博账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $0.56 到 $0.81，失败和空结果不收费。微博共 17 个能力：<https://everyinfra.com/weibo-api?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/weibo-api.git
cd weibo-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search 露营装备 --out posts.csv
python main.py post <微博 ID> --out post.json
python main.py comments <微博 ID> --out comments.csv
python main.py user <user_id>
python main.py posts <user_id> --pages 2 --out user_posts.csv
```

- `post` 和 `comments` 传 `search` 结果里的 `id`，就是数字微博 ID。
- `user` 和 `posts` 的 `user_id` 用 `search` 结果里的 `author_id`（数字 UID），不能用昵称。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- `--pages N` 按 `next_page_token` 翻页，每翻一页算一次调用。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"weibo","action":"search","params":{"keyword":"露营装备"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`post_detail`、`comments`、`profile`、`user_posts` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $0.81 |
| 内容详情 | `post_detail` | $0.81 |
| 评论 | `comments` | $0.56 |
| 主页或对象详情 | `profile` | $0.56 |
| 用户内容 | `user_posts` | $0.81 |

- 按调用次数计费，每次约 $0.00056 到 $0.00081；失败、空结果、参数错误和鉴权失败都不收费。
- `--pages` 翻的每一页算一次调用。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>
- 微博其他 12 个能力的单价见平台页 <https://everyinfra.com/weibo-api?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `device` | 发布设备（如「iPhone客户端」）。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `comment_count` | 评论数。 |
| `like_count` | 点赞数。 |
| `is_repost` | 是否为转发。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `image_urls` | 图片列表；不带图的微博没有。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `video_url` | 视频链接；不是视频微博时没有。 |

完整参数和字段：<https://everyinfra.com/weibo-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `post_detail`（内容详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `device` | 发布设备（如「iPhone客户端」）。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `comment_count` | 评论数。 |
| `like_count` | 点赞数。 |
| `is_repost` | 是否为转发。 |
| `is_long_text` | 是不是长微博（post_detail / user_posts）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_bio` | 作者简介；作者没填时没有。 |
| `author_follower_count` | 作者粉丝数。 |
| `author_following_count` | 作者关注数。 |
| `author_verified` | 作者是否加 V。 |
| `author_verified_reason` | 认证说明（如「XX公司CEO」），判断大V身份靠它；没认证时没有。 |
| `author_avatar_url` | 作者头像。 |
| `image_urls` | 图片列表；不带图的微博没有。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/weibo-api/post_detail?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `comments`（评论）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `like_count` | 点赞数。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_avatar_url` | 作者头像。 |
| `post_id` | 微博 ID。 |
| `post_url` | 微博链接。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/weibo-api/comments?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `profile`（主页或对象详情）

| 字段 | 含义 |
|---|---|
| `user_id` | 用户在原平台的唯一 ID。 |
| `display_name` | 显示名，可能与 username 不同。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `bio` | 个人简介，账号自己填写的文本。 |
| `gender` | 性别。 |
| `follower_count` | 粉丝数。 |
| `following_count` | 关注数。 |
| `post_count` | 这个用户发过的微博数（likers、following_list、followers_list）。 |
| `is_verified` | 是否为平台认证账号（蓝V等）。 |
| `avatar_url` | 头像图片链接。 |
| `cover_image_url` | 封面图。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/weibo-api/profile?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

#### `user_posts`（用户内容）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `device` | 发布设备（如「iPhone客户端」）。 |
| `repost_count` | 转发数（区别于引用转发）。 |
| `comment_count` | 评论数。 |
| `like_count` | 点赞数。 |
| `is_repost` | 是否为转发。 |
| `is_long_text` | 是不是长微博（post_detail / user_posts）。 |
| `author_id` | 作者在原平台的唯一 ID。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_verified` | 作者是否加 V。 |
| `author_avatar_url` | 作者头像。 |
| `image_urls` | 图片列表；不带图的微博没有。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `next_page_token` | 翻页令牌（user_search、user_posts、topic_search、user_post_search、user_album、collection_videos）：作为下一次请求的 page_token 原样传回取下一页；同一页每行的值相同，响应顶层也有同一个 next_page_token。 |
| `original_post_id` | 转发微博时，被转发的原微博 ID（post_detail / user_posts）；可作为 post_detail 的 url 传入读原微博。 |
| `video_url` | 视频链接；不是视频微博时没有。 |
| `duration_sec` | 视频时长（秒；post_detail、user_posts、video、collection_videos、video_feed 的视频微博）。 |
| `duration_seconds` | 时长，单位秒。 |

完整参数和字段：<https://everyinfra.com/weibo-api/user_posts?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### 常见问题

**调用时要不要提供微博账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

**能把微博接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>。Agent 能自己搜微博内容、读评论、查账号。

**用微博数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到微博的哪些数据？**

微博有 17 个能力：关键词搜索、主页或对象详情、评论、热榜、内容详情、用户内容、账号搜索、转发列表、评论回复、话题搜索、在用户微博里搜索、视频详情、用户相册、合集里的视频、用户的视频合集、地区表、热搜榜单列表。每个能力的参数和返回字段见平台页 <https://everyinfra.com/weibo-api?utm_source=github&utm_medium=example_repo&utm_campaign=weibo-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search 露营装备 --out posts.csv` | 2026-11-21 09:29 | 20 | $0.000806 |
| `python main.py post <微博 ID> --out post.json` | 2026-11-21 09:29 | 1 | $0.000806 |
| `python main.py comments <微博 ID> --out comments.csv` | 2026-11-21 09:29 | 20 | $0.000556 |
| `python main.py user <user_id>` | 2026-11-21 09:30 | 1 | $0.000556 |
| `python main.py posts <user_id> --pages 2 --out user_posts.csv` | 2026-11-21 09:41 | 42 | $0.001612 |

`post_detail` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "5365823519850744",
  "text": "#尚界Z7T星野套装门店抢先曝光# 尚界Z7T星野套装11月16日起展车陆续到店，11月20日正式发布。余总也发微博聊了…",
  "posted_at": "2026-11-16T02:18:01+00:00",
  "repost_count": 89,
  "comment_count": 170,
  "like_count": 265
}
```

## License

MIT
