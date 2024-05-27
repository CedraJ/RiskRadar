document.addEventListener('DOMContentLoaded', function() {
    // Function to update summary cards
    function updateSummaryCards(assets) {
        const totalRisks = assets.length;
        const highRisks = assets.filter(asset => asset.risk_level.toLowerCase() === 'high').length;
        const moderateRisks = assets.filter(asset => asset.risk_level.toLowerCase() === 'moderate').length;
        const lowRisks = assets.filter(asset => asset.risk_level.toLowerCase() === 'low').length;

        document.getElementById('total-risks').querySelector('p').textContent = totalRisks;
        document.getElementById('high-risks').querySelector('p').textContent = highRisks;
        document.getElementById('moderate-risks').querySelector('p').textContent = moderateRisks;
        document.getElementById('low-risks').querySelector('p').textContent = lowRisks;
    }

    // Function to update risk chart
    function updateRiskChart(assets) {
        const ctx = document.getElementById('riskChart').getContext('2d');
        const riskLevels = ['High', 'Moderate', 'Low'];
        const riskData = riskLevels.map(level => assets.filter(asset => asset.risk_level.toLowerCase() === level.toLowerCase()).length);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: riskLevels,
                datasets: [{
                    label: 'Number of Assets',
                    data: riskData,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(75, 192, 192, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                plugins: {
                    legend: {
                        display: false // Hide the legend
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Number of Assets'
                        },
                        ticks: {
                            stepSize: 1
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Risk Level'
                        }
                    }
                }
            }
        });
    }

    // Function to populate risk register table
    function populateRiskRegister(assets) {
        const tbody = document.getElementById('risk-register-body');
        tbody.innerHTML = ''; 

        assets.forEach((asset, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${asset.name}</td>
                <td>${asset.asset_type}</td>
                <td>${asset.owner}</td>
                <td>${asset.value}</td>
                <td>${asset.priority}</td>
                <td>${asset.risk_level}</td>
                <td>${asset.control_measures_effectiveness}</td>
                <td>${asset.status}</td>
            `;
            tbody.appendChild(row);
        });
    }

    // Function to fetch data from backend
    function fetchAssets() {
        fetch('/api/assets/')  // API endpoint for fetching assets
            .then(response => response.json())
            .then(data => {
                // Update dashboard with fetched data
                updateSummaryCards(data);
                updateRiskChart(data);
                populateRiskRegister(data);
            })
            .catch(error => console.error('Error fetching assets data:', error));
    }

    fetchAssets();
});
