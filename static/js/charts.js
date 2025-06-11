// Initialize category bar chart
function initCategoryChart(chartData) {
  if (!chartData || !chartData.length) return;
  
  const labels = chartData.map(row => row.category);
  const counts = chartData.map(row => row.count);

  const ctx = document.getElementById('categoryChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Category Count',
        data: counts,
        backgroundColor: '#1474b8'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.raw}`;
            }
          },
          titleFont: { size: 18 },
          bodyFont: { size: 16 }
        }
      },
      scales: {
        x: {
          ticks: {
            font: { size: 15, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          },
          title: {
            display: true,
            text: 'UNSPSC Category Name',
            font: { size: 22, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          }
        },
        y: {
          ticks: {
            font: { size: 16, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          },
          title: {
            display: true,
            text: 'Counts',
            font: { size: 22, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          }
        }
      }
    }
  });
}

// Initialize amount bar chart
function initAmountChart(amountData) {
  if (!amountData || !amountData.length) return;
  
  const labels = amountData.map(row => row.category);
  const values = amountData.map(row => row.amount);

  const ctx = document.getElementById('amountBarChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Amount',
        data: values,
        backgroundColor: '#30A3DA'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.raw}`;
            }
          },
          titleFont: { size: 18 },
          bodyFont: { size: 16 }
        }
      },
      scales: {
        x: {
          ticks: {
            font: { size: 15, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          },
          title: {
            display: true,
            text: 'Spend Amount ($)',
            font: { size: 22, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          }
        },
        y: {
          ticks: {
            font: { size: 16, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          },
          title: {
            display: true,
            text: 'Supplier',
            font: { size: 22, family: 'Arial', weight: 'bold' },
            color: '#3a3a6a'
          }
        }
      }
    }
  });
}

// Initialize category pie chart
function initCategoryPieChart(pieData) {
  if (!pieData || !pieData.length) return;
  
  const labels = pieData.map(row => row.category);
  const counts = pieData.map(row => row.count);
  const blueShades = [
    'rgba(54, 162, 235, 0.15)',
    'rgba(54, 162, 235, 0.9)',
    '#30A3DA',
    '#163E93',
    '#051C2A'
  ];

  const ctx = document.getElementById('categoryPieChart').getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Top 5 Category Count',
        data: counts,
        backgroundColor: blueShades
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          labels: { font: { size: 30 } }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.raw}`;
            }
          },
          titleFont: { size: 30, family: 'Arial', weight: 'bold' },
          bodyFont: { size: 20, family: 'Arial', weight: 'normal' }
        }
      }
    }
  });
}

// Initialize confidence pie chart
function initConfidencePieChart(confidenceData) {
  if (!confidenceData || !confidenceData.length) return;
  
  const labels = confidenceData.map(row => row.category);
  const counts = confidenceData.map(row => row.count);
  const colors = ['#30A3DA', '#163E93', '#051C2A', '#1474b8', '#3a3a6a'];

  const ctx = document.getElementById('confidencePieChart').getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Confidence Distribution',
        data: counts,
        backgroundColor: colors
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          labels: { font: { size: 30 } }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.label}: ${context.raw}`;
            }
          },
          titleFont: { size: 30, family: 'Arial', weight: 'bold' },
          bodyFont: { size: 20, family: 'Arial', weight: 'normal' }
        }
      }
    }
  });
}

// Initialize all charts when the page loads
document.addEventListener('DOMContentLoaded', function() {
  // Get chart data from the page
  const chartData = JSON.parse(document.getElementById('chartData').textContent || '[]');
  const amountData = JSON.parse(document.getElementById('amountData').textContent || '[]');
  const pieData = JSON.parse(document.getElementById('pieData').textContent || '[]');
  const confidenceData = JSON.parse(document.getElementById('confidenceData').textContent || '[]');

  // Initialize each chart
  initCategoryChart(chartData);
  initAmountChart(amountData);
  initCategoryPieChart(pieData);
  initConfidencePieChart(confidenceData);
}); 