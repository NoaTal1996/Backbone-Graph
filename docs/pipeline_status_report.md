# Pipeline Status Report

Status as of **2026-08-02 10:50 IDT**, incorporating the supplied SLURM queue
snapshot. Rows are datasets and columns are pipeline steps. Archived results
under `results/Labeled_Datasets/old_2026_07_22/` are excluded.

| Dataset | Step 1: translate, topics, entities | Step 2: BERTopic clustering | Step 3: key-authors graph | Step 4: inter/intra classification |
|---|---|---|---|---|
| Armenia | ✅ Complete | ✅ Complete (4/4 configurations) | ✅ Complete | ⏸️ Not started |
| Cuba | 🔄 Running: translation (`19624428`) | ⏳ Waiting for Step 1 | ⏳ Waiting for Step 2 | ⏸️ Not started |
| Cuba_Test | ✅ Complete | ✅ Complete (4/4 configurations) | ✅ Complete | ⏸️ Not started |
| Ecuador | ✅ Complete | ✅ Complete (4/4 configurations) | 🔄 Running (`19673544`): computing graph indicators | ⏸️ Not started |
| Ecuador_Test | ✅ Complete | ✅ Complete (4/4 configurations) | ✅ Complete | ⏸️ Not started |
| Iran_1 | ✅ Complete | ✅ Complete (4/4 configurations) | ✅ Complete | ⏸️ Not started |
| UAE | 🔄 Running: translation (`19673546`) | 🕒 Queued: 4 jobs (`19673547`–`19673550`) | 🕒 Queued (`19673551`) | ⏸️ Not started |
| Venezuela | ✅ Complete | 🔄 Running (`19699923`): final configuration; 3/4 complete | 🕒 Queued (`19699930`) | ⏸️ Not started |

## Summary

| Step | Complete | Running | Queued | Partial | Waiting/not started |
|---|---:|---:|---:|---:|---:|
| Step 1 | 6 | 2 | 0 | 0 | 0 |
| Step 2 | 5 | 1 | 1 | 0 | 1 |
| Step 3 | 4 | 1 | 2 | 0 | 1 |
| Step 4 | 0 | 0 | 0 | 0 | 8 |

## Notes

- **UAE Step 1 is active.** Its progress report was updating every few seconds
  during inspection. Its four Step 2 jobs and Step 3 job are already submitted
  and pending their dependencies.
- **Cuba Step 1 is active according to SLURM.** Its progress report has not
  changed since 2026-07-30 at 13:42 IDT because the current Spanish translation
  batch contains 5,356,660 posts.
- **Venezuela Step 2** completed the 128, 256, and 512 configurations. Job
  `19699923` is rerunning the final configuration (10). Replacement Step 3 job
  `19699930` is submitted with a dependency on that run.
- **Ecuador Step 3 is active.** Its 21,921-node, 2,816,888-edge graph is built.
  Job `19673544` finished harmonic centrality after roughly 16 hours and is
  continuing with the expensive graph-indicator calculations.
- **Step 4 is a cross-dataset experiment.** Its only current artifact is a
  progress report. The attempted run produced no experiment result files and
  stopped while probing missing legacy campaign paths (`Cuba` and
  `Egypt_UAE`), so no dataset is marked complete.
- `US_24` is not included in the matrix because the repository contains only
  its overview document, not a local pipeline input parquet.

## Status Rules

- **Complete:** expected final artifacts and terminal progress milestones are
  present.
- **Running:** SLURM reports the job in the `R` state, even if its progress file
  is temporarily unchanged during a long operation.
- **Queued:** SLURM reports the submitted job in the `PD` dependency state.
- **Partial/stalled:** some artifacts exist, but the expected terminal outputs
  or milestones are missing.
- **Waiting/not started:** no artifacts for that step are present.
