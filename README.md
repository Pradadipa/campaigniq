# 🎯 CampaignIQ

**AI-Powered Multi-Agent Marketing Analytics System**

CampaignIQ is an intelligent marketing analytics platform that uses multiple AI agents to analyze campaign performance, generate actionable insights, and create executive-ready reports automatically.

---

## 🌟 Features

### **Multi-Agent Architecture**
- **Agent 1: Data Ingestion** - Validates and prepares campaign data
- **Agent 2: Performance Analyzer** - Calculates KPIs and identifies trends
- **Agent 3: Insight Generator** - Uses GPT-4 Mini to generate business insights
- **Agent 5: Dashboard Builder** - Creates interactive Streamlit visualizations
- **Agent 6: Report Composer** - Generates professional written reports

### **Comprehensive Outputs**
- 📊 Interactive Streamlit dashboard with performance visualizations
- 💡 AI-powered insights with prioritized recommendations
- 📄 Executive reports in multiple formats (summary, detailed, action plan, client-facing)
- 📈 Weekly trend analysis with ad fatigue detection
- 🎯 Platform and creative performance comparisons

### **Realistic Data Patterns**
- Ad fatigue modeling (performance decline over time)
- Learning phase simulation (first week optimization)
- Day-of-week behavioral patterns
- Creative performance variance
- Platform-specific characteristics

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.9+
- OpenAI API key

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/campaigniq.git
cd campaigniq
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### **Run Complete Pipeline**
```bash
python run_campaigniq.py
```

This will:
1. Generate synthetic campaign data (30 days, 3 platforms)
2. Validate and process data
3. Analyze performance metrics
4. Generate AI insights (requires OpenAI API)
5. Prepare dashboard
6. Create executive reports

**Time:** ~3-5 minutes

### **View Interactive Dashboard**
```bash
streamlit run dashboard_app.py
```

Opens in browser at `http://localhost:8501`

---

## 📁 Project Structure
```
campaigniq/
├── data/
│   ├── raw/                    # Generated campaign data
│   ├── processed/              # Cleaned and analyzed data
│   └── outputs/
│       └── reports/            # Generated reports
├── src/
│   ├── agents/                 # All agent modules
│   │   ├── data_ingestion.py
│   │   ├── performance_analyzer.py
│   │   ├── insight_generator.py
│   │   ├── dashboard_generator.py
│   │   └── report_composer.py
│   └── utils/
│       └── data_generator.py   # Synthetic data creator
├── config.yaml                 # Campaign configuration
├── run_campaigniq.py          # Master pipeline script
├── dashboard_app.py           # Dashboard entry point
└── requirements.txt
```

---

## 📊 Sample Outputs

### **Dashboard**
Interactive visualizations including:
- Executive KPI summary cards
- Weekly performance trends
- Platform comparison charts
- Creative performance rankings
- AI-generated insights display

### **Reports**
- **Executive Summary** - 1-page overview for C-level
- **Detailed Analysis** - Comprehensive performance report
- **Action Plan** - Prioritized recommendations
- **Client Report** - Simplified for non-technical audiences

---

## 🛠️ Technology Stack

- **Language:** Python 3.9+
- **AI/ML:** OpenAI GPT-4 Mini
- **Data Processing:** Pandas, NumPy
- **Visualization:** Streamlit, Plotly
- **Data Generation:** Faker
- **Configuration:** YAML, python-dotenv

---

## 💡 Use Cases

- **Marketing Agencies:** Automate client reporting and campaign analysis
- **Startups:** Optimize limited marketing budgets with data-driven insights
- **Marketing Teams:** Identify underperforming creatives and platforms quickly
- **Analysts:** Generate comprehensive reports in minutes instead of hours

---

## 🎓 Key Insights CampaignIQ Provides

1. **Budget Efficiency**
   - Which platforms deliver best ROI
   - Budget reallocation opportunities
   - Cost optimization recommendations

2. **Creative Performance**
   - Top vs bottom performing creatives
   - Creative refresh timing
   - A/B test winners

3. **Ad Fatigue Detection**
   - When performance declines
   - Optimal creative refresh schedule
   - Audience saturation indicators

4. **Platform Optimization**
   - Cross-platform performance comparison
   - Platform-specific strategies
   - Day-of-week optimization

---

## 📈 Example Results

**From BaliGlow Campaign (30 days, $15K budget):**

- Generated **1.4M impressions** across 3 platforms
- Identified **TikTok as best performer** (6.47% CTR vs 1.46% Meta)
- Detected **18.9% CTR decline in Week 4** (ad fatigue)
- Recommended **$1,500 budget reallocation** for 20% efficiency gain
- **Saved 2-3 hours** of manual analysis time

---

## 🔧 Configuration

Edit `config.yaml` to customize:
- Campaign duration and budget
- Platform allocation percentages
- Target metrics (CPM, CTR benchmarks)
- Number of creatives per platform

---

## 📝 Development

### **Run Individual Agents**
```bash
# Test data generation
python generate_data.py

# Test Agent 1 (Data Ingestion)
python test_agent1.py

# Test Agent 2 (Performance Analyzer)
python test_agent2.py

# Test Agent 3 (Insight Generator)
python test_agent3.py

# Test Agent 6 (Report Composer)
python test_agent6.py
```

### **Run Dashboard Standalone**
```bash
streamlit run dashboard_app.py
```

---

## 💰 Cost Estimate

**OpenAI API Usage:**
- Agent 3 (Insights): ~$0.15 per run (5 API calls)
- Agent 6 (Reports): ~$0.20 per run (4 API calls)
- **Total per complete pipeline run: ~$0.35**

Using GPT-4 Mini for cost efficiency while maintaining quality.

---

## 🤝 Contributing

This is a portfolio project for demonstration purposes. Feel free to fork and adapt for your needs!

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Your Name**
- Portfolio: https://docs.google.com/presentation/d/1q-vn-f_uMjzUCKMxJuakJKf5QBvO4SEye53qxtgEE4U/edit
- LinkedIn: linkedin.com/in/prada-dipa-014284210
- Email: putu.pradadipa@gmail.com

---

## 🙏 Acknowledgments

- Built as part of marketing analytics portfolio project
- Uses OpenAI GPT-4 Mini for intelligent insights
- Inspired by real-world marketing analytics workflows

---

## 📞 Contact

Questions or feedback? Reach out via [email] or [LinkedIn]

---

**⭐ If you found this project interesting, please consider starring it!**