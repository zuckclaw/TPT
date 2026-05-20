# TikTok Shadowban Research Toolkit

A specialized Python-based toolkit designed for reverse engineering and analyzing TikTok's shadowban mechanisms. This project aims to observe how specific behavioral patterns (bot-like activity, content duplication, etc.) affect account visibility and reach.

> **Disclaimer**: This project is for educational and research purposes only. Using automation on TikTok may violate their Terms of Service and lead to account suspension. Use responsibly and only on research-dedicated accounts.

## Core Features

- **Automated Research Core**: Robust session management with browser-mimicking headers.
- **Shadowban Monitoring**: Real-time tracking of search visibility and video performance metrics.
- **Experimental Triggers**: Pre-defined scenarios to simulate behaviors known to trigger shadowbans.
- **Bulk Content Management**: Automated retrieval and mass deletion of profile videos.
- **Data Analytics**: Post-experiment analysis tools that generate visual reports (graphs) of reach and status changes.

## Prerequisites

- Python 3.8+
- `requests` library
- `matplotlib` (for data analysis)

```bash
pip install requests matplotlib
```

## Setup

1. Clone this repository.
2. Log in to TikTok in your web browser.
3. Open Developer Tools (F12) > Application > Cookies.
4. Create a `config.json` file in the project root with the following structure:

```json
{
   "sessionid": "your_sessionid",
   "tt_csrf_token": "your_csrf_token",
   "uid_tt": "your_uid_tt",
   "ttwid": "your_ttwid",
   "msToken": "your_mstoken"
}
```

5. Verify your session:
```bash
python setup_session.py
```

## Usage

### 1. Recording Baseline
Before starting an experiment, record the initial state of the account:
```bash
python baseline.py
```

### 2. Running Experiments
Execute specific behavioral scenarios to observe algorithmic responses:
```bash
python trigger_shadowban.py
```

### 3. Monitoring
Run a background monitor to track visibility changes:
```bash
python monitor_shadowban.py <username> <video_id>
```

### 4. Automated Content Deletion
Quickly clear profile content (useful for resetting research accounts or testing mass-deletion impact):
```bash
python bulk_delete.py
```

### 5. Analyzing Results
Generate visual reports from your experiment logs:
```bash
python analyze_results.py
```

## Project Structure

- `tiktok_research.py`: Core library containing API interaction logic.
- `setup_session.py`: Handles authentication and session verification.
- `trigger_shadowban.py`: Interactive script for running research scenarios.
- `monitor_shadowban.py`: Real-time monitoring and logging.
- `baseline.py`: Records initial metrics for comparison.
- `bulk_delete.py`: Automated video listing and mass deletion.
- `analyze_results.py`: Data visualization and summary generator.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
