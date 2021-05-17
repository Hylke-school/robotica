let interval;
let counter = 0;
let ctx = document.getElementById('myChart').getContext('2d');

const labels = [];
const data = {
    labels: labels,
    datasets: [{
        label: 'Potentiometer',
        data: [],
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgb(255, 99, 132)"],
        borderWidth: 1
    }]
};

const config = {
    type: 'bar',
    data: data,
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 1023
            }
        }
    },
};

let myChart = new Chart(ctx,
    config
);

interval = window.setInterval(function () {
    $.get("http://141.252.29.30:5356", function (data, status) {
        // $("#pot").text(data.pot);
        myChart.data.labels[0] = counter;
        myChart.data.datasets.forEach((dataset) => {
            dataset.data[0] = data.pot
        });
        myChart.update("");
    })
    counter++;
    // if (counter === 100) {
    //     clearInterval(interval)
    // }
}, 100)