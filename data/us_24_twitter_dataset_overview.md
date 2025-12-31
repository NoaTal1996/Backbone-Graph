# US-24 Twitter Dataset (Cleaned)

## Dataset File
**Filename:** `US-24_Fix.zip`  
**Database type:** SQLite  

**Download link:**  
https://tauex-my.sharepoint.com/:f:/g/personal/shimshi_tauex_tau_ac_il/EgSW3Jgsy6NOk8dfgyFTLzgBaf7JeBlJs5Hr6AP7dXPwOg?e=r16QJg

---

## Overview
This dataset contains a **cleaned SQLite database of tweets** related to the United States during **calendar year 2024**.

- All corrupted / malformed rows were removed.
- Total number of tweets: **42,211,159**
- Time range: **2024-01-01 → 2024-12-31**
- The dataset is intended for large-scale temporal, network, and event-driven analysis.

---

## Key Political Events Covered
The dataset spans several major political events in the **2024 US** election cycle:

1. **07-13.01** – Attempted assassination of Donald Trump  
2. **07-21.02** – Joe Biden withdraws from the presidential race  
3. **05-08.03** – Formal nomination of Kamala Harris as the Democratic candidate  
4. **05-11.04** – Election Day  
5. **06-11.05** – Election results announced

---

## Indexes
The SQLite database contains **two indexes**:

- **IDX** – Primary key (unique, auto-increment). Internal identifier added during cleaning.
- **epoch** – Tweet timestamp (Unix epoch time), indexed for fast temporal queries.

---

## Table Schema: `tweets`


```sql
"tweets" (
  "IDX" INTEGER PRIMARY KEY AUTOINCREMENT,  -- Added unique identifier
  "id" INTEGER,
  "text" TEXT,
  "url" TEXT,
  "epoch" INTEGER,
  "media" TEXT,
  "retweetedTweet" INTEGER,
  "retweetedTweetID" INTEGER,
  "retweetedUserID" INTEGER,
  "lang" TEXT,
  "replyCount" INTEGER,
  "retweetCount" INTEGER,
  "likeCount" INTEGER,
  "quoteCount" INTEGER,
  "conversationId" INTEGER,
  "hashtags" TEXT,
  "mentionedUsers" TEXT,
  "links" TEXT,
  "viewCount" TEXT,
  "viewCountNo" INTEGER,
  "quotedTweet" INTEGER,
  "in_reply_to_screen_name" TEXT,
  "in_reply_to_status_id_str" INTEGER,
  "in_reply_to_user_id_str" INTEGER,
  "location" TEXT,
  "cash_app_handle" TEXT,
  "user" TEXT,  -- dictionary, contains multiple attributes
  "date" TEXT,
  "type" TEXT
);
