# Information Flow Graph Design

**Topic-Specific Graph via Hashtag(#) and Mention(@) Reuse**

## Intro

The graph is specific to a single topic, representing interactions within that context.  
It consists of `nodes` representing authors and directed `edges` representing the reuse of hashtags and mentions.  
For visual clarity, only key-authors (authors with high TF-IDF scores) are included in the graph.  
A time window `w` (in days) ensures edges reflect timely hashtag or mention reuse, capturing relevant influence.  
The graph is built using *Neo4j* graph engine.  

The graph aims to reflect potential influence through shared entities (hashtag, mention) usage.

## Nodes

Each node represents a single key-author (user) participating in the topic.

#### **Node Properties:**

| Property         | Type         | Description |
|------------------|--------------|-------------|
| `username`       | String       | Author's unique handle |
| `tfidf_score`    | Float        | TF-IDF score of the author for this topic |
| `num_posts`      | Integer      | Total number of posts the author made on this topic |
| `hashtags`       | JSON String  | `{ "#hashtag1": count, "#hashtag2": count, ... }` |
| `mentions`       | JSON String  | `{ "@mentions": count, "@mentions": count, ... }` |
| `top_topics`     | JSON String  | `{ "topicA": frequency, "topicB": frequency, ... }` |

## Edges

An edge from `Author A → Author B` means that, within a sliding time window of `w` days, `Author B` used at least one hashtag *after* `Author A` used it. 

#### **Edge Properties:**

| Property                 | Type    | Description |
|--------------------------|---------|-------------|
| `shared_entity_count`    | Integer | Number of shared hashtags and mentions within the time window |
| `shared_hashtags`        | List    | Hashtags reused within the time window |
| `shared_mentions`        | List    | Mentions reused within the time window |
