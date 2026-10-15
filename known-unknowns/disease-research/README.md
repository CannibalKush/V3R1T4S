# 🧬 Disease research

Cancer, rare and neglected diseases, antimicrobial resistance and outbreaks: public data, public scorers, computational claims only.

**51 open problems**, easiest first. Tractability is a rough guess at the odds for one agent on one machine (★ long shot, ★★★★★ likely).

| Odds | Problem | Kind | Compute |
|---|---|---|---|
| ★★★★☆ | [Breast-cancer prognosis benchmark: beat the published time-dependent concordance on METAB…](pycox-metabric-gbsg-breast-cancer-survival.md) | harvest | laptop-minutes |
| ★★★★☆ | [IMMREP22 TCR-epitope specificity: beat the best published per-epitope micro-AUC on the pu…](immrep22-tcr-epitope-microauc.md) | harvest | laptop-hours |
| ★★★★☆ | [Peptide-MHC class I binding: beat NetMHCpan's blind-set AUC on the frozen public IEDB BD2…](iedb-mhci-bd2009-blind-auc.md) | harvest | laptop-hours |
| ★★★★☆ | [ProteinGym supervised benchmark: beat the public best 5-fold Spearman on a cancer-gene DM…](proteingym-cancer-dms-supervised-5fold.md) | harvest | laptop-hours |
| ★★★★☆ | [ProteinGym zero-shot: beat the best public Spearman on a cancer-gene deep-mutational-scan…](proteingym-cancer-dms-zero-shot.md) | harvest | laptop-hours |
| ★★★★☆ | [TDC DrugComb HSA/Loewe/Bliss/ZIP: lower the leaderboard MAE on a cancer drug-synergy endp…](tdc-drugcomb-synergy-four-endpoints.md) | harvest | laptop-hours |
| ★★★★☆ | [TDC DrugComb_CSS: lower the leaderboard MAE for drug-combination sensitivity in cancer ce…](tdc-drugcomb-css-mae.md) | harvest | laptop-hours |
| ★★★★☆ | [CDC FluSight emergency-department visits: beat the FluSight-ensemble's season WIS on the…](flusight-ed-visits-beat-ensemble-wis.md) | harvest | laptop-hours |
| ★★★★☆ | [CDC FluSight hub: beat the FluSight-ensemble's season-average WIS retrospectively on a co…](flusight-retrospective-beat-ensemble-wis.md) | harvest | laptop-hours |
| ★★★☆☆ | [AMR genotype-to-phenotype: beat the published benchmark F1 on the frozen PATRIC species-a…](amr-patric-folds-beat-published-f1.md) | harvest | laptop-hours |
| ★★★☆☆ | [DRIAMS MALDI-TOF resistance prediction: beat the published per-species-drug AUROC on the…](driams-maldi-amr-beat-published-auroc.md) | harvest | laptop-hours |
| ★★★☆☆ | [Dengue Forecasting Project (San Juan and Iquitos): beat the published forecast skill on t…](dengue-2015-open-challenge-beat-published-skill.md) | harvest | laptop-hours |
| ★★★☆☆ | [DrEval cross-study generalisation: beat the public best CTRPv2-to-GDSC2 (and CCLE/GDSC1/C…](dreval-cross-study-ctrpv2-to-gdsc2.md) | harvest | laptop-hours |
| ★★★☆☆ | [DrEval leave-cell-line-out: beat the public best normalized R^2 / Pearson for cancer drug…](dreval-lco-ctrpv2-normalized-r2.md) | harvest | laptop-hours |
| ★★★☆☆ | [DrEval leave-drug-out: the open question of beating the naive mean-effects baseline for u…](dreval-ldo-beat-naive-mean-effects.md) | harvest | laptop-hours |
| ★★★☆☆ | [European COVID-19 Forecast Hub archive: beat EuroCOVIDhub-ensemble's WIS on the hub's own…](covid19-hub-europe-archive-beat-eurocovidhub-ensemble.md) | harvest | laptop-hours |
| ★★★☆☆ | [European RespiCast hub: beat the hub ensemble's WIS for influenza-like illness or acute r…](respicast-ili-ari-europe-beat-hub-ensemble.md) | harvest | laptop-hours |
| ★★★☆☆ | [German COVID-19 hospitalization nowcast hub: beat the hub ensemble's WIS on the published…](german-hospitalization-nowcast-hub-beat-ensemble-wis.md) | harvest | laptop-hours |
| ★★★☆☆ | [Gut-microbiome disease classification: beat the published cross-validated AUC on public n…](metagenomics-nonneoplastic-disease-classification.md) | harvest | laptop-hours |
| ★★★☆☆ | [HEST-Benchmark: beat the best published Pearson for predicting spatial gene expression fr…](hest-bench-cancer-expression-from-morphology.md) | harvest | laptop-hours |
| ★★★☆☆ | [ISIC 2018 Task 2 (dermoscopic attribute segmentation): beat the challenge-best mean Jacca…](isic2018-task2-attribute-detection-jaccard.md) | standard | laptop-hours |
| ★★★☆☆ | [ISIC 2019 skin-lesion diagnosis with an 'unknown' class: beat the best balanced accuracy…](isic2019-diagnosis-balanced-accuracy-with-unknown.md) | harvest | laptop-hours |
| ★★★☆☆ | [MFASS splice-disruption prediction: beat Pangolin's published average precision on the 27…](mfass-splice-disruption-beat-pangolin-ap.md) | harvest | laptop-hours |
| ★★★☆☆ | [MedMNIST v2: beat the best published accuracy/AUC on the colorectal-histology (PathMNIST)…](medmnist-pathmnist-breastmnist-accuracy.md) | harvest | laptop-hours |
| ★★★☆☆ | [NCBI Pathogen Detection AST: beat the published antibiotic-specific genotype-phenotype F1…](ncbi-pathogen-ast-ecoli-genotype-phenotype-f1.md) | harvest | laptop-hours |
| ★★★☆☆ | [NIH/NLM thin-smear malaria cells: beat the published sensitivity at matched specificity,…](nih-thin-smear-malaria-patient-grouped-sensitivity.md) | harvest | laptop-hours |
| ★★★☆☆ | [PerturBench Frangieh21: beat the published best covariate-transfer metrics for Perturb-se…](perturbench-frangieh21-melanoma-transfer.md) | harvest | laptop-hours |
| ★★★☆☆ | [PerturBench Jiang24: beat the published best cytokine-perturbation transfer metrics acros…](perturbench-jiang24-cancer-lines-transfer.md) | harvest | laptop-days (jiang24_processed.h5ad.gz is 15.2 GB compressed; budget ~60 GB free disk and out-of-core or pseudobulk processing) |
| ★★★☆☆ | [PerturBench Norman19: beat the published best combination-perturbation prediction metrics…](perturbench-norman19-combo-prediction.md) | harvest | laptop-hours |
| ★★★☆☆ | [PerturBench Srivatsan20: beat the published best cross-cell-line chemical-perturbation tr…](perturbench-srivatsan20-cell-line-transfer.md) | harvest | laptop-hours |
| ★★★☆☆ | [ProteinGym clinical indels: beat the leaderboard's best average AUC on insertion/deletion…](proteingym-clinical-indels-auc.md) | harvest | laptop-hours |
| ★★★☆☆ | [ProteinGym indel benchmark (zero-shot): beat the best average Spearman on insertion/delet…](proteingym-dms-indels-zeroshot-spearman.md) | harvest | laptop-hours |
| ★★★☆☆ | [RSV forecast hub: beat the hub ensemble's season-average WIS retrospectively on a complet…](rsv-hub-retrospective-beat-ensemble-wis.md) | harvest | laptop-hours |
| ★★★☆☆ | [Rare-disease gene prioritisation: beat published ranking performance on a frozen phenopac…](phenopacket-store-rare-disease-gene-prioritization.md) | harvest | laptop-hours |
| ★★★☆☆ | [RareDis corpus: beat the published BioBERT F1 for rare-disease and sign entity recognitio…](raredis-corpus-rare-disease-ner-f1.md) | harvest | laptop-hours |
| ★★★☆☆ | [RespiCast COVID-19 hub: beat the hub ensemble's season WIS for COVID-19 hospital admissio…](respicast-covid19-hub-beat-ensemble-wis.md) | harvest | laptop-hours |
| ★★★☆☆ | [TCGA multi-omics survival: beat the best published C-index or integrated Brier score for…](tcga-multiomics-survival-cindex-herrmann.md) | harvest | laptop-hours |
| ★★★☆☆ | [Tuberculosis drug resistance from genotype: beat the WHO catalogue head-to-head on the pu…](cryptic-tb-resistance-beat-who-catalogue.md) | harvest | laptop-hours |
| ★★★☆☆ | [US COVID-19 Forecast Hub: beat the hub ensemble's season-average WIS for hospital admissi…](covid19-forecast-hub-retrospective-beat-ensemble-wis.md) | harvest | laptop-hours |
| ★★★☆☆ | [Unseen single-gene perturbations in leukaemia cells: beat the linear baseline that curren…](linear-baseline-perturbation-replogle-k562.md) | harvest | laptop-hours |
| ★★☆☆☆ | [CAID3 (Critical Assessment of Intrinsic Disorder): beat the published best average precis…](caid3-disorder-binding-average-precision.md) | harvest | laptop-hours |
| ★★☆☆☆ | [CODE-test 12-lead ECG: beat the published per-abnormality F1 on the 827-exam annotated te…](code-test-ecg-abnormality-f1.md) | harvest | laptop-hours |
| ★★☆☆☆ | [ISIC 2017 Part 3 (melanoma and seborrheic keratosis): beat the challenge-best mean AUC of…](isic2017-part3-melanoma-sk-mean-auc.md) | standard | laptop-hours |
| ★★☆☆☆ | [ISIC 2018 Task 3 (HAM10000 diagnosis, 7 classes): beat the best balanced multiclass accur…](isic2018-task3-lesion-diagnosis-balanced-accuracy.md) | standard | laptop-hours |
| ★★☆☆☆ | [ISIC 2018 skin-lesion segmentation: beat the challenge-winning thresholded Jaccard on the…](isic2018-lesion-segmentation-thresholded-jaccard.md) | standard | laptop-hours |
| ★★☆☆☆ | [OpenKBP radiotherapy dose prediction: beat the challenge winner's dose score 2.429 Gy or…](openkbp-dose-prediction-test-dose-dvh-score.md) | standard | laptop-hours |
| ★★☆☆☆ | [PTB-XL ECG classification: beat the best published macro-AUC on the fixed fold-10 test set](ptbxl-ecg-macro-auc-fold10.md) | standard | laptop-hours |
| ★★☆☆☆ | [PatchCamelyon (lymph-node metastasis patches): beat 89.8% accuracy / 0.963 AUC on the off…](pcam-patchcamelyon-from-scratch-accuracy.md) | standard | laptop-hours |
| ★★☆☆☆ | [ProteinGym clinical substitutions (ClinVar benign/pathogenic): beat the leaderboard's bes…](proteingym-clinical-substitutions-auc.md) | harvest | laptop-hours |
| ★★☆☆☆ | [DrEval ex vivo transfer: beat the naive baseline when a cell-line drug-response model mee…](dreval-exvivo-beataml2-pdx-transfer.md) | moonshot | laptop-days |
| ★★☆☆☆ | [LUNA16 lung-nodule detection and false-positive reduction: beat the best CPM (0.951 detec…](luna16-nodule-detection-cpm-10fold.md) | standard | laptop-days |

← [All categories](../README.md)
