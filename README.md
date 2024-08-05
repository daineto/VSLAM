# About VSLAM

VSLAM is an online algorithm for Action Model Learning with full observability. VSLAM leverages Version Space Learning to compute a compact representation of all action models consistent with a set of demonstrations. The output of VSLAM can be used to build models that are guaranteed to be sound or complete w.r.t. the true model.

For more details, please read the paper at <https://arxiv.org/abs/2404.09631> (accepted in KR2024) 

# Contents

This commit contains a python implementation of VSLAM, as well as all the code used for the empirical evaluation included in the KR2024 paper. It also includes an Appendix, containing the full proofs of the lemmas that were only sketched in the paper alongside some additional results.  

Structure of the repository:
1. The benchmarks folder contains the domains and problems used for our experiments.
2. The appendix folder contains the appendix of the KR2024 paper.
3. The "Evaluation" and "Evaluation FAMA" notebooks have instructions to reproduce our results of Figure 3. 
   Generated data from the experiments is stored in the respective domain folder as csv.
4. The "Sample Analysis" notebook has instructions to reproduce our results of Figure 2.
5. The "Figures" notebook generates Figure 2 and Figure 3
6. VSLAM.py contains the main code of our algorithm.

When time allows, we will reformat the code into a pip package and document it better.

# Installation

VSLAM is built on top of the Unified Planning Framework (https://github.com/aiplan4eu/unified-planning)

To run this code install python 3.10 and the libraries in "requirements.txt"

