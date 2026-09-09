# Iran_1: Shared-hashtag and coordination report

Prepared: September 8, 2026. Scope: saved 15-minute and 1-hour peak-window results.

## Main finding

The strongest observed pattern is repeated synchronized amplification: **the same 13 accounts reposted the same 15 source posts between the recorded times 13:07 and 13:10 on December 2, 2017**. These 195 distinct posts cover several political and news subjects. Each source post appears once per participating account, and its 13 reposts have matching recorded minutes.

This is evidence consistent with coordinated reposting or a shared automated distribution process. It does not establish direct communication, common ownership, or the identity of an organizer. The political content is predominantly U.S.-focused, despite the dataset name Iran_1.

## Technical setup and scope

- **Dataset:** `Iran_1_part_all`.
- **Graph:** Step-3 account graph for `BERTopic_topic_256`, with `top_percentage=100`.
- **Subgroup selection:** the connected highest-k-core component containing the selected top-core author, **including that author**. The subgroup contains **312 accounts**.
- **Time aggregation:** fixed, non-overlapping pandas time bins. The start is inclusive and the end is exclusive: `[start, end)`.
- **Peak selection:** for each hashtag used by at least two distinct subgroup authors in a window, calculate `n × (n − 1) / 2`; sum across hashtags. Select the highest-scoring window, breaking ties by summed author–hashtag uses and then earliest start.
- **Post selection:** all subgroup posts in the winning window, including posts without shared hashtags. No 100-post truncation is applied. There is no additional topic filter on exported posts.
- **Time interpretation:** timestamps below are exactly as stored. The exported CSVs do not specify a timezone; no timezone conversion is assumed. The central burst has minute-resolution timestamps.
- **Folder naming:** the saved 1-hour folder is `time_delta_h` because pandas normalized `1h` to `h`. The 15-minute folder is `time_delta_15min`.

## Results

| Measure | 15-minute window | 1-hour window |
| --- | --- | --- |
| Date | 2017-12-02 | 2017-12-02 |
| Start, inclusive | 13:00:00 | 13:00:00 |
| End, exclusive | 13:15:00 | 14:00:00 |
| Time delta | 15 minutes (`15min`) | 1 hour (`1h`) |
| Exported posts | 244 | 256 |
| Distinct active authors | 15 | 18 |
| Total subgroup authors | 312 | 312 |
| Reposts | 242 | 242 |
| Non-reposts | 2 | 14 |
| Posts containing a shared hashtag | 101 | 101 |
| Shared hashtags | 30 | 30 |
| Summed distinct-author counts across shared hashtags | 381 | 381 |
| Shared-author-pair score | 2,232 | 2,232 |

The 15-minute interval contains **95.3%** of the posts in the selected hour. Extending to one hour adds 12 non-reposts and three active authors, but does not change the shared-hashtag score. The two windows overlap and are not independent confirmations.

### Top 10 words

Counts are token occurrences across **all exported translated posts**, including repeated reposts. The pipeline lowercases text, removes URLs, mentions, hashtags and `<url>`/`<user>` placeholders, retains ASCII letters, and removes WordCloud stopwords. These are descriptive frequencies, not distinct-author counts or measures of narrative importance. The token `s` is a tokenization artifact, likely from apostrophes/possessives, and is retained here to reproduce the saved output.


#### 15-minute window

| word | count |
| --- | --- |
| trump | 77 |
| roy | 52 |
| moore | 52 |
| weinstein | 52 |
| s | 51 |
| carmen | 39 |
| cruz | 26 |
| hall | 26 |
| twitter | 26 |
| colbert | 26 |


#### 1-hour window

| word | count |
| --- | --- |
| trump | 78 |
| s | 54 |
| roy | 52 |
| moore | 52 |
| weinstein | 52 |
| carmen | 39 |
| scandal | 26 |
| impeach | 26 |
| yul | 26 |
| mayor | 26 |


### Top 10 hashtags

Counts represent the number of exported posts containing each normalized hashtag: lowercase, without the leading `#`, counted at most once per post. **Fourteen hashtags tie at 26 posts each in both windows.** The tables reproduce the first ten rows in each saved CSV; differences in their order do not imply differences in importance. All 14 tied hashtags were used by 13 distinct authors each.


#### 15-minute window

| hashtag | count |
| --- | --- |
| roymoore | 26 |
| harassment | 26 |
| middleclass | 26 |
| taxbill | 26 |
| mooresenate | 26 |
| moore | 26 |
| weinsteinscandal | 26 |
| weinstein | 26 |
| spacey | 26 |
| roymoorechildmolester | 26 |


#### 1-hour window

| hashtag | count |
| --- | --- |
| taxreform | 26 |
| taxcuts | 26 |
| taxcut | 26 |
| taxbill | 26 |
| middleclass | 26 |
| harassment | 26 |
| taxscambill | 26 |
| weinstein | 26 |
| spacey | 26 |
| roymoorechildmolester | 26 |


The complete tied set is: `roymoore`, `harassment`, `middleclass`, `taxbill`, `mooresenate`, `moore`, `weinsteinscandal`, `weinstein`, `spacey`, `roymoorechildmolester`, `taxscambill`, `taxreform`, `taxcut`, and `taxcuts`. Hashtag wording describes the posts' framing; allegations embedded in hashtags are not adopted as factual findings.

## Coordination evidence

### Repeated participation by the same accounts

A check against the Step-3 parquet, including `postid`, `post_text`, `is_repost`, `reposted_postid`, and `application_name`, confirmed:

- **13 identical participating accounts** across **15 messages**.
- **195 distinct post IDs**, comprising 15 original-text values and 15 reposted source IDs.
- All 195 posts are explicitly marked as reposts.
- All use the same recorded application identifier. This is compatible with a shared posting mechanism, but a common client alone does not establish common control.
- The burst represents **79.9% of the 15-minute window** and **76.2% of the hour's posts**.

| Recorded timestamp on 2017-12-02 | Reposts in this repeated set | Distinct authors | Distinct source messages |
| --- | --- | --- | --- |
| 13:07:00 | 52 | 13 | 4 |
| 13:08:00 | 65 | 13 | 5 |
| 13:09:00 | 65 | 13 | 5 |
| 13:10:00 | 13 | 13 | 1 |
| Total | 195 | 13 across the burst | 15 |

This repeated account–message pattern is more informative than a single popular hashtag: the same accounts redistribute multiple messages at matching recorded minutes. These messages include both hashtagged and non-hashtagged posts; the 195-post burst should not be confused with the 101 posts containing shared hashtags.

**Interpretation:** a strong descriptive signal of synchronized amplification, suitable for follow-up investigation. No null-model test or comparison with similarly active outside accounts has yet been performed, so statistical significance and abnormality relative to a baseline remain unestablished.

## Narratives observed

The following themes are interpretations of the saved translated text, supported by repeated messages and hashtag use. They are not independent fact checks of the posts' claims.

| Theme | Evidence in the selected windows | Reading |
| --- | --- | --- |
| Criticism of Trump and calls for impeachment | Repeated messages about an impeachment vote, Tom Steyer's petition, and criticism of the administration; `trump` is the most frequent word. | Anti-Trump political amplification. |
| U.S. tax policy | `taxscambill`, `taxreform`, `taxbill`, `taxcut`, `taxcuts`, and `middleclass`; repeated messages mentioning political cartoonists. | Tax-policy debate, including explicitly critical framing through `taxscambill`. |
| Sexual misconduct and political controversy | Roy Moore, Weinstein and Spacey-related hashtags, plus repeated scandal-themed messages. | Linking misconduct controversies with political discussion. |
| Trump–Russia investigation | Repeated messages on Flynn's guilty plea, Mueller, and a proposed investigation involving the NRA. | Amplification of investigation-related news and claims. |
| Carmen Yulín Cruz and criticism of Trump | Repeated messages concerning the San Juan mayor, Colbert, and a “Trump attacked Twitter” hall of fame. | Political satire and criticism of Trump's treatment of opponents. |
| International affairs | Repeated messages about a Bosnian Croat war criminal's death, Libya and human trafficking, and Sadiq Khan's comments on an immigration case. | A broader international-news stream accompanying U.S. politics. |
| Regional victory framing | A translated message mentioning ISIS, Iraq, Syria, Iran, Hezbollah and “axis resistance” appears across 12 authors. | A smaller regional narrative alongside the dominant U.S. political material. |

The mixture suggests distribution of a political/news content package rather than discussion of a single issue. That is an interpretation of the selected burst, not a characterization of every account or the entire Iran_1 dataset.

## Historical background

The selected date falls immediately after Michael Flynn's December 1, 2017 guilty plea to making false statements to FBI agents. This helps explain the timeliness of the repeated Flynn/Mueller headline. This statement describes the event at the time, not the later legal disposition. [U.S. Department of Justice, Special Counsel archive](https://www.justice.gov/archives/sco-mueller).

The message concerning a Bosnian Croat war criminal dying after drinking poison appears to refer to Slobodan Praljak. The ICTY reported that Praljak died on November 29, 2017, after drinking a liquid during the appeal judgment and receiving medical assistance. The event identification is inferred from the post wording and timing. [ICTY statement, November 29, 2017](https://www.icty.org/en/press/statement-on-passing-of-slobodan-praljak).

These contemporaneous events provide context for the news being redistributed. The name `Iran_1` is treated here as a dataset label; this report does not independently establish account nationality, sponsorship, or operational attribution.

## Limitations and next checks

1. **Selection effects:** the subgroup and windows were selected for strong graph connectivity and hashtag sharing. These peak examples cannot establish typical behavior across the dataset.
2. **Timestamp precision:** matching recorded minutes do not demonstrate second-level simultaneity. Timestamp provenance should be checked before making finer timing claims.
3. **Translation and preprocessing:** translated text can merge wording differences. The central 15-message finding was checked against original text and repost source IDs, but word frequencies still contain preprocessing artifacts.
4. **Dependent observations:** reposts by the same accounts and multiple hashtags in one message are not independent pieces of evidence. The score counts an author pair again for every hashtag it shares.
5. **Alternative mechanisms:** a common feed, shared scheduler, or coordinated human reposting could produce similar patterns. The results do not distinguish these mechanisms.
6. **Next validation:** test whether these 13 accounts repeatedly repost the same source sets on other days, compare their timing with similarly active outside accounts, and inspect source-account and application patterns.

Methodological review: all 11 categories in the statistical-interpretation checklist were considered. The material concerns here are selection, peak searching, analysis choices, dependent observations, and overinterpretation of group-level or causal claims. No p-values, confidence intervals, or causal estimates were produced; other checklist categories are not assessable or applicable to this descriptive comparison. Verification status: **ANALYZED**, with the central burst checked against Step-3 source rows; full pipeline reproduction and inferential validation were not performed.

## Local source files


### 15-minute outputs


- [peak_shared_hashtag_posts.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_15min/peak_shared_hashtag_posts.csv)

- [shared_hashtag_window_summary.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_15min/shared_hashtag_window_summary.csv)

- [group_accountids.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_15min/group_accountids.csv)

- [peak_shared_hashtag_word_counts.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_15min/peak_shared_hashtag_word_counts.csv)

- [peak_shared_hashtag_hashtag_counts.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_15min/peak_shared_hashtag_hashtag_counts.csv)



### 1-hour outputs


- [peak_shared_hashtag_posts.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_h/peak_shared_hashtag_posts.csv)

- [shared_hashtag_window_summary.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_h/shared_hashtag_window_summary.csv)

- [group_accountids.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_h/group_accountids.csv)

- [peak_shared_hashtag_word_counts.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_h/peak_shared_hashtag_word_counts.csv)

- [peak_shared_hashtag_hashtag_counts.csv](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/top_k_core_authors/shared_hashtags_example/time_delta_h/peak_shared_hashtag_hashtag_counts.csv)



- [Step-3 source parquet](../results/Labeled_Datasets/Iran_1/Iran_1_part_all/step_3_key_authors_graph/topic_col_BERTopic_topic_256_top_percentage_100/Iran_1_part_all_step_3.gzip.parquet)
- [Example notebook](../src/temp/group_shared_hashtags_example.ipynb)
- [Shared-hashtag implementation](../src/3_key_authors_graph.ipynb)
