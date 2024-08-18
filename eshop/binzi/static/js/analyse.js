
document.addEventListener('DOMContentLoaded', function () {
    // Monthly Sales Chart
    var ctxMonthly = document.getElementById('monthlySalesChart').getContext('2d');
    var monthlySalesChart = new Chart(ctxMonthly, {
        type: 'line',
        data: {
            labels: [{% for sale in monthly_sales %}'Month {{ sale.created_at__month }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Total Sales',
                data: [{% for sale in monthly_sales %}{{ sale.total_sales }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Yearly Sales Chart
    var ctxYearly = document.getElementById('yearlySalesChart').getContext('2d');
    var yearlySalesChart = new Chart(ctxYearly, {
        type: 'bar',
        data: {
            labels: [{% for sale in yearly_sales %}'Year {{ sale.created_at__year }}'{% if not forloop.last %}, {% endif %}{% endfor %}],
            datasets: [{
                label: 'Total Sales',
                data: [{% for sale in yearly_sales %}{{ sale.total_sales }}{% if not forloop.last %}, {% endif %}{% endfor %}],
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});