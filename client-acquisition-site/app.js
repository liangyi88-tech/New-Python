const fallbackCompanies = [
  {
    name: "Greif",
    country: "Malaysia",
    city: "Shah Alam",
    recentJobs: 16,
    productionShare: 0.69,
    logisticsShare: 0.18,
    recencyDays: 5,
    source: "Public jobs / careers signals",
    summary:
      "Strong operations and plant hiring suggests packaging and industrial throughput expansion in Malaysia.",
  },
  {
    name: "SCGM Berhad",
    country: "Malaysia",
    city: "Kulai",
    recentJobs: 12,
    productionShare: 0.74,
    logisticsShare: 0.11,
    recencyDays: 7,
    source: "Public jobs / careers signals",
    summary:
      "Manufacturing and shift-based openings indicate active production demand with local packaging relevance.",
  },
  {
    name: "Daibochi",
    country: "Malaysia",
    city: "Melaka",
    recentJobs: 11,
    productionShare: 0.72,
    logisticsShare: 0.14,
    recencyDays: 8,
    source: "Public jobs / careers signals",
    summary:
      "Hiring mix points to capacity support across flexible packaging and plant execution roles.",
  },
  {
    name: "Dynapack Asia",
    country: "Singapore",
    city: "Singapore",
    recentJobs: 9,
    productionShare: 0.62,
    logisticsShare: 0.2,
    recencyDays: 6,
    source: "Public jobs / careers signals",
    summary:
      "Regional packaging footprint and fresh hiring activity suggest near-term operating momentum.",
  },
  {
    name: "Kimball Electronics",
    country: "Malaysia",
    city: "Penang",
    recentJobs: 18,
    productionShare: 0.66,
    logisticsShare: 0.17,
    recencyDays: 4,
    source: "Public jobs / careers signals",
    summary:
      "Electronics manufacturing ramp indicators can correlate with stronger industrial packaging requirements.",
  },
  {
    name: "V.S. Industry",
    country: "Malaysia",
    city: "Senai",
    recentJobs: 14,
    productionShare: 0.71,
    logisticsShare: 0.15,
    recencyDays: 9,
    source: "Public jobs / careers signals",
    summary:
      "High proportion of production and plant roles suggests throughput support and supplier opportunity.",
  },
  {
    name: "Vinda Singapore",
    country: "Singapore",
    city: "Singapore",
    recentJobs: 7,
    productionShare: 0.48,
    logisticsShare: 0.28,
    recencyDays: 10,
    source: "Public jobs / careers signals",
    summary:
      "Consumer goods hiring is moderate but distribution support roles may imply increased packaging movement.",
  },
  {
    name: "Briggs Packaging",
    country: "Malaysia",
    city: "Johor Bahru",
    recentJobs: 8,
    productionShare: 0.64,
    logisticsShare: 0.19,
    recencyDays: 11,
    source: "Public jobs / careers signals",
    summary:
      "Consistent operational hiring makes this a relevant target for packaging supply conversations.",
  },
];

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function scoreCompany(company) {
  const hiringScore = clamp(company.recentJobs / 20, 0, 1) * 45;
  const productionScore = company.productionShare * 30;
  const logisticsScore = company.logisticsShare * 10;
  const recencyScore = clamp((30 - company.recencyDays) / 30, 0, 1) * 10;
  const regionScore = ["Singapore", "Malaysia"].includes(company.country) ? 5 : 0;
  const total = Math.round(hiringScore + productionScore + logisticsScore + recencyScore + regionScore);

  return {
    ...company,
    score: total,
    outlook: total >= 75 ? "High" : total >= 55 ? "Medium" : "Low",
  };
}

let scoredCompanies = fallbackCompanies.map(scoreCompany).sort((a, b) => b.score - a.score);

const leadTableBody = document.getElementById("leadTableBody");
const companyCards = document.getElementById("companyCards");
const searchInput = document.getElementById("searchInput");
const regionFilter = document.getElementById("regionFilter");
const topCompany = document.getElementById("topCompany");
const topSignal = document.getElementById("topSignal");
const companyCount = document.getElementById("companyCount");
const averageScore = document.getElementById("averageScore");

function scoreClass(score) {
  if (score >= 75) return "high";
  if (score >= 55) return "medium";
  return "low";
}

function renderSummary(data) {
  const best = data[0] || scoredCompanies[0];
  const avg = data.length
    ? Math.round(data.reduce((sum, company) => sum + company.score, 0) / data.length)
    : 0;

  topCompany.textContent = best ? best.name : "No companies";
  topSignal.textContent = best
    ? `${best.recentJobs} recent jobs, ${Math.round(best.productionShare * 100)}% production-role share`
    : "No matching signals";
  companyCount.textContent = String(data.length);
  averageScore.textContent = String(avg);
}

function renderTable(data) {
  if (!data.length) {
    leadTableBody.innerHTML =
      '<tr><td colspan="6" class="empty-state">No companies match the current filter.</td></tr>';
    return;
  }

  leadTableBody.innerHTML = data
    .map((company) => {
      const level = scoreClass(company.score);
      return `
        <tr>
          <td><strong>${company.name}</strong></td>
          <td>${company.country}</td>
          <td>${company.recentJobs}</td>
          <td>${Math.round(company.productionShare * 100)}%</td>
          <td><span class="score-pill score-${level}">${company.score}</span></td>
          <td><span class="outlook-pill outlook-${level}">${company.outlook}</span></td>
        </tr>
      `;
    })
    .join("");
}

function renderCards(data) {
  if (!data.length) {
    companyCards.innerHTML = "";
    return;
  }

  companyCards.innerHTML = data
    .map((company) => {
      const level = scoreClass(company.score);
      return `
        <article class="company-card">
          <div class="card-meta">
            <span class="meta-chip">${company.country}</span>
            <span class="meta-chip">${company.city}</span>
            <span class="score-pill score-${level}">Score ${company.score}</span>
          </div>
          <h3>${company.name}</h3>
          <p>${company.summary}</p>
          <div class="card-stats">
            <div class="card-stat">
              <span>Recent jobs</span>
              <strong>${company.recentJobs}</strong>
            </div>
            <div class="card-stat">
              <span>Production share</span>
              <strong>${Math.round(company.productionShare * 100)}%</strong>
            </div>
            <div class="card-stat">
              <span>Freshness</span>
              <strong>${company.recencyDays}d</strong>
            </div>
          </div>
          <p><strong>Source:</strong> ${company.source}</p>
          <p><strong>Outlook:</strong> ${company.outlook} probability of manufacturing volume increase based on hiring activity.</p>
        </article>
      `;
    })
    .join("");
}

function applyFilters() {
  const query = searchInput.value.trim().toLowerCase();
  const region = regionFilter.value;

  const filtered = scoredCompanies.filter((company) => {
    const matchesQuery =
      !query ||
      company.name.toLowerCase().includes(query) ||
      company.country.toLowerCase().includes(query) ||
      company.city.toLowerCase().includes(query);

    const matchesRegion = region === "all" || company.country === region;

    return matchesQuery && matchesRegion;
  });

  renderSummary(filtered);
  renderTable(filtered);
  renderCards(filtered);
}

async function loadCompanies() {
  try {
    const response = await fetch("./leads.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Unable to load leads.json: ${response.status}`);
    }

    const remoteCompanies = await response.json();
    if (!Array.isArray(remoteCompanies) || !remoteCompanies.length) {
      throw new Error("Lead data is empty or invalid.");
    }

    scoredCompanies = remoteCompanies.map(scoreCompany).sort((a, b) => b.score - a.score);
  } catch (error) {
    console.warn("Using fallback lead data.", error);
    scoredCompanies = fallbackCompanies.map(scoreCompany).sort((a, b) => b.score - a.score);
  }

  applyFilters();
}

searchInput.addEventListener("input", applyFilters);
regionFilter.addEventListener("change", applyFilters);

loadCompanies();

// Auto-refresh data every 24 hours
setInterval(loadCompanies, 24 * 60 * 60 * 1000);
console.log("Data will refresh automatically every 24 hours");
