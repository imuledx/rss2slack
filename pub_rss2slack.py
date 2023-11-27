#!/usr/bin/python3
import requests
import feedparser
import time
import json
import os

# List of RSS Feed URLs
rss_feeds = ["https://grahamcluley.com/feed/",
"https://rss.packetstormsecurity.com/",
"https://threatpost.com/feed/",
"https://krebsonsecurity.com/feed/",
"https://www.darkreading.com/rss.xml",
"http://feeds.feedburner.com/eset/blog",
"https://davinciforensics.co.za/cybersecurity/feed/",
"https://blogs.cisco.com/security/feed",
"https://www.infosecurity-magazine.com/rss/news/",
"http://feeds.feedburner.com/GoogleOnlineSecurityBlog?format=xml",
"http://feeds.trendmicro.com/TrendMicroResearch",
"https://www.bleepingcomputer.com/feed/",
"https://www.proofpoint.com/us/rss.xml",
"http://feeds.feedburner.com/TheHackersNews?format=xml",
"https://www.schneier.com/feed/atom/",
"https://www.binarydefense.com/feed/",
"https://securelist.com/feed/",
"https://research.checkpoint.com/feed/",
"https://www.virusbulletin.com/rss",
"https://modexp.wordpress.com/feed/",
"https://www.tiraniddo.dev/feeds/posts/default",
"https://blog.xpnsec.com/rss.xml",
"https://msrc-blog.microsoft.com/feed/",
"https://www.recordedfuture.com/feed",
"https://www.sentinelone.com/feed/",
"https://redcanary.com/feed/",
"https://cybersecurity.att.com/site/blog-all-rss",
"https://www.cisa.gov/uscert/ncas/alerts.xml",
"https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml",
"https://www.cisecurity.org/feed/advisories"
]

# Slack Webhook URL
webhook_url = "YOUR SLACK WEBHOOK"

# Text file to keep track of already submitted events
state_file = "/root/rss_feed_to_slack_webhook_python3/state.txt"

# Time interval to check for new events (in seconds)
interval = 1800

# Maximum age of events to submit (in days)
max_age = 1


# Create the text file if it doesn't exist
if not os.path.exists(state_file):
    open(state_file, 'w').close()


# Check for new events
while True:
    state_entries = set()
    # Read the text file and store the entries in a set
    with open(state_file, 'r') as f:
        for line in f:
            state_entries.add(line.lower().strip('\n'))

    for rss_feed in rss_feeds:
        # Parse the RSS Feed
        feed = feedparser.parse(rss_feed)

        # Iterate over the events
        for entry in feed.entries:
            # Check if the event is already submitted
            url = entry.link.lower()
            
            if url in state_entries:
                pass
            else:
                # Check if the event is not too old
                try:
                    if (time.time() - time.mktime(entry.published_parsed)) < (max_age * 86399):
                        # Submit the event to the webhook
                        data = {
                        "text": f"<{entry.link}|{entry.title}>\nSource: {feed.feed.title} on {feed.date}"
                        }
                        
                        response = requests.post(
                            webhook_url, data=json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                        )
                        if response.status_code == 200:
                            # Add the event to the state file
                            with open(state_file, "a") as f:
                                f.write(entry.link + "\n")
                            print("Event submitted: " + entry.title)
                        else:
                            print("An error occurred while submitting the event: " +
                                  entry.title)
                except:
                    pass
    # Wait for the interval
    f.close()
    state_entries.clear()
    time.sleep(interval)

