# Information Flow Graph Design

**Topic-Specific Graph via Hashtag(#) and Mention(@) Reuse**

## Intro

The graph is specific to a single topic, representing interactions within that context.  
It consists of `nodes` representing authors and directed `edges` representing the reuse of entities (hashtags and mentions).  

The graph is built using *Neo4j* graph engine.  

The graph aims to reflect potential influence through shared entities (hashtag, mention) usage.

## Filtering Relevant Interactions
* For visual clarity, only key-authors (authors with high TF-IDF scores) are included in the graph.
* A time window ensures edges reflect timely reuse:
  * Minimum bound `min_time` (in days) to filter out cases when autors use enteties simultaneously.
  * Maximum bound `max_time` (in days) to ensure that only reuse occurring within a relevant timeframe is considered
* A threshold `entities_threshold` (in decimal) is used to ensure that only entities appearing in less than a given proportion of all posts are considered significant. This filters out overly common entities, allowing the graph to focus on rarer, mor meaningful interactions while reducing noise from generic or widely used terms.



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
