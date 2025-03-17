Domain Adaptive Object Detection for Autonomous Driving Under Foggy Weather
This repository contains the implementation of a domain-adaptive object detection framework based on Faster R-CNN for improving object detection performance in foggy weather conditions.

Project Overview
Autonomous vehicles face significant challenges when navigating through adverse weather conditions, such as fog, which can obscure objects and reduce the accuracy of object detection systems. Most object detection models are trained on data from clear weather conditions and struggle to maintain performance under different environmental conditions due to domain shifts.
Our project implements a domain adaptation approach that addresses this domain gap to ensure the robustness and reliability of autonomous driving systems in foggy conditions without requiring extensive labeled data from these adverse environment

Key Features
Implementation of Faster R-CNN with domain adaptation components
Image-level and object-level domain adaptations
Adversarial Gradient Reversal Layer (AdvGRL) for hard example mining
Domain-level metric regularization with auxiliary domain generation
Comprehensive evaluation and comparison with baseline methods
