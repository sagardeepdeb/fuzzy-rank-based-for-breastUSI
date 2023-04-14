# Breast Ultra Sound Image Classification using fuzzy-rank-based ensemble network


## This repository contains code for the article Breast Ultrasound Image classification using fuzzy-rank-based ensemble network. The article is accepted for publication in Biomedical Signal Processing and Control, Elseivier. 

This section briefly introduces our proposed fuzzy-rank-based ensemble network. The same schematic diagram is given in followingfigure ![Figure 1](https://github.com/sagardeepdeb/fuzzy-rank-based-for-breastUSI/blob/main/block%20diagram.png) The main idea behind proposing a fuzzy-ensemble-based breast cancer detector is to use multiple customized base learners, each generating a confidence score for the presence of breast cancer. Using multiple base learners provides more robust and accurate results than relying on a single classifier. The fuzzy-ensemble approach then combines these confidence scores using fuzzy set theory, taking into account the uncertainty and variability in the scores. The resulting fuzzy-ensemble score is then used to make a final diagnosis. This approach aims to improve breast cancer detection's accuracy and reliability by utilizing the strengths of multiple classifiers and incorporating uncertainty in the final decision. The weights of the initial layers of four base learners are frozen, whereas the later layers are fine-tuned on the Ultrasound dataset we have used. The brief details about the base learners used are as follows.


As base learners, we have used four partially pre-trained Convolutional Neural Networks (CNN), namely VGG-Net, DenseNet, Xception, and Inception. These base classifiers have been pre-trained on the ImageNet dataset except for the last five layers. The last five layers of the base learners are fine-tuned on the BUSI dataset. The fusion approach employs a fuzzy ranking-based method where the probability scores from the base classifiers are transformed through three non-linear functions: an exponentially decaying function, the tanH function, and the Sigmoid function. The transformed scores are then used to assign ranks to the class probabilities. The exact process is repeated for each base classifier, and the rank products are added to obtain the final ranks. The aim of using three different non-linear functions with different concavities is to produce complementary results. The final decision is made by combining the multiple ranks associated with an identity and determining a new rank. The class with the lowest sum of rank products is considered the predicted class for the ensemble model. Using two ranks considers the closeness to and deviation from the expected result corresponding to the primary classification result, and the final rank normalizes the entire product. A higher confidence score results in a smaller value of the sum of rank products, indicating a better prediction. The following figure shows the operation suggested on a sample test image.

![Figure 2](https://github.com/sagardeepdeb/fuzzy-rank-based-for-breastUSI/blob/main/sample%20test%20image.png)

## Results

Conducting five-fold cross-validation using the base learners an accuracy of $77.69 \pm 3.22$, $83.23 \pm 3.14$, $78.31 \pm 2.27$, and $78.62 \pm 4.23$ were obtained. Furthermore, using the proposed fuzzy-rank-based model, an accuracy of $85.23 \pm 2.52$ is obtained. We have proved that the proposed fuzzy-rank-based ensemble network increases the classification performance. 

This repository is heavily inspired from https://github.com/Rohit-Kundu/Fuzzy-Rank-Ensemble


## Citation
Please cite our paper if you find the work useful: 
<pre>
  @article{deb2023breast,
  title={Breast UltraSound Image classification using fuzzy-rank-based ensemble network},
  author={Deb, Sagar Deep and Jha, Rajib Kumar},
  journal={Biomedical Signal Processing and Control},
  volume={85},
  pages={104871},
  year={2023},
  publisher={Elsevier}}
</pre>
