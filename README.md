# Lido Reporting
![GitHub all releases](https://img.shields.io/github/downloads/Steakhouse-Financial/lido-reports/total?style=for-the-badge)![GitHub pull requests](https://img.shields.io/github/issues-pr/Steakhouse-Financial/lido-reports?style=for-the-badge)![GitHub forks](https://img.shields.io/github/forks/Steakhouse-Financial/lido-reports?style=for-the-badge)![GitHub Repo stars](https://img.shields.io/github/stars/Steakhouse-Financial/lido-reports?style=for-the-badge)![GitHub last commit](https://img.shields.io/github/last-commit/Steakhouse-Financial/lido-reports?style=for-the-badge)

-- Description goes here

## Components
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg?style=for-the-badge)](https://www.python.org/downloads/release/python-360/) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

## 🔧 How to Install

### 🐳 Docker


```bash
git clone https://github.com/Steakhouse-Financial/lido-reports.git
cd lido-reports
docker run -d --restart=always -p 8000:8000 -v ./lido:/lido --name lido_reports louislam/uptime-kuma:1
```
Lido reports is now running on http://localhost:8000

### 🐳 Docker-Compose
```bash
git clone https://github.com/Steakhouse-Financial/lido-reports.git
cd lido-reports
docker run -d --restart=always -p 8000:8000 -v ./lido:/lido --name lido_reports louislam/uptime-kuma:1
```
Lido reports is now running on http://localhost:8000