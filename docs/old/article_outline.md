# Detecting Coordinated Information Operations via Topic-Aware Influence, Behavioral Similarity Graphs, and Core-Periphery Analysis

## 1. Introduction (Definitions & Terms)

### Information Operations (IO)  
Information Operations (IO) refer to coordinated efforts by groups of accounts to influence discourse, typically around specific topics and target audiences.

### Graph Representation  
We model the social network as a graph:
- Nodes represent users/accounts  
- Edges represent co-action\behavioral similarity (e.g., retweets, mentions, replies)  

### K-Core 
The **k-core indicator** identifies densely connected subgraphs:
- Higher k-core → more structurally central and cohesive  
- Lower k-core → more peripheral  

### Key-Score  
A **topic-aware influence score**:
- Measures how much an author influences a specific topic.
- Captures targeted impact.

---

## 2. Hypothesis  

We hypothesize that IO actors exhibit two complementary properties:

1. **Structural Coordination**  
   IO actors are highly connected and tend to cluster in dense regions of the graph.

2. **Core Concentration**  
   IO actors are more likely to appear in **higher k-core regions**.

3. **Topic-Driven Influence**  
   IO actors are not only coordinated but also **focused on influencing specific topics**, which is captured by Key-Score.

4. **Distributional Anomaly**  
   In a natural network:
   - The k-core distribution typically follows a smooth decay (e.g., exponential-like).

   In the presence of IO:
   - IO nodes concentrate in higher cores  
   - This creates an **unnatural bump** in the distribution  
   - Lower cores remain mostly unaffected  

Therefore:
- High k-core regions are **disproportionately influenced**


#### k-shell
We may prefer using k-shell instead of k-core because it puts each node in just one group, making it easier to spot unusual “bumps” in the higher levels where IO actors tend to gather.
In k-shell, each node is placed only in the shell where it gets removed during the decomposition process.
---

## 3. Approach A: Key Filtering → Core Filtering  

### Steps:
1. Compute **KeyScore** for all authors
2. Select authors with **high KeyScore**
3. Build backbone graph from the selected authors.
4. Select authors\nodes with **high k-core**  on this subset.
5. Build a new grpah from the selected authors\nodes.

### Rationale:
- First identify nodes that are influential on a topic  
- Then check if they are also structurally coordinated

---

## 4. Approach B: Core Filtering → Key Filtering  

### Steps:
1. Build backbone graph.
2. Compute **k-core** for all authors\nodes 
3. Select authors\nodes with **high k-core**
4. Compute **key score** for the selected authors
5. Build a new grpah from the selected authors\nodes.
 

### Rationale:
- First identify structurally coordinated
- Then detect which nodes are actively influencing topics  

---

## 5. Approach C: Clustering + Core Distribution Analysis  

### Steps:
1. Build backbone graph.
2. Perform **community detection (clustering)**  
3. For each cluster:
   - Compute the **average k-core value**  
4. Analyze the **distribution of average k-core across clusters**
5. Look for "bumps" in the distribution.
6. Anelize the bump using approach a or approach b.


### Distribution Hypothesis  

**Distribution = average k-core across communities/clusters.**

The distribution is expected to behave as follows:

- In a natural network:  
  - The distribution of k-core values follows a **smooth decay** (e.g., Exponential distribution)  

- In the presence of IO:  
  - IO actors form a **dense core**  
  - This creates a **non-natural concentration in higher k-core regions**  
  - Many IO nodes are grouped in these high-core clusters -  a "bump.  

This results in:
- A deviation from the expected distribution  
- A detectable structural anomaly  

---

## 6. Summary  

We propose three complementary approaches:

- **Approach A:** Focus on influence first, then coordinatnation
- **Approach B:** Focus on coordinatnation first, then influence  
- **Approach C:** Detect global anomalies via clustering and core distribution  

Together, they provide:
- Node-level detection (who are the IO actors)  
- Network-level detection (whether and where IO activity exists)  
