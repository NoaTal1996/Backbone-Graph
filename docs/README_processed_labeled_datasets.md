
# Processed Labeled Dataset (Parquet)

This folder contains *processed / labeled* social-media posts exported as Parquet tables for downstream analysis (topic modeling, NER, and information-flow graph construction).

## DataFrame shape (Ecuador Campaign)

`df.shape == (1468565, 29)`

That is: **1,468,565 rows** (posts) and **29 columns**.

## Column schema

 Notes on types:
- `Timestamp` refers to a pandas datetime (`datetime64[ns]`).
- `date` refers to Python `datetime.date`.
- `ndarray` columns typically contain a NumPy array (list-like).
- `min_topic_size` is a number (e.g. 128,256,512) serve as parameter for BERTopic. Higher `min_topic_size` mean few and larger topics.

| Column | Type | Description |
|---|---:|---|
| `postid` | `str` | Unique identifier of the post. |
| `post_text` | `str` | The textual content of the post. The PII inside post_text such as mentions and URLs are hashed. |
| `application_name` | `str` | Hashed version of the name of the application or platform from which the post was made. |
| `post_language` | `str` | Language code of the original post as provided by the platform or detection pipeline. |
| `in_reply_to_postid` | `str` | Anonymized ID of the post this entry is replying to. `None` when not a reply. |
| `in_reply_to_accountid` | `str` | AAnonymized ID of the account the post is replying to. `None` when not a reply. |
| `post_time` | `Timestamp` | Timestamp indicating when the post was made. |
| `accountid` | `str` | Unique anonymized ID for the account that created the post. |
| `account_profile_description` | `str` | Description provided by the account holder in their profile. |
| `follower_count` | `int64` | Number of followers the account had at the time of data collection. |
| `following_count` | `int64` | Number of accounts the user was following at the time of data collection. |
| `account_creation_date` | `date` | Date when the account was created. |
| `is_repost` | `bool_` | Boolean indicator if the post is a repost. |
| `reposted_accountid` | `str` | Anonymized ID of the original account that made the reposted post. `None` when not a re-post. |
| `reposted_postid` | `str` | Anonymized ID of the original post that was reposted. `None` when not a re-post. |
| `hashtags` | `ndarray` | Hashtags included in the post content. Empty list when none found. |
| `urls` | `ndarray` | Hashed URLs shared within the post. Empty list when none found. |
| `account_mentions` | `ndarray` | Anonymized ID of accounts mentioned within the post. Empty list when none found. |
| `is_control` | `bool_` | Boolean indicator marking whether the post is from a control (True) or IO (False) account.|
| `clean_text_with_entities` | `str` | Cleaned text with entity strings preserved. |
| `clean_text_without_enteties` | `str` | Cleaned text with entities removed or masked.|
| `translated_post` | `str` | Machine-translated version of the post to English. Original English posts was translated from and to english for normalization |
| `BERTopic_topic_<min_topic_size>` | `int64` | Topic assignment from BERTopic using the `min_topic_size` configuration. `-1` often indicates outliers/unassigned (BERTopic default). |
| `BERTopic_prob_<min_topic_size>` | `float32` | Probability/confidence of the BERTopic model to the chosen topic. |
| `ner_entities` | `ndarray` | Named entities extracted from the post. Empty list when none found. |
| `<entity_type>_reuse_<time_window>_postids"` | `JSON` | Earlier posts within a `time_window` that share at least one entity from the <entity_type>. Note: This column may be unavailable due to system constraints. |
| `<entity_column>_reuse_<time_window>_accountids` | `ndarray` | Account ids of the authors of the relevant posts. |

## Acknowledgments and Additional Details

This dataset is a processed derivative of the **"Labeled Datasets for Research on Information Operations."**

For more details, including the dataset schema, see:
https://zenodo.org/records/14189193


> Ö. C. Seçkin, “Labeled Datasets for Research on Information Operations”. Zenodo, Nov 19, 2024. doi: 10.5281/zenodo.14189193.
