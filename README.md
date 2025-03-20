## Domain Adaptive Object Detection for Autonomous Driving Under Foggy Weather
This repository contains the implementation of a domain-adaptive object detection framework based on Faster R-CNN for improving object detection performance in foggy weather conditions.

## Project Overview
Autonomous vehicles face significant challenges when navigating through adverse weather conditions, such as fog, which can obscure objects and reduce the accuracy of object detection systems. Most object detection models are trained on data from clear weather conditions and struggle to maintain performance under different environmental conditions due to domain shifts.
Our project implements a domain adaptation approach that addresses this domain gap to ensure the robustness and reliability of autonomous driving systems in foggy conditions without requiring extensive labeled data from these adverse environment

The project is based on Faster R-CNN architecture and evaluated on Cityscapes (source domain) and Foggy Cityscapes (target domain) datasets.

## Environment Setup
```sh
git clone git@github.com:emapendo/Domain-Adaptive-Object-Detection.git
cd domain-adaptive-object-detection

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt # Install dependencies
```

## Dataset Preparation

## 📂 Project Structure
```sh

```