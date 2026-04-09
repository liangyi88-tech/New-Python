# VolumeSignal

VolumeSignal is a lightweight client acquisition website for identifying manufacturing companies in Singapore and Malaysia that may be increasing production volume.

## What it does

- Presents a polished landing page for industrial packaging prospecting
- Shows a lead dashboard focused on hiring-based expansion signals
- Scores companies based on:
  - recent job posting volume
  - production-role share
  - logistics-role share
  - posting recency
  - Singapore/Malaysia relevance
- Loads lead data from `leads.json`
- Falls back to built-in sample data if external loading fails

## Files

- `index.html` – page structure
- `styles.css` – website styling
- `app.js` – filtering, scoring, rendering, and data loading
- `leads.json` – editable lead dataset

## How to use

### Option 1: Open directly
Open `index.html` in a browser.

Note: some browsers block `fetch()` from local `file://` paths. If that happens, the site will still render using fallback in-memory data.

### Option 2: Run a simple local server
If Python is available:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/client-acquisition-site/
```

## Editing the lead list

Update `leads.json` with objects in this format:

```json
{
  "name": "Company Name",
  "country": "Singapore",
  "city": "Singapore",
  "recentJobs": 10,
  "productionShare": 0.65,
  "logisticsShare": 0.18,
  "recencyDays": 6,
  "source": "Public jobs / careers signals",
  "summary": "Short explanation of why this company may be increasing production."
}
```

## Notes on live data

This MVP is structured to support public-source hiring intelligence. For a more advanced version, the next step would be adding a backend collector that periodically refreshes `leads.json` from scrape-friendly public job pages and company careers sites.

## Current limitations

- Uses seed data rather than a full automated live collection backend
- Does not directly scrape restricted platforms
- Scoring is heuristic and intended for lead prioritization, not guaranteed production forecasts
