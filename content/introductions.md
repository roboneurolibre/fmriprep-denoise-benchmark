# Introductions
<!-- aim at 500 words -->

<!-- We all know denosiing is important now. And we cannot understand brain activity without it. -->
Analysing brain activity observed through functional magnetic resonance imaging (fMRI) is a challenging task. 
Unwanted signal distortion introduced by non-neuronal sources, 
such as head motion, scanner noise, cardiac and repiratory artifacts, <!-- cite a review here -->
is entangled with the spontaneous fluctuations in the blood oxygenation level dependent (BOLD) signal.
These source of noise, known as confounds or nuisance regressors, pose a major challenge in relevant analytic approaches.
A primary method in understanding functional brain individual differences is resting state functional connectivity.
It has been used to study a wide range of neurodegenerative and psychiatric diseases as well as differences in cognitive function across the healthy population.
When functional connectivity is contaminated with motion, it can lead to altered network structure {cite:p}`power_scrubbing_2012`.
Many patient populations exhibit significantly more motion in the MRI scanner than the healthy controls. <!-- reference here -->
Therefore, in functional connectivity based analysis, reducing the impact of confounds, known as denosing, is an major compoenent of the workflow.

<!-- Classes of nuisance regressors - like how load_confounds separate them -->
<!-- need to add reference to this section-->
## Types of noise regressors

To minimize impact of confounds, 
the most common method in functional connectivity analysis is performing a linear regression using the nuisance regressors to model the signals.
The residual of the linear regression will be the denoised signal for the subsequent analysis.
The nuisance regressors are separated into a few classes, capturing different type of non-neuronal noises.
__Temporal high-pass filtering__ accounts low-frequency signal drifts introduced by _physiological and scanner noise sources_.
__Head motion__ is captured by _6 rigid-body motion parameters_ (3 translations and 3 rotation)  estimated relative to a reference image.
__Non-grey matter tissue signal__, including _white matter_ and _cerebrospinal fluid_, are unlikely to include signal related to neuronal activity. 
They are captured by averaging signal within the anatomically-derived masks.
__Global signal__ is calculated by averaging signal within the _full brain_ mask.
All these four classes of regressors can be expanded to their first temporal derivatives and their quadratic terms {cite:p}`satterthwaite_2013`.
Principle componenet based method __CompCor__ extracts principal components from white matter and cerebrospinal fluid masks to estimate non-neuronal activity. 
Independent component analysis based method, __ICA-FIX__ and __ICA-AROMA__,
estimate independent component time series related to head-motion through a priori heuristics (ICA-AROMA) or a data-driven classifier. 
Different strategy has there own strength and benefits and often involves combining a few classes of regressors described above.
These regressors are regressed out from the signal after basic processing steps (see fMRIPrep) with linear regression. 
All the subsequent analysis performs on the redisual signal after the regression step.

## Implementation of denoising step

<!-- How denoising is traditionally done in propriatory software -->
This was less of an issue when users use preprocessing software with statistical modelling functionality.
Each of these software would implement their own preferred strategy, 
For instence, FSL added the motion parameters by default, and provided option to run ICA-AROMA.
The noise regressors would be preselect and avoid user intervention here.
However, when users wants to use additional regressors, the processes can be complicated.
With the recent benchmark papers on confound denoising, 
it's not uncommon for users wanting to adding parameters other than the native options from a given software.
In the FSL example, if user wants to use unsupported strategy, such as CompCor, 
they will have to calculate the regressors and inject to the workflow manually. 
<!-- Question: should we compare some other software? ie. niak and cpac has a more flexible approach, but still lock user-in  -->

Recent rise of minimal preprocessing pipelines fMRIPrep {cite:p}`esteban_fmriprep_2020` has address the confound regressor issue from a different angle.
fMRIprep aims to standardize the established steps of fMRI preprocessing, including registration, slice timing correction, motion correction, and distortion correction.
Their approach leaves the choice of denoising and spatial smoothing to users.
Instead of generating a small subset of confound regressors, fMRIPrep calculate a wide range of noise regressors that can be extracted from the fMRI data.
The benefit of this approach is that the generation of these regressors are standardised and accessible from the same source,
several issues related how users select the regressors for the denoisng step still remains.
A common concern is that users might not be familiar with the denoising literature or the fMRIprep documentation, 
leading to potentially selecting regressors that are not competible (e.g. applying melodic ICA components to the ICA-AROMA output), 
or missing regressors that should be used together (e.g. discrete cosine-basis regressors should always be applied with CompCor components),
resulting in reintroducing noises into the data or suboptimal denoising results.
In addition, there's no standard way of tracking the choice of denoising regressors.
Users can implement project-specific ways to retrieve the relevant regressors, 
making replication of others denoising step more difficult.
Lastly, the past denoising benchmark literature was performed on the study specific preprocessing pipeline.
The validity of these results on fMRIPrep has yet to be examined. 

## Aim of the benchmark

Current work aims to introduce an application programming interface (API) to standardise the interaction with fMRIPrep and provide benchmark using functional connectivity generated from resting state data.
The API is released under popular Python neuroimaging analytic library `nilearn`, 
with the aim to maximise the exposure of the API to the larger Python fMRI community.
The benchmark will provide a useful reference for fMRIPrep users by systematically evaluating the impact of common denoising strategies and select the best approach for their dataset.  