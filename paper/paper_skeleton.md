# I Can See U: Indicator-Based Information Operation Detection with Topic-Aware Analysis

## Abstract

Information operations are coordinated attempts to shape online discourse by making many accounts act as if they are independent voices while they are actually reinforcing the same narratives. The story of this paper is that suspicious users can be detected by their behavior in the network, not only by the content of their posts. We build a topic-aware behavior graph in which authors are connected when they reuse the same campaign entities, participate in the same narratives, or show similar co-action patterns. The central idea is that IO drivers should appear less like isolated users and more like actors embedded inside dense regions of coordinated activity. Instead of relying on an opaque classifier, the paper focuses on interpretable indicators such as core number and other structural measures that explain why an account looks suspicious.

## 1. Introduction

Social networks make it easy for coordinated actors to amplify narratives, imitate organic discussion, and hide their coordination inside ordinary public conversation. A single post may not look suspicious, and a single user may appear legitimate when viewed alone, but repeated shared behavior across many users can reveal the operation. The paper begins from this intuition: if IO drivers coordinate, then their coordination should leave a visible trace in the relationships between accounts. The goal is therefore to move from isolated posts to a behavior-based view of users, where suspiciousness is explained by an author's position in a topic-aware co-action structure.

## 2. Related Work

Most IO detection work can be understood as choosing where to look for the signal: in text, in timing, in account metadata, in interaction networks, or in learned graph representations. This paper belongs to the coordination and graph-based family, but its emphasis is deliberately simple and interpretable. Rather than treating the graph as a technical input to a black-box model, the graph is the story itself: it shows who acts like whom, which users gather around the same narratives, and which accounts sit in dense regions that are difficult to explain as ordinary independent behavior.

## 3. Methodology

The method turns raw social-media activity into an author-level story. Posts are cleaned, entities such as hashtags, mentions, URLs, and named entities are extracted, and topic modeling is used to organize posts into narratives. Authors are then represented as nodes in a behavior graph, and edges connect authors who share meaningful co-actions inside the same campaign context. Once the graph is built, each author can be described by indicators that measure how connected, central, embedded, or narrative-focused the author is.

### 3.1 Indicator-Based IO Classification

The main indicator story is about dense coordination. IO drivers are expected to be embedded in groups where many accounts repeatedly behave alike, so structural indicators should help distinguish them from ordinary users. Core number is especially intuitive because it measures how deeply a node belongs to a dense subgraph: an author with high core number is not merely connected to many others, but remains inside a mutually connected region after peripheral accounts are peeled away. This makes the feature explainable to an analyst: the account looks suspicious because it belongs to the inner coordination structure, not because a model produced an unexplained score.

### 3.2 Influential IO Drivers Detection

The paper also separates ordinary participation from narrative leadership. Some users simply appear in a topic, while others repeatedly use the entities that define that topic and help drive the discussion. The author-topic key score captures this idea by measuring how strongly an author is associated with topic-specific entities. This creates a topic-aware backbone: first focus on authors who matter to the narratives, then inspect which of them are also structurally embedded in coordinated behavior. The story is that influential IO drivers are suspicious not only because they post, but because they both push narratives and move with others.

### 3.3 Topic-Aware Graph Analysis

Topic awareness gives meaning to the structure. A dense group of accounts is more informative when we can also ask what narrative holds the group together. Topic modeling therefore acts as the bridge between content and structure: it does not replace graph analysis, but it helps explain what the graph is about. In the paper's story, topic-aware analysis lets an analyst move from "these accounts coordinate" to "these accounts coordinate around this campaign narrative," which is a much stronger and more useful interpretation.

## 4. Experiments

The experimental setup is used to demonstrate the story rather than to make this draft a full evaluation paper. The pipeline takes labeled IO datasets, preprocesses posts, extracts entities, assigns topics, builds co-action graphs, computes author indicators, and trains simple classifiers on the author-level feature vectors. The important design choice is that the models are ordinary and the features remain interpretable, so the framework can show why a user is suspicious instead of only predicting that the user is suspicious.

### 4.1 Dataset

The data consists of labeled social-media campaigns containing posts from IO and control accounts. Each post provides the raw material for the story: who posted, when they posted, what entities they used, and which topic or narrative the post belongs to. The author-level label allows the framework to ask whether accounts that participate in coordinated narrative behavior are more likely to be IO drivers.

### 4.2 Baseline

The baseline idea is simple: compare ordinary machine-learning models trained on interpretable author indicators. The point is not to introduce a complex new classifier, but to test whether the graph representation itself carries the IO signal. If simple models can use these indicators, then the main contribution is the representation and the explanation, not model complexity.

### 4.3 Frameworks and Hardware

The implementation is organized as a notebook pipeline that performs preprocessing, translation when needed, entity extraction, topic modeling, key-author scoring, graph construction, indicator computation, and classification. This structure keeps the workflow modular: each step has a clear role in the narrative, from raw posts to topics, from topics to behavior graphs, and from behavior graphs to interpretable suspicious-user indicators.

## 5. Discussion

The core claim is that IO detection should be told as a network story. A suspicious account is not only an account that writes suspicious text; it is an account that repeatedly appears in the same narrative space as other coordinated actors and occupies a dense structural position in the behavior graph. This gives the analyst a chain of reasoning: the account pushes a narrative, reuses campaign entities, connects to similar actors, and belongs to a dense coordination region. That chain is the main value of the approach.

## 6. Conclusion

This paper's idea is that topic-aware graph indicators can make IO detection more interpretable. Topic modeling identifies the narratives, entity reuse connects authors through shared behavior, key-author scoring highlights narrative leaders, and graph indicators reveal which authors are embedded in coordination. The final story is simple: to find IO drivers, look not only at what users say, but at how they move together inside the campaign.
