# League of Legends Match Outcome Predictor 🎮🤖

A machine learning project that predicts League of Legends match outcomes based on champion picks, team composition, and player statistics. This project demonstrates the complete data science workflow from data collection to model deployment.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## 🎯 Project Overview

This project leverages machine learning to analyze League of Legends matches and predict outcomes with a target accuracy of 70%+. As a comprehensive data science portfolio project, it showcases:

- **Data Engineering**: API integration, ETL pipelines, data versioning
- **Data Science**: Exploratory analysis, feature engineering, statistical modeling
- **Machine Learning**: Classification models, hyperparameter tuning, model evaluation
- **MLOps**: Model versioning, experiment tracking, deployment

### Problem Statement

Can we predict the outcome of a League of Legends match based on:
- Champion selections (team compositions)
- Player historical performance
- Champion synergies and counter-picks
- Role assignments

### Business Value

- **Players**: Optimize champion picks in draft phase
- **Coaches**: Data-driven draft strategy recommendations
- **Analysts**: Understand meta trends and balance issues

## ✨ Features

### Current Implementation
- [x] Project structure setup
- [ ] Riot Games API integration
- [ ] Data collection pipeline
- [ ] Exploratory Data Analysis (EDA)
- [ ] Feature engineering
- [ ] Baseline model (Logistic Regression)
- [ ] Advanced models (Random Forest, XGBoost)
- [ ] Model evaluation and comparison
- [ ] REST API for predictions
- [ ] Interactive web dashboard

### Planned Enhancements
- [ ] Real-time prediction during draft phase
- [ ] Champion recommendation system
- [ ] Performance tracking over time
- [ ] Deep learning models (Neural Networks)

## 📊 Dataset

### Data Sources
- **Primary**: [Riot Games API](https://developer.riotgames.com/)
  - Match history data
  - Champion statistics
  - Player rankings and performance

### Data Volume
- **Target**: 50,000+ matches for training
- **Features**: ~100 engineered features
- **Update Frequency**: Weekly refreshes for current patch

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pip (Python package manager)
Riot Games API Key (free from developer.riotgames.com)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/lol-performance-predictor.git
cd lol-performance-predictor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your RIOT_API_KEY
```

### Quick Start

```bash
# 1. Collect data
python scripts/collect_data.py --matches 1000

# 2. Train model
python src/models/train.py --model xgboost

# 3. Make predictions
python src/api/predict.py --blue-team "Ahri,LeeSin,Darius,Jinx,Thresh" \
                          --red-team "Zed,Elise,Garen,Caitlyn,Blitzcrank"
```

## 📁 Project Structure

```
lol-performance-predictor/
│
├── src/
│   ├── data_collection/        # API clients and data fetching
│   ├── preprocessing/          # Data cleaning and transformation
│   ├── models/                 # ML models
│   ├── api/                    # Prediction API
│   ├── visualization/          # Plotting and dashboards
│   └── utils/                  # Helper functions
│
├── tests/                      # Unit and integration tests
├── data/                       # Data storage (gitignored)
│   ├── raw/                    # Raw API responses
│   ├── processed/              # Cleaned and featured data
│   └── models/                 # Saved model artifacts
│
├── notebooks/                  # Jupyter notebooks
├── scripts/                    # Utility scripts
├── docs/                       # Documentation
└── requirements.txt           # Python dependencies
```

## 🔬 Methodology

### Feature Engineering

**Champion-Level Features:**
- Champion win rates (global and by role)
- Champion mastery scores
- Recent performance (last 20 games)

**Team Composition Features:**
- Team synergy scores
- Counter-pick advantages
- Damage type balance (AP/AD ratio)
- Crowd control (CC) availability

**Player-Level Features:**
- Historical win rate
- Average KDA
- Rank/MMR
- Recent performance trend

## 📈 Expected Results

### Model Performance Targets

| Model                  | Expected Accuracy | Training Time |
|------------------------|-------------------|---------------|
| Logistic Regression    | 60-65%           | < 1 min       |
| Random Forest          | 68-73%           | 5-10 min      |
| XGBoost                | 70-75%           | 3-7 min       |

## 🛠️ Technology Stack

### Core Technologies
- **Language**: Python 3.8+
- **ML Libraries**: scikit-learn, XGBoost
- **Data Processing**: pandas, numpy
- **API Integration**: requests
- **Visualization**: matplotlib, seaborn, plotly

### Development Tools
- **Testing**: pytest
- **Notebooks**: JupyterLab
- **API Framework**: FastAPI / Flask

## 🎓 Learning Objectives

### Data Science Skills
✅ **Data Collection & ETL**
- REST API integration
- Data validation and quality checks

✅ **Machine Learning**
- Supervised learning (classification)
- Model selection and comparison
- Hyperparameter optimization

✅ **Software Engineering**
- Clean code principles
- Testing and documentation
- Version control

## 🚦 Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] Project setup and structure
- [ ] Riot API integration
- [ ] Basic data collection (1000 matches)
- [ ] Data exploration notebook

### Phase 2: Feature Engineering (Weeks 3-4)
- [ ] Champion statistics aggregation
- [ ] Team composition features
- [ ] Feature selection analysis

### Phase 3: Baseline Models (Week 5)
- [ ] Train/test split strategy
- [ ] Logistic Regression baseline
- [ ] Random Forest model

### Phase 4: Advanced Models (Week 6)
- [ ] XGBoost implementation
- [ ] Hyperparameter tuning
- [ ] Final model selection

### Phase 5: API & Deployment (Week 7)
- [ ] FastAPI development
- [ ] Model serving
- [ ] Dockerization

### Phase 6: Dashboard & Polish (Week 8)
- [ ] Interactive visualizations
- [ ] Documentation completion
- [ ] Portfolio presentation

## 📖 Resources & References

### Riot API Documentation
- [Riot Developer Portal](https://developer.riotgames.com/)
- [API Documentation](https://developer.riotgames.com/apis)

### Data Science Resources
- [scikit-learn Documentation](https://scikit-learn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

**Last Updated**: January 2026  
**Project Status**: 🟡 In Development  
**Version**: 0.1.0-alpha

---

*This project is not endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties.*
