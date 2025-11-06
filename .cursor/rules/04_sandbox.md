# 🔒 Secure Sandbox

Executes generated code safely with process isolation.

### Implementation
- Runs in subprocess/Docker with time & memory limits.
- Whitelisted libs: pandas, numpy, matplotlib, plotly.
- Blocks all others.

### Output Format
```
{
  "stdout": "Execution OK",
  "chart_url": "/charts/chart_123.png",
  "summary": "Visualization ready."
}
```
