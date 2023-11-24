# CS445_Final_Project

This project was finished by Han Chen (hanc7), Daniel Zhuang, Eric Jin (ericjin2).


We created a single-image dezaher based on the approaches of “Single Image Haze Removal Using Dark Channel Prior” by He et al. (referred to as “paper 1” in this report) for land dehazing and “A Retinex-Based Enhancing Approach for Single Underwater Image” by Fu et al. (“paper 2”) for underwater dehazing. We trained a neural network to classify if an input image is on land or underwater. Based on its classification, we would run the appropriate algorithm implementation to reduce the fog of the image. We also used methods described in “Blind Contrast Enhancement Assessment by Gradient Ratioing at Visible Edges” by Hautiér et al. (“paper 3”) to evaluate the effectiveness of our dehazing method.