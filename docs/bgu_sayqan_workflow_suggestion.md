# BGU  sayqan workflow Suggestion

## Main Idea
Build features from a **discussion**.
Features can be extracted at:
- **Discourse level**
- **Node (account) level**

For each **account**, we construct a **feature vector**.


## Workflow

### 1. Feature Extraction from Data

#### Sayqan (Content & Temporal Signals)
- **Flow**
  - Post rate
  - Activity spikes
- **NLP**
  - Sentiment analysis
  - Language patterns
  - Stance detection
  - Polarity

#### CBG (Graph-Based Features)
- **Graph Metrics**
  - Centralities (e.g., degree, betweenness, eigenvector)
  - k-core / core number

---

### 2. Feature Presentation
- Present features for user withe thire standard deviation.

---

### 3. Classification
- Train a classifier using **XGBoost**

---

## Output
- A unified **feature vector per account**
- Predicted class / label for each account
