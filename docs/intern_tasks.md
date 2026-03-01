# Intern Tasks
For each section, create a GitHub issue and mark the checkbox of tasks you have completed.
All reports, codes. slides are in English. Communications can be in Hebrew or English.
Ask questions if needed.


## 0. Learning and Preparation
- [ ] Get access to the BGU cluster. `https://slurm.bgu.ac.il/register` (use VPN)
- [ ] Complete the cluster course.
- [ ] Understand git, GitHub, and GitHub issues.
- [ ] Get access to the GitHub repo.
- [ ] In the Github repo, open a branch for your work.
- [ ] Read "A combined synchronization index for evaluating collective action social media" paper (focus on definitions and methodology, results are less relevant).
- [ ] Have a kickoff meeting with Amit where he explains the project (see [base_slides](base_slides.pptx)), intent tasks, match schedules (when working, when in office), who Sayqan and מפא"ת are, introduces the team (Amit, Noa, Rami), and gives a tour of CBG.
- [ ] Do a HR interview in CBG.
- [ ] Recommended: Use GitHub copilot (free for students) of other AI tools.

## 1. Processed Dataset Publication 
- [x] ~(Blocked) Cannot publish processed datasets, licensing restrictions.~

## 2. Run Pipeline on Additional Datasets
- [ ] Read "Labeled Datasets for Research on Information Operations" (find via Google Scholar, use AI summary if preferred).
- [ ] Read [README_processed_labeled_datasets.md](../final_results/Labeled_Datasets/README_processed_labeled_datasets.md). 
- [ ] Choose a campaign from a different country in the dataset (criteria: > 1M posts, Latin language, not Spanish).
- [ ] Create a README for the campaign (reference: [Ecuador_campaign_overview.md](../data/Ecuador_campaign_overview.md)).
- [ ] Run the full pipeline on the selected dataset (translate, clustering, key authors detection). Output folder shuild be `final_results\<campaign name\country>

## 3. Documentation & Reproducibility
- [ ] Improve README and setup instructions to clarify the pipeline for new contributors.
- [ ] Document environment setup and dependencies.
- [ ] Update quick-start guide.

## 4. Graph Configuration Experiments
Using the existing pipeline:
- [ ] Build graphs with different relation types (e.g., hashtags only; hashtags + mentions; entity reuse with various time windows)
- [ ] Calculate indicators (e.g., centrality, modularity) for each configuration
- [ ] Compare indicator information gain and model performance across configurations
- [ ] Create comparison figures (Venn diagrams, information gain graphs, etc.)
- [ ] Write a report comparing configurations (or add findings to article—check with Amit) 
