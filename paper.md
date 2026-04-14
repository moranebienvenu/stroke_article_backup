---
numbering:
  heading_2: false
  figure:
    template: Fig. %s
---

<center>
<div style="font-size: 1.5em; font-weight: bold; margin: 1em 0; text-align: center;">
Dashboard
</div>
</center>

:::{iframe} https://stroke-dashboard.db.neurolibre.org/
:width: 100%
:border: 0
:::

<br><br>

# Introduction


Stroke is a major global public health issue, severely affecting quality of life through a wide range of consequences, including aphasia, motor and sensory deficits, behavioral changes, and even death [@BrainInjuryCanada2024]. It is among the most devastating non-communicable diseases (NCDs), ranking second in global mortality and third in combined mortality and disability. In 2021, nearly 12 million people experienced a first-ever stroke, of which 65.3% were ischaemic, and 52.6% occurred in men [@Feigin2025]. This pattern happens slightly similar each year.  

Ischaemic stroke, caused by an obstruction of cerebral blood flow, is the most common type. The present study focuses on ischaemic strokes in the left middle artery leading to aphasia, which affects about one-third of patients [@Pedersen1995]. Aphasia is a disorder that impairs the production and comprehension of language, as well as reading and writing, due to brain damage. While stroke recovery has been widely studied, sex-specific mechanisms underlying aphasia recovery remain underexplored, especially in the acute phase (<72 hours post-stroke). 

Recent advances in molecular neuroimaging now allow investigation of these mechanisms.  [Hansen et al.](https://doi.org/10.1038/s41593-022-01186-3) published a neurotransmitter atlas of normative receptor and transporter densities, later used by [Alves et al.](https://doi.org/10.1038/s41467-025-57680-2) to build an MRI-based white matter atlas of neurotransmitter circuits representing the axonal projections of acetylcholine, dopamine, noradrenaline, and serotonin receptors and transporters. This framework maps how stroke lesions disrupt neurotransmission, distinguishes pre- and postsynaptic effects, and could further help identify sex-specific differences in early neurotransmitter dynamics, guiding more personalized recovery strategies.

To ensure a standardized and reproducible analysis, an interactive dashboard was developed to extract, organize, and visualize the data from [Alves et al.](https://doi.org/10.1038/s41467-025-57680-2), facilitating interpretation in relation to the research question.

The objective of this study is twofold: (1) to use a dashboard-based framework to investigate whether and how biological sex influences neurotransmitter receptor and transporter characteristics during the acute phase of post-stroke aphasia; and (2) to assess whether these early neurochemical patterns can help predict long-term language recovery. Ultimately, this work aims to contribute to more personalized stroke rehabilitation approaches, including the tailored use of receptor agonists or transporter inhibitors, recognizing that men and women may respond differently to the same pharmacological intervention.


# Materials and methods

## Participants

Forty-eight people with aphasia (PWA) were recruited from the Neurology Unit of Hôpital du Sacré-Cœur de Montréal (HSCM), part of the CIUSSS du Nord-de-l’Île-de-Montréal, for a longitudinal study including three timepoints: the acute stage (24–72 h post-stroke), the subacute stage (8–14 days post-stroke), and the chronic stage (approximately 6 months post-stroke). Thirty-eight participants (23 men and 15 women) completed the first assessment during the acute phase, and ultimately, seventeen participants (9 men and 8 women) completed all three timepoints up to the chronic phase. Inclusion and exclusion criteria for PWA were based on those described in [Boucher et al., 2023](https://doi.org/10.1093/braincomms/fcad313). 


## Language Assessment

At each timepoint, participants completed a language assessment battery, including naming comprehension repetition and production tests, as described in [Boucher et al., 2023](https://doi.org/10.1093/braincomms/fcad313). Three core language subscores were derived: naming, repetition, and comprehension. Based on the previous work of [Osa García et al.](https://doi.org/10.3389/fneur.2020.00120), each subscore was scaled from 0 to 10 according to task-specific maximums, yielding a total aphasia severity index, referred to as the Composite Score, ranging from 0 to 30.


## MRI acquisition and lesion processing


Participants underwent MRI scans at all three timepoints. Longitudinal T1-weighted images were processed with *FreeSurfer* to generate within-subject templates. Lesion segmentation was performed semi-automatically using the *Clusterize* toolbox on T1-weighted images and MD maps for the acute phase, and on T1-weighted images maps for the subacute and chronic phases. All segmentations were manually reviewed and corrected by an experienced researcher specialized in lesion tracing in PWA. Binary lesion masks were then generated for each timepoint in RAS orientation (1 mm isotropic resolution). These masks and their corresponding anatomical images were registered to MNI152 2 mm space using FSL’s FLIRT (nearest-neighbor interpolation, no smoothing, zero padding).


The NeuroT-Map pipeline [@Alves2025] was then applied to compute neurotransmitter-specific lesion metrics, including the sum of receptor and transporter location density map voxels or white matter projection map voxels intersecting the lesion, as well as pre- and postsynaptic ratios for the studied neurotransmitter systems. The NeuroT-Map tool and associated scripts are publicly available on [GitHub](https://github.com/Pedro-N-Alves/NeuroT-Map). 


## Dashboard template

An [interactive dashboard](https://stroke-dashboard.db.neurolibre.org/) was developed using the Dash framework ([source code](https://github.com/moranebienvenu/stroke_dashboard)). The dashboard allows users to upload a .zip file containing:

- individual **NeuroT-Map outputs** for each participant: 
  - ***output_les_dis_sub-XXX_ses-VX.csv*** and,
  - ***output_pre_post_synaptic_ratio_sub-XXX_ses-VX.csv***,
- an optional **clinical_data** file (.csv or .xlsx) including: 
  - Demographic (e.g., age, sex) variables and, 
  - Linguistic variables (e.g., naming, repetition, comprehension, and composite scores).

All files are automatically merged into a unified dataset linking clinical, demographic, and NeuroT-Map–derived metrics. The dataset can be filtered by **aphasia type** (Global, Wernicke, Broca, Conduction, Anomic, Transcortical Motor, Transcortical Sensory, Transcortical Mixed, simply Aphasic or Non-aphasic), **sex** (all, men, or women), and **session** (V1–V3, corresponding to acute, subacute, and chronic post-stroke stages).
The dashboard provides interactive visualizations including circular plots illustrating lesion effects on receptor/transporter density maps, tract projection maps, and pre/post-synaptic disruption ratios. These visualizations follow the same representation conventions as NeuroT-map. Users can overlay groups or individual subjects to enable direct visual comparisons.

In addition, the application integrates statistical modules to perform analyses such as:

- **Generalized Linear Models** (GLMs): Tweedie, Poisson, Gaussian, or Binomial distributions,

- **T-tests**: Student’s, Welch’s, Wilcoxon or non-parametric Mann–Whitney U tests; paired or unpaired, 

- **Correlation analyses**: Pearson or Spearman, with automatic visualization as heatmaps or correlation matrices.

All significant effects are displayed as bar plots for the GLMs, and group-level distributions can be visualized through violin or box plots. These features allow for standardized, transparent, and reproducible data exploration and statistical reporting across aphasia subtypes, sexes, and timepoints.

## Statistical Analysis 

To address our first objective, thanks to the dashboard, we performed a series of generalized linear models (GLMs) using a Tweedie distribution (variance power =1.4) with a logarithmic link function to accommodate continuous outcomes with skewed distributions and potential zero-values. In the acute full-sample analysis (n = 38), models included interaction terms between sex, lesion volume, and age to explore their potential modulatory effects on the relationship between acute phase neurotransmitter metrics (voxelwise damage to density and projection maps, as well as pre- and post-synaptic ratios) and early language outcomes. We also ran stratified GLMs in men and women separately, without interaction terms but controlling for lesion volume. 

To address the second objective, an additional GLM was conducted using acute-phase neurotransmitter metrics as early predictors of chronic-phase language outcomes (n=17), adjusting for sex and lesion volume as covariates. 

Additionally, two-sample tests (Student’s or Welch’s t-test, Wilcoxon or Mann–Whitney U test) were used depending on the normality (Shapiro–Wilk test) and variance homogeneity (Levene’s test) already tested by the dashboard. Comparisons were performed between men and women separately for each predictor and outcome variable in the acute phase (nm=19; nf=13), in line with our first objective, as well as longitudinal group-level changes between acute and chronic phases (nm=7; nf=9), consistent with our second objective. The significance threshold was set at α = 0.05 (with the Benjamini-Hochberg false discovery rate correction).

Linear mixed models (LMMs) with time (acute, subacute, chronic) and biological sex as fixed effects were conducted to evaluate longitudinal changes in language scores in accordance with the second objective.

Finally, Pearson correlations were used for normally distributed variables, while Spearman correlations were applied otherwise, to assess relationships between neurotransmitter ratios, between ratios and clinical scores, and between damage metrics and outcomes. All correlation tests were performed separately and jointly for males and females in the acute phase, as specified in the first objective. Also, the same correlation tests were made with acute metrics and chronic outcomes, aligned with the second objective. Group-level descriptive statistics (mean, median, SD) were also computed.


The following figure illustrates the architecture behind our results [](#fig1). 


:::{figure} static/fig1.jpg
:label: fig1
:name: fig-methode

Explanatory figure summarizing the main points of the methodology.
:::



# Results

We first examined sex-related differences in neurotransmitter system disruption and language outcomes during the acute phase after stroke, and whether early post-stroke imbalance could predict long-term language recovery.

To visualize disruptions, group-averaged male (n = 23) and female (n = 15) data were overlaid on circular graphs showing lesion effects on receptor/transporter density maps, tract projection maps, and derived synaptic disruption ratios [](#fig1), computed with the NeuroT-Map method by [Alves et al.](https://doi.org/10.1038/s41467-025-57680-2). Note that these sample sizes differ from those used for statistical analyses, as not all participants had clinical data but all had lesion masks.

:::{attention} Enable Computational Interactivity 

**<span style="color:red">To enable interactivity, attach a runtime by clicking the `⏻` icon in the top-right corner of the figure 2 panel</span>**. If no runtime is attached, the figure will remain in its default state: hover and basic interactions are available.

**<span style="color:red">Once loaded, three buttons appear in the corner. Click the middle play button `▶️` to activate figure 2.</span>** When the static figure is replaced by an interactive Plotly chart, use the toggles to modify the display. Use <span style="display:inline-block; transform: scaleX(-1) scaleY(-1);">↪️</span> to revert to the original static figure.

:::


:::{figure} #fig2cell
:label: fig2
:name: fig-neurotmap-analysis
:placeholder: ./static/fig2.png

Interactive NeuroTmap analysis showing base and overlay comparisons. 
Left panel: Proportion of each neurotransmitter system affected by the lesion based on receptor/transporter location density maps. Middle panel: Proportion of each neurotransmitter system affected by the lesion based on receptor/transporter tract projection maps. Right panel: Synaptic disruption ratios for men and women, shown in natural logarithmic scale. Abbreviations: 5HT1a serotonin receptor 1a, 5HT1b serotonin receptor 1b, 5HT2a serotonin receptor 2a, 5HT4 serotonin receptor 4, 5HT6 serotonin receptor 6, 5HTT serotonin transporter, α4β2 acetylcholine receptor α4β2, D1 dopamine receptor 1, D2 dopamine receptor 2, DAT dopamine transporter, M1 muscarinic 1 receptor, Nor noradrenaline transporter, VAChT acetylcholine vesicular transporter.
***Users can select different sessions (V1, V2, V3) and sex filters (men, women, all) to explore the data interactively.***

:::

When controlling for equal lesion volume, women exhibited greater damage to neurotransmitter systems than men on both density and projection maps, although overall involvement was low (< 2.5%), except for the serotonin transporter in women (3.5%) on location maps injury  [](#fig2).

Concerning the synaptic disruption graph, the presynaptic ratio compares transporter damage to receptor damage. A positive value means transporters are more affected, while a negative value means receptors are more affected. The postsynaptic ratio does the opposite, comparing receptor to transporter damage. Since one transporter can be linked to several receptors, the postsynaptic damage is averaged across them. Both ratios are calculated from the overlap between lesion maps and the density or projection maps of transporters and receptors [@Alves2025].
Synaptic ratios revealed opposite sex-specific patterns: men showed a predominance of transporters over receptors damages in dopaminergic systems, while women showed the reverse, with the opposite holding true for cholinergic systems. Serotonergic disruption imbalance was also more pronounced in women ([](#fig2)). In addition, statistical testing revealed a significant sex difference for only the presynaptic 5HT1A ratio (Mann–Whitney U = 106, p = 0.049), with women showing higher values compared to men. This corresponds to an estimated +37.7% ($=e^{0.32}$) increase in transporter damage relative to receptor damage. 

Global and sex-stratified GLM analyses, performed using the dashboard with a Tweedie distribution (power = 1.4) and a log link, including age and lesion volume as covariates, showed no significant associations between synaptic ratios and language outcomes (naming, repetition, comprehension, composite score), although sex-specific trends were apparent ({numref}`tab1-glm`). These non-significant results (p >0.05), likely reflect the limited sample size.

:::{table} Table 1 – Percentage change in acute clinical scores per 0.1 unit increase in acute neurotransmitter ratio
:widths: auto
:align: center
:class: tight-table
:name: tab1-glm


| **System**      | **Synaptic Ratio** | **Group** | **Repetition [%]** | **Naming [%]** | **Comprehension [%]** | **Composite [%]** |
|-----------------|-------------------:|:----------|-------------------:|----------------:|-----------------------:|------------------:|
| **Cholinergic** | Pre-α4B2 | Global | 16.81 | 3.39 | 1.63 | 8.06 |
|  |  | Men | 31.18 | (14.78) | (6.47) | 4.55 |
|  |  | Women | 2.08 | 1.19 | 1.22 | 2.03 |
|  | Pre-M1 | Global | 4.30 | 1.74 | 1.97 | 3.09 |
|  |  | Men | 0.48 | (13.12) | (5.52) | (3.29) |
|  |  | Women | 3.99 | 5.34 | 5.27 | 4.69 |
|  | Post-VAchT | Global | (8.22) | (2.92) | (2.80) | (5.35) |
|  |  | Men | (3.48) | 28.31 | 11.6 | 5.54 |
|  |  | Women | (4.60) | (5.65) | (5.79) | (5.32) |
| **Dopaminergic** | Pre-D1 | Global | 4.40 | 1.80 | (1.17) | 2.03 |
|  |  | Men | 8.05 | 2.62 | (1.31) | 3.76 |
|  |  | Women | 0.01 | 2.36 | (0.40) | 0.25 |
|  | Pre-D2 | Global | 0.80 | (4.96) | (4.29) | (2.34) |
|  |  | Men | 16.63 | 0.44 | (4.51) | 5.30 |
|  |  | Women | (5.04) | (6.23) | (3.89) | (4.69) |
|  | Post-DAT | Global | (2.65) | 2.52 | 3.64 | 0.54 |
|  |  | Men | (10.67) | (2.05) | 2.82 | (4.55) |
|  |  | Women | 4.85 | 4.76 | 3.94 | 4.36 |
| **Serotonergic** | Pre-5HT1a | Global | 0.36 | 1.48 | 2.57 | 1.55 |
|  |  | Men | (3.99) | (1.84) | 0.65 | (1.33) |
|  |  | Women | 3.74 | 4.47 | 5.17 | 4.28 |
|  | Pre-5HT1b | Global | (0.12) | 1.21 | 1.11 | 0.74 |
|  |  | Men | (2.79) | (0.74) | (0.64) | (1.34) |
|  |  | Women | 1.94 | 2.87 | 3.71 | 2.81 |
|  | Pre-5HT2a | Global | (0.42) | 1.26 | 1.74 | 0.88 |
|  |  | Men | (4.85) | (1.57) | (0.08) | (1.90) |
|  |  | Women | 2.43 | 3.28 | 3.75 | 3.08 |
|  | Pre-5HT4 | Global | (3.06) | (2.10) | 2.02 | (0.67) |
|  |  | Men | (6.46) | (4.66) | 1.72 | (2.15) |
|  |  | Women | 3.66 | 2.94 | 3.36 | 3.38 |
|  | Pre-5HT6 | Global | (1.20) | 1.88 | 2.31 | 0.93 |
|  |  | Men | (5.59) | (0.36) | 0.56 | (1.66) |
|  |  | Women | 2.95 | 4.00 | 5.13 | 3.95 |
|  | Post-5HTT | Global | 0.77 | (1.27) | (2.08) | (0.92) |
|  |  | Men | 5.31 | 1.55 | (0.28) | 1.83 |
|  |  | Women | (3.40) | (4.12) | (4.87) | (4.04) |

:::

{numref}`tab1-glm` summarizes the estimated effects of a 0.1 increase in pre- or post-synaptic damage imbalance on language performance (naming, repetition, comprehension, and composite score), stratified by sex and neurotransmitter system. In the cholinergic system, pre-α4β2 imbalance was estimated to enhance repetition, particularly in men, but reduce naming and comprehension scores in men, whereas pre-M1 showed negative effects in men and modest benefits in women. Post-VAChT effects were overall estimated as unfavorable, yet sex-specific: predicted improvements in naming and comprehension for men and declines across tasks for women. In the dopaminergic system, pre-D2 was estimated to support repetition in men but impair comprehension, with women showing consistent negative associations; post-DAT exhibited the reverse pattern for women and men exhibited an unfavorable pattern for all scores except comprehension. In the serotonergic system, presynaptic imbalances were generally predicted to benefit women and be neutral or negative in men, while post-5HTT showed the opposite trend.

We then examined correlations between pre- and post-synaptic ratios in the acute phase (n = 38) by selecting all subjects, men only, and women only for the V1 session and synaptic ratio variables in the dashboard. Several strong positive associations emerged across neurotransmitter systems (e.g., pre-M1 with pre-5HT1b/2a, r > 0.8, p < 0.05). Post-hoc power was high (mean = 0.904). Stratified analyses revealed sex-related differences: women exhibited more and stronger correlations, including strong positive associations between post-DAT and serotonergic presynaptic ratios, and strong negative associations between pre-D2 and both pre-M1 and serotonergic presynaptic ratios. These patterns were not observed in men. The mean post-hoc statistical power for all significant correlations remained high in both subgroups (0.948 in men, 0.927 in women) [](#fig3).

:::{note} To activate Figure 3 interactivity: **<span style="color:red">click the play button `▶️`</span>** if available. If only the `⏻` icon is present, click it first to start the runtime, then click `▶️`.
:::

:::{figure} #fig3cell
:label: fig3
:name: fig-correlation-analysis
:placeholder: ./static/fig3.png

Interactive correlation heatmaps showing the relationship between pre- and post-synaptic ratios across location and projection maps in the acute phase separately for All participants, Men, and Women. Pearson’s r was used for normally distributed pairs (Shapiro-Wilk test, p > 0.05), Spearman’s rₛ otherwise. Colors indicate correlation (–1 = blue, +1 = red); only FDR-significant correlations (p < 0.05) are shown in bright colors, non-significant in grey. Panels: all participants (left, n=38), men (center, n=23), women (right, n=15). 
***Users can toggle the display of correlations values and adjust the p-value threshold with the slider to explore the data interactively.***
:::


We then applied linear mixed-effects modeling for each bounded clinical language outcome (0–10 for naming, repetition, and comprehension; 0–30 for the composite), with fixed effects for time (acute, subacute and chronic phases), sex (reference: women in the acute phase), and their interaction, while adjusting for lesion volume. A random intercept accounted for within-subject variability, and residual diagnostics (QQ plots, Shapiro-Wilk tests) supported the model assumptions ({numref}`tab2-mixed-model`).

::::{table} Table 2 – Mixed Linear Model Regression
:widths: auto
:align: center
:class: tight-table
:name: tab2-mixed-model

| Outcome        | Effect               | Coeff  | SE     | Z      | P-value | [CI 95%]             |
|----------------|----------------------|--------|--------|--------|----------|----------------------|
| **Repetition** | Intercept            | 6.943  | 1.007  | 6.989  | 0.000    | [4.970 ; 8.916]     |
|                | Time[T.V2]           | 0.675  | 0.860  | 0.785  | 0.432    | [-1.010 ; 2.361]    |
|                | Time[T.V3]           | 2.177  | 0.942  | 2.311  | 0.021    | [0.331 ; 4.023]     |
|                | Sexe[T.M]            | -1.029 | 1.090  | -0.944 | 0.345    | [-3.166 ; 1.107]    |
|                | Time[T.V2]:Sexe[T.M] | 0.571  | 1.129  | 0.505  | 0.613    | [-1.643 ; 2.784]    |
|                | Time[T.V3]:Sexe[T.M] | 1.198  | 1.357  | 0.883  | 0.377    | [-1.461 ; 3.858]    |
|                | Group Var            | 4.990  | 1.461  | —      | —        | —                    |
| **Naming**     | Intercept            | 5.966  | 0.902  | 6.613  | 0.000    | [4.198 ; 7.735]     |
|                | Time[T.V2]           | 0.453  | 1.037  | 0.437  | 0.662    | [-1.579 ; 2.485]    |
|                | Time[T.V3]           | 0.489  | 1.110  | 0.440  | 0.660    | [-1.686 ; 2.663]    |
|                | Sexe[T.M]            | -0.974 | 1.005  | -0.969 | 0.332    | [-2.943 ; 0.995]    |
|                | Time[T.V2]:Sexe[T.M] | 1.080  | 1.361  | 0.794  | 0.427    | [-1.587 ; 3.748]    |
|                | Time[T.V3]:Sexe[T.M] | 4.651  | 1.587  | 2.930  | 0.003    | [1.539 ; 7.762]     |
|                | Group Var            | 1.522  | 0.659  | —      | —        | —                    |
| **Comprehension** | Intercept         | 6.102  | 0.731  | 8.342  | 0.000    | [4.668 ; 7.535]     |
|                | Time[T.V2]           | 1.198  | 0.697  | 1.720  | 0.086    | [-0.168 ; 2.564]    |
|                | Time[T.V3]           | 2.869  | 0.756  | 3.795  | 0.000    | [1.387 ; 4.351]     |
|                | Sexe[T.M]            | 1.003  | 0.797  | 1.258  | 0.208    | [-0.559 ; 2.565]    |
|                | Time[T.V2]:Sexe[T.M] | -0.355 | 0.913  | -0.388 | 0.698    | [-2.145 ; 1.435]    |
|                | Time[T.V3]:Sexe[T.M] | 0.702  | 1.088  | 0.646  | 0.519    | [-1.430 ; 2.835]    |
|                | Group Var            | 2.117  | 0.757  | —      | —        | —                    |
| **Composite**  | Intercept            | 19.103 | 2.196  | 8.698  | 0.000    | [14.799 ; 23.408]   |
|                | Time[T.V2]           | 2.353  | 2.213  | 1.063  | 0.288    | [-1.985 ; 6.691]    |
|                | Time[T.V3]           | 5.563  | 2.393  | 2.324  | 0.020    | [0.872 ; 10.253]    |
|                | Sexe[T.M]            | -0.975 | 2.383  | -0.410 | 0.682    | [-5.643 ; 3.692]    |
|                | Time[T.V2]:Sexe[T.M] | 1.225  | 2.903  | 0.422  | 0.673    | [-4.465 ; 6.914]    |
|                | Time[T.V3]:Sexe[T.M] | 6.664  | 3.441  | 1.937  | 0.053    | [-0.080 ; 13.408]   |
|                | Group Var            | 15.545 | 2.218  | —      | —        | —                    |

::::



{numref}`tab2-mixed-model` showed naturally that for each clinical score, lesion volume was negatively associated with most scores (p < 0.001; p < 0.05 for repetition). Women improved in repetition over time (β = 2,177, p = 0.021). Naming showed a significant time × sex interaction at V3 (β = 4.651, p = 0.003), with men improving more than women in chronic phase. Comprehension and composite scores improved in women (p < 0.001 and p < 0.05 at V3, respectively), with a non-significant trend for greater composite score improvement in men (β = 6.664, p = 0.053).

To illustrate longitudinal changes in neurotransmitter system disruption and synaptic ratio imbalance, we overlaid acute (n=38) and chronic (n=17) group-averaged data in circular graphs as we did in [](#fig2), as shown in [](#fig4).

:::{note} To activate Figure 4 interactivity: **<span style="color:red">click the play button `▶️`</span>** if available. If only the `⏻` icon is present, click it first to start the runtime, then click `▶️`.
:::

:::{figure} #fig4cell
:label: fig4
:name: fig-cross-correlation-analysis
:placeholder: ./static/fig4.png

Interactive NeuroTmap analysis showing base and overlay comparisons for all subjects in acute versus chronic phases. 
Panels and Abbreviations as in Fig.1.
***Users can select different sessions (V1, V2, V3) to explore the data interactively.***
:::

Neurotransmitter system damage was slightly higher in the chronic phase than in the acute, with each percentage difference being significant according to a Wilcoxon signed-rank test (p < 0.05). Synaptic ratios were more imbalanced in the chronic phase for the cholinergic and serotonergic systems (except pre-5HT4 and pre-5HT1a), whereas dopaminergic ratios tended toward zero in the chronic phase, with pre-D2 reversing sign compared to acute phase. Only, post-VAChT showed a negative significant increase in the chronic phase (Paired t-test, t = 2.18, p = 0.044).

After that, we assessed whether acute synaptic disruption imbalance predicted chronic language outcomes using GLM models, , performed using the dashboard with a Tweedie distribution (power = 1.4) and a log link, including sex and lesion volume as covariates. {numref}`tab3-chronic-scores` reports the estimated percentage change in chronic scores per 0.1-unit increase in acute ratio. Although the results did not reach statistical significance (p > 0.05), this may be due to the relatively small sample size (n = 15), which limits statistical power.

::::{table} Table 3 – Percentage change in chronic clinical scores per 0.1 unit increase in acute neurotransmitter ratio
:widths: auto
:align: center
:class: tight-table
:name: tab3-chronic-scores

| **System**     | **Synaptic Ratio** | **Repetition [%]** | **Naming [%]** | **Comprehension [%]** | **Composite [%]** |
|----------------|--------------------|--------------------|----------------|-----------------------|-------------------|
| **Cholinergic** | Pre-α4B2  | (5,74) | (10,64) | (4,97) | (6,67) |
|                | Pre-M1     | 5,33   | (8,73)  | 1,64   | 0,49   |
|                | Post-VAchT | (11,32)| 24,21   | (2,55) | (0,001) |
| **Dopaminergic** | Pre-D1    | 4,30   | 7,71   | 1,08   | 4,08   |
|                | Pre-D2     | (3,11) | (2,42) | (1,10) | (2,20) |
|                | Post-DAT   | (1,34) | (5,71) | 0,04   | (2,10) |
| **Serotonergic** | Pre-5HT1a | 1,59   | (5,53) | 0,57   | (0,62) |
|                | Pre-5HT1b | 1,59   | (3,72) | 0,62   | (0,15) |
|                | Pre-5HT2a | 1,63   | (4,17) | 0,71   | (0,19) |
|                | Pre-5HT4  | 1,19   | (5,39) | 0,08   | (1,01) |
|                | Pre-5HT6  | 1,28   | (4,67) | 0,58   | (0,50) |
|                | Post-5HTT | (1,56) | 5,30   | (0,56) | 0,51   |

::::


The cholinergic system, particularly the post-VAChT ratio, was the strongest predictor of chronic language outcomes. While it conferred notable benefits for naming, it was associated with a detrimental effect on repetition, and minor effects on comprehension and the composite score. Moderate associations were also observed for the pre-α4β2 and pre-M1 ratios across several outcomes, with pre-α4β2 generally linked to reduced scores and pre-M1 showing a negative effect mainly on naming. In the dopaminergic system, pre-D1 and pre-D2 showed modest but opposite trends, while serotonergic markers exhibited overall moderate to weak associations, with pre-synaptic ratios favoring repetition but negatively impacting naming score.

Mann–Whitney U tests showed chronic scores exceeded acute scores for the whole sample,  reaching statistical significance for comprehension (meanV1 = 5.49; meanV3 = 8.41; p = 0.019) and the composite score (meanV1= 15.79; meanV3 = 23.24; p = 0.028).

Correlation between pre- and post-synaptic ratios in acute and chronic phases (n=17) were strong for serotonergic ratios, pre-M1, pre-D2, and post-DAT (r > 0.55; p < 0.05; mean post-hoc power = 0.786). Also, early pre-M1 positively correlated with late serotonergic presynaptic ratios, while early pre-D2 showed negative correlations with late serotonergic presynaptic ratios and pre-M1 [](#fig5).

:::{note} To activate Figure 5 interactivity: **<span style="color:red">click the play button `▶️`</span>** if available. If only the `⏻` icon is present, click it first to start the runtime, then click `▶️`. 
:::

:::{figure} #fig5cell
:label: fig5
:name: fig-cross-correlation-analysis
:placeholder: ./static/fig5.png


Interactive correlation heatmaps showing the relationship between pre- and post-synaptic ratios in the acute phase. The Y-axis shows the variables from the 1st selection, and the X-axis shows the variables from the 2nd seletion.
***Users can select different sessions (V1, V2, V3), sex filters (men, women, all) and variables (synaptic ratio, neurotransmitter (Loc),neurotransmitter (Tract), clinical outcomes) to explore the data interactively.***
:::

Correlations between acute pre-synaptic ratios and chronic clinical outcomes were generally low and non-significant, likely due to the small sample size (n = 17; 8 men, 9 women). 

# Discussion

This study represents a contribution to the field of post-stroke aphasia research by implementing a novel, dashboard-based framework for the standardized analysis of neurotransmitter system disruptions. By integrating NeuroT-Map outputs with clinical and demographic data in an interactive, user-friendly interface, our approach allows for systematic visualization and statistical analysis of pre- and post-synaptic receptor and transporter imbalances across acute, subacute, and chronic phases of stroke recovery. This framework not only enables researchers to explore sex-specific patterns of neurotransmitter disruption in real time but also facilitates longitudinal tracking of how early neurochemical alterations may relate to long-term language outcomes. The development of this dashboard, made publicly accessible along with source code and documentation, ensures that the methodology is transparent, reproducible, and readily adaptable for future studies or clinical applications.

Moreover, the present study serves as a proof-of-concept demonstration that combining advanced neuroimaging metrics with interactive data analytics can provide meaningful insights into the biological underpinnings of aphasia recovery. In our cohort of stroke participants with left-hemisphere ischemic lesions, we were able to identify sex-specific trends in neurotransmitter disruption, such as differential presynaptic and postsynaptic imbalance patterns in dopaminergic, cholinergic, and serotonergic systems, and examine their potential associations with language recovery trajectories. Although the sample size was limited, these findings illustrate the feasibility of leveraging a dashboard-based approach to explore individualized and group-level neurochemical effects, paving the way for future personalized rehabilitation strategies that consider biological sex, lesion characteristics, and early neurotransmitter dynamics.

***whether and how biological sex is associated with specific patterns of estimated neurochemical vulnerability during the acute phase of post-stroke aphasia:***


Our results indicate that biological sex is associated with sex-specific patterns of estimated neurotransmitter receptor and transporter vulnerability during the acute phase of post-stroke aphasia. Statistical testing revealed a significant sex difference for the pre-5HT1A ratio, suggesting higher estimated vulnerability of the transporter 5HTT than in this receptor, with women showing higher values than men, whereas other sex effects did not reach statistical significance, likely due to limited sample size. Notably, the 5-HT1A receptor is known to be involved in the modulation of depressive symptoms and stress responses [@Tahiri2024], suggesting that sex-specific differences in this receptor could have functional consequences beyond language outcomes. Women also exhibited greater estimated lesion-related vulnerability across neurotransmitter systems, particularly in serotonergic transporter (5HTT) pathways, highlighting relative vulnerability patterns. While the underlying mechanisms cannot be directly measured here, these patterns are consistent with the higher incidence of post-stroke depression reported in women [@Bushnell2014]. In contrast, men tended to show a predominance of transporters over receptors vulnerability in dopaminergic systems and the reverse in cholinergic systems, suggesting distinct sex-specific neurochemical vulnerabilities after stroke.

Stratified correlation analyses revealed stronger interdependencies between neurotransmitter systems’ estimated vulnerabilities in women, suggesting a more integrated neurochemical network architecture. This pattern was less evident in men. Consequently, a lesion disrupting one system in men may have more localized effects, while in women, stronger cross-system coupling could allow the disruption to cascade, amplifying the impact on acute language performance. This sex difference aligns with established brain connectivity concepts where women typically show stronger inter-hemispheric connectivity, facilitating integration, while men show stronger intra-hemispheric connectivity, supporting modular processing [@Ingahalikar2013]. 

Beyond simple lesion magnitude, the organization of neurotransmitter systems also differs by sex. Interestingly, females showed greater lateralization of dopaminergic receptors, for example with the right striatum displaying higher D1 receptor density than the left [@Andersen2000]. Also, an asymmetry was found for D1R location density and white matter projection maps in general [@Alves2025]. In our cohort, the pre-D1 ratio was close to equilibrium in women during the acute phase (0.01) and remained low in the chronic phase (-0.02), whereas men had slightly higher pre-D1 ratios in both phases (0.05 in acute; 0.09 in chronic). This suggests that estimated vulnerability to DAT and D1 receptors was not significantly different for both sexes, potentially resulting in a limited impact on dopaminergic neurotransmission, particularly given that the lesions were located in the left hemisphere. 

GLM analyses also suggested sex-specific patterns in the acute post-stroke phase, although these effects did not reach statistical significance. In women, it was associated with little or no effect on language scores, suggesting that D1 receptors may not be strongly associated with acute language performance in women. In men, pre-D1 showed a slight association with improved repetition performance, indicating a potential sex difference in dopaminergic modulation. Notably, the GLM indicated a trend for a positive association between pre-α4β2 and repetition scores in men, accompanied by a moderate to high negative correlation with naming and comprehension scores this pattern was not observed in women. This may reflect an acute facilitatory role of α4β2 receptors for the phonological and articulatory processes underlying repetition, but potentially at the expense of semantic and lexical processes or perhaps reflecting a maladaptive compensatory mechanism for these other tasks. Indeed, the α4β2 nicotinic receptor is well known to support verbal memory, attention and learning [@Sabri2018]. This suggests that, during the acute phase, predominant damage to cholinergic transporters relative to nicotinic receptors may exert a larger influence on language performance in men. Moreover, sex-specific trends were also observed in serotonergic ratios: presynaptic imbalances were generally predicted to benefit women’s language outcomes and be neutral or negative in men, whereas post-5HTT imbalances showed the opposite trend. These sex-specific patterns in serotonergic vulnerability are consistent with baseline differences in serotonin biology. Females have higher whole blood 5-HT levels [@Gur1990], higher 5-HT transporter availability in the diencephalon and brainstem [@Rodriguez1988], and higher 5-HT1A receptor numbers than males [@Baxter1987;@Staley2006]. In contrast, males synthesize serotonin significantly faster than females, reaching 52% higher mean synthesis rates [@Andreason1994]. This fundamental difference in serotonin turnover may underlie our finding that a 0.1-unit increase in transporter over receptor damage ratio could lead to greater impairments in language outcomes for men: faster serotonin synthesis may require proportionally more transporter function to maintain optimal neurotransmission, whereas women, who generally have higher baseline transporter availability, may be less affected by a comparable degree of transporter damage. This disparity underscores that the functional impact of a neurochemical lesion may be modulated by biological sex. Taken together, these findings suggest the need for nuanced, task-dependent, and potentially personalized approaches to modulating cholinergic, dopaminergic, and serotonergic systems, and warrant further investigation in sex-stratified controlled trials considering individual neurochemical profiles.

These acute-phase sex-specific neurochemical vulnerabilities set the stage for divergent long-term recovery trajectories. We next investigated whether these early neurochemical estimated vulnerability could predict chronic language outcomes.

***whether these early neurochemical patterns can help predict long-term language recovery:***

Our longitudinal models confirmed significant behavioral recovery in language outcomes over time, particularly for repetition, comprehension, and composite scores. However, a sex-specific trajectory was uncovered for naming, where men improved significantly more than women by the chronic phase. Paradoxically, this clinical improvement co-occurred with a worsening damage across system and a trend toward greater presynaptic ratio imbalances in cholinergic and serotonergic systems (except pre-5HT4 and pre-5HT1a), indicating a shift toward greater transporter damage relative to receptors. This apparent paradox suggests that behavioral recovery can progress despite persistent neurochemical dysregulation. However, the fact that serotonergic and cholinergic systems remain imbalanced over time may indicate a biological limit to full recovery, potentially predisposing patients to residual language deficits or affective disturbances. 

A key limitation of this study is the absence of reference values for transporter-to-receptor ratios in healthy individuals, stratified by sex and age. Without such normative baselines, it remains unclear whether the observed imbalances reflect true neurochemical dysfunction or instead arise from methodological factors, such as changes in lesion appearance between acute and chronic MRI scans that affect neurotransmitter mapping.

Although no associations reached statistical significance in our GLM model, likely due to the limited sample size, several consistent trends emerged across systems. Among them, the cholinergic system stood out: the post-VAChT ratio was the strongest predictor of chronic outcomes, showing a paradoxical pattern of facilitating naming performance while hindering repetition. Similarly, pre-α4β2 and pre-M1 ratios were associated with detrimental effects on multiple outcomes, highlighting the possible critical role of early cholinergic integrity for language recovery Dopaminergic predictors revealed modest but directionally distinct effects: pre-D1 tended to support recovery across domains, whereas pre-D2 predicted poorer outcomes, in line with their differential contributions to reward-based learning and executive modulation. The opposite polarity observed between pre-D1 and pre-D2 disruption ratio aligns with established models of dopamine-dependent synaptic plasticity, whereby D1 receptor activation promotes long-term potentiation (LTP) while D2 receptor stimulation facilitates long-term depression (LTD) [@Calabresi2007]. In contrast, serotonergic markers showed weak or inconsistent associations, with presynaptic ratios modestly favoring repetition but negatively impacting naming. This suggests that early serotonergic disruption may be less predictive of chronic outcomes, despite its persistent dysregulation over time.

The correlational analyses provided additional insight. Strong positive correlations of serotonergic, pre-M1, pre-D2, and post-DAT ratios across acute and chronic phases suggests that initial disruptions in these systems persist and could shape longer-term trajectories. Interestingly, early pre-M1 correlated positively with late serotonergic ratios, while pre-D2 correlated negatively, pointing toward potential cross-system interactions that may influence compensatory dynamics.

Taken together, these findings indicate that while our predictive models were underpowered, certain neurotransmitter systems, particularly cholinergic and dopaminergic damage, may provide early biomarkers of long-term recovery trajectories. The significant improvement in comprehension and composite scores across the cohort further underscores that recovery is possible even in the context of persistent dysregulation. A larger sample will be necessary to validate these trends and establish whether specific acute synaptic imbalances can serve as reliable predictors of language outcomes post-stroke.

*Several limitations* of our study must be considered. First, our analysis relied on normative neurotransmitter maps, which do not account for individual variability. The absence of a healthy control group prevents the establishment of reference transporter-to-receptor ratios, making it difficult to determine whether the observed imbalances reflect inherent neurochemical dysregulation in post-stroke individuals or are influenced by methodological factors. Furthermore, the functional impact of any imbalance is likely shaped by lesion location, as receptor and transporter density varies regionally and exhibits hemispheric asymmetries [@Alves2025]. Consequently, a lesion affecting a region with a high receptor density may disproportionately disrupt that system’s function, regardless of total lesion volume. Thus, both age and neuroanatomical context likely determine how neurotransmitter disruptions influence recovery trajectories. Finally, the use of a single, sex-combined white matter projection map, although necessary, may obscure inherent sex differences in structural connectivity, as well as the sex-specific distribution and predominance of neurotransmitter system densities. 

In conclusion, age, sex and lesion location could alter the direction and magnitude of post-aphasia neurochemistry differences. This emphasizes that a simplistic binary view of sex effects is insufficient. Future research and clinical trials must adopt a multi-dimensional perspective that considers the role of sex, age, and neurochemical profile to truly personalize predictions and interventions for stroke recovery. Our study provides initial evidence and a methodological framework for this nuanced approach, which, with further analysis, could pave the way for personalized therapeutic strategies for patients with post-stroke aphasia.


# Data availability

Our data are available on https://github.com/moranebienvenu/stroke_dashboard , it’s the ‘data_article.csv’ file.

# Acknowledgements

This work was supported by the Heart and Stroke Foundation of Canada [grant numbers G16-00014039 and G-19- 0026212] and Canadian Institutes of Health Research/ Instituts de recherche en santé du Canada [grant number 470371]. S.M.B. hold a CHAIRE COURTOIS EN RECHERCHE FONDAMENTALE III (NEUROSCIENCE) de la Faculté des Arts et des Sciences de l'Université de Montréal. 
