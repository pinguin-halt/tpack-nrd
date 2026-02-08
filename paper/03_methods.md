## 3. Methods

### 3.1 Research Design

This study employed a pre-experimental one-group pretest-posttest design (Creswell & Creswell, 2018) to examine the effect of a Project-Based Learning (PjBL) intervention on pre-service science teachers' integrative lesson planning competence. Participants designed lesson plans before and after the PjBL intervention, and the quality of these lesson plans was assessed using a standardized rubric across three integration dimensions: TPACK, STEM, and ESD. The pre-experimental design was selected because the primary purpose of the study was not to establish strict causal inference through between-group comparison, but rather to (a) document changes in integrative design competence following the intervention and (b) model the structural relationships among PjBL implementation quality, integration dimensions, and overall lesson plan quality using PLS-SEM. The absence of a control group is acknowledged as a limitation in Section 5.8.

### 3.2 Participants

The participants were 95 pre-service science teachers enrolled in a teacher education program at a public university in Indonesia. All participants were undergraduate students in their third or fourth year of study, having completed foundational courses in science content, general pedagogy, and educational technology. Purposive sampling was employed, selecting participants who were concurrently enrolled in a course on instructional planning for science education, which served as the natural site for the PjBL intervention. The sample size of 95 exceeds the minimum threshold recommended for PLS-SEM, which Hair et al. (2022) suggest should be at least ten times the maximum number of structural paths directed at any single construct (in this model, four paths directed at the RPP construct, yielding a minimum of 40). All participants provided informed consent prior to data collection, and the study was conducted in accordance with the ethical guidelines of the participating institution.

### 3.3 Intervention: PjBL Implementation

The PjBL intervention was implemented across the instructional planning course over a structured sequence of sessions. Participants engaged in a project cycle requiring them to design integrative lesson plans that simultaneously incorporated TPACK, STEM, and ESD dimensions. The intervention followed five stages adapted from Krajcik and Shin (2014):

1. **Orientation and driving question.** Participants were introduced to a real-world sustainability problem related to their science content area. Driving questions were designed to necessitate interdisciplinary inquiry and the consideration of environmental, social, and economic sustainability dimensions.

2. **Planning and investigation.** Participants investigated the scientific content, identified relevant technologies for instruction, explored connections across STEM disciplines, and examined sustainability implications. They were provided with exemplar lesson plan frameworks and rubric criteria to guide their design process.

3. **Artifact creation.** Participants designed integrative lesson plans (RPP) as the primary project artifact. Each lesson plan was required to demonstrate explicit integration of technology-enhanced pedagogy (TPACK), interdisciplinary STEM connections, and sustainability perspectives (ESD).

4. **Peer review and revision.** Completed drafts were subjected to structured peer review using the same rubric employed for formal assessment. Participants revised their lesson plans based on peer feedback, a process intended to deepen their understanding of integration quality criteria.

5. **Presentation and reflection.** Participants presented their final lesson plans, articulated their design rationale, and reflected on the integration process. This stage provided opportunities for metacognitive engagement with the design challenges encountered.

The quality of PjBL implementation was assessed through an observation instrument completed by course instructors, measuring the fidelity and quality of each PjBL stage as experienced by participants.

### 3.4 Instruments

#### 3.4.1 Integrative Lesson Plan Rubric (Pretest-Posttest)

The primary instrument was a rubric for evaluating the quality of integrative lesson plans, scored on a four-point Likert scale (1 = does not meet the criterion, 2 = partially meets, 3 = meets, 4 = exceeds the criterion). The rubric assessed three integration dimensions comprising 14 indicators:

- **TPACK** (7 indicators): Technology Knowledge (TK), Pedagogical Knowledge (PK), Content Knowledge (CK), Technological Pedagogical Knowledge (TPK), Technological Content Knowledge (TCK), Pedagogical Content Knowledge (PCK), and the integrative TPACK component.
- **STEM** (4 indicators): Science content integration (S), Technology application (T), Engineering design process (E), and Mathematical reasoning (M).
- **ESD** (3 indicators): ESD-Pedagogical Content Knowledge (ESD-PCK), ESD-Inquiry (ESD-INQ), and ESD-Evaluative thinking (ESD-EVA).

Composite scores for each dimension were calculated as the mean of its constituent indicators. The overall integrative lesson plan quality score (RPPInt_total) was calculated as the grand mean across all 14 indicators, operationalizing integrative lesson plan quality as a composite of the three dimensions. The rubric was developed through expert judgment involving three science education specialists and demonstrated adequate content validity.

#### 3.4.2 PjBL Implementation Observation Instrument

The quality of PjBL implementation was measured using a five-item observation instrument, with each item scored on a 1--4 scale corresponding to the five PjBL stages. The instrument was completed by course instructors who observed the implementation process. During data screening, one item (PjBL05, corresponding to the presentation and reflection stage) was excluded from the SEM analysis because it exhibited zero variance---all 95 participants received the maximum score of 4, providing no discriminating information. The remaining four items (PjBL01--PjBL04) were retained for the structural model.

### 3.5 Data Collection Procedure

Data collection followed a three-phase timeline: (a) pretest, in which participants designed an initial lesson plan that was scored using the integrative rubric; (b) the PjBL intervention, during which PjBL implementation quality was observed and scored; and (c) posttest, in which participants designed a second lesson plan under the same conditions, scored by the same assessors using the identical rubric. Lesson plans were anonymized before scoring to reduce assessor bias.

### 3.6 Data Analysis

Data analysis proceeded in two phases corresponding to the research questions.

#### 3.6.1 Phase 1: Pre-Post Comparison (RQ1)

To address RQ1, which examined changes in integration competences before and after the PjBL intervention, the following analyses were conducted:

- **Descriptive statistics** (mean, standard deviation, minimum, maximum) were computed for each construct and indicator at pretest and posttest.
- **Normality testing** was performed using the Shapiro-Wilk test on the difference scores (posttest minus pretest) for each construct, given the sample size of N = 95.
- **Paired inferential tests** were applied based on normality results: the paired-samples t-test for constructs with normally distributed difference scores, and the Wilcoxon signed-rank test for constructs violating the normality assumption. The significance level was set at alpha = .05.
- **Effect sizes** were calculated using Cohen's *d* for parametric tests and rank-biserial correlation *r* for non-parametric tests. Effect sizes were interpreted following Cohen (1988): small (d = 0.2), medium (d = 0.5), and large (d = 0.8).
- **Normalized gain (N-Gain)** was calculated using Hake's (1998) formula: N-Gain = (post - pre) / (max - pre), where max = 4 (the maximum rubric score). N-Gain values were categorized as High (> 0.7), Medium (0.3--0.7), or Low (< 0.3).

All Phase 1 analyses were conducted in Python 3.11 using pandas, scipy, and pingouin.

#### 3.6.2 Phase 2: Structural Equation Modeling (RQ2--RQ5)

To address RQ2 through RQ5, Partial Least Squares Structural Equation Modeling (PLS-SEM) was employed. PLS-SEM was selected over covariance-based SEM (CB-SEM) for several reasons: (a) the study's exploratory-confirmatory nature, testing a novel integrative model for the first time; (b) the inclusion of a single-indicator construct (RPPInt_total_post for the RPP construct); (c) the modest sample size (N = 95), which is adequate for PLS-SEM but may be insufficient for CB-SEM with the specified model complexity; and (d) PLS-SEM's capacity to handle non-normal data and formative measurement (Hair et al., 2022).

**Model specification.** The structural model comprised five constructs: PjBL (exogenous), TPACK, STEM, ESD, and RPP (endogenous). All constructs were specified as reflective (Mode A). The structural paths included seven relationships: PjBL -> TPACK, PjBL -> STEM, PjBL -> ESD, PjBL -> RPP (direct), TPACK -> RPP, STEM -> RPP, and ESD -> RPP. The RPP construct was operationalized as a single-indicator construct using the composite integrative lesson plan quality score (RPPInt_total_post), with the indicator's loading fixed to 1.000. The data matrix for the SEM analysis used posttest scores for TPACK, STEM, ESD, and RPP, and the PjBL observation scores, yielding 19 manifest variables.

**Measurement model evaluation.** The outer (measurement) model was assessed using standard PLS-SEM criteria (Hair et al., 2022):

- *Indicator reliability:* outer loadings >= 0.708 (indicators between 0.40 and 0.70 were retained if their removal did not improve AVE or CR, following Hair et al.'s recommendation for exploratory research).
- *Convergent validity:* Average Variance Extracted (AVE) >= 0.50.
- *Internal consistency reliability:* Composite Reliability (CR) >= 0.70 and Cronbach's alpha >= 0.70.
- *Discriminant validity:* Heterotrait-Monotrait ratio (HTMT) < 0.90 (Henseler et al., 2015), supplemented by the Fornell-Larcker criterion.

**Structural model evaluation.** The inner (structural) model was assessed through:

- *Path coefficients (beta):* standardized regression coefficients indicating the strength and direction of structural relationships.
- *Statistical significance:* determined through bootstrapping (5,000 iterations) with bias-corrected 95% confidence intervals. A unified manual bootstrap procedure was employed, in which each bootstrap resample simultaneously yielded path coefficients and indirect effects, ensuring consistency across direct and mediation analyses.
- *Coefficient of determination (R-squared):* proportion of variance in endogenous constructs explained by the model. Interpreted as substantial (0.75), moderate (0.50), or weak (0.25) (Hair et al., 2022).
- *Effect size (f-squared):* the incremental impact of each exogenous construct on an endogenous construct. Interpreted as small (0.02), medium (0.15), or large (0.35) (Cohen, 1988).
- *Predictive relevance (Q-squared):* assessed through blindfolding (Stone-Geisser's procedure via k-fold cross-validation, k = 7). Values above zero indicate predictive relevance.

**Mediation analysis (RQ5).** Indirect effects were calculated as the product of constituent path coefficients (e.g., indirect effect of PjBL on RPP through TPACK = beta_PjBL->TPACK x beta_TPACK->RPP). Statistical significance of indirect effects was determined through the bootstrap confidence interval method (Preacher & Hayes, 2008): an indirect effect was deemed significant if the 95% bias-corrected confidence interval did not include zero. The Sobel test was additionally computed as a cross-check. The Variance Accounted For (VAF) was calculated to classify mediation type: full mediation (VAF > 80%), partial mediation (20% < VAF < 80%), or no mediation (VAF < 20%) (Hair et al., 2022).

**Comparative analysis (RQ3).** The relative influence of PjBL on each integration dimension was assessed by comparing path coefficients and their associated f-squared values. Bootstrap confidence intervals were examined for overlap to determine whether observed differences were statistically meaningful.

**Software.** PLS-SEM analysis was conducted using the plspm Python package (version 0.5.7) with a random seed of 42 for reproducibility. All bootstrap procedures used 5,000 iterations with a single-process configuration to ensure deterministic execution. Figures were generated using matplotlib.
