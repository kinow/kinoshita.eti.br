---
categories:
- blog
date: "2021-10-22T00:00:00Z"
tags:
- opensource
title: Removing invisible unread GitHub notifications
---

<img
src="/assets/posts/{{ page.date | date: "%Y-%m-%d" }}-{{ page.title | slugify }}/notifications.png"
alt="GitHub Notifications icon always-on mode"
class="center-aligned"
/>

Some months ago I noticed that even after I marked all my GitHub notifications
as read, the unread icon displayed at the right top corner was still showing as
if I had unread notifications.

I tried changing the filters, waiting for a new notification to appear so that
I could mark it as read, all hoping that icon would then change. But no matter
what I tried in the GitHub UI, the icon was still there.

Then I opened a ticket with GitHub support and within a couple of days they
replied suggesting me to use their
[REST API](https://docs.github.com/en/rest/reference/activity#mark-notifications-as-read)
to mark notifications as read.
So if you have the same issue, try the following
[code](https://github.com/kinow/dork-scripts/blob/master/github/mark-notifications-as-read.sh):

```bash
# https://docs.github.com/en/rest/reference/activity#mark-notifications-as-read
curl -X PUT \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $TOKEN_GOES_HERE" \
  https://api.github.com/notifications -d '{"last_read_at": "'$(date '+%Y-%m-%dT%H:%M:%SZ')'"}'
```

You will have to create a [token](https://github.com/settings/tokens) and use
it in the command above. Just give it "Notifications" permission, and delete
it after you have used it.
