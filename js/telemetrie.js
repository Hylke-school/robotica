let interval;
counter = 0;

let chartList = new Array();

chartList.push(makeChart("joy1x"));
chartList.push(makeChart("joy1y"));
chartList.push(makeChart("joy2x"));
chartList.push(makeChart("joy2y"));



interval = window.setInterval(function () {
    $.get("http://dns.hylke.xyz:5356", function (data, status) {
        data.manual = false;
        if (!data.manual){
            $("body").css("background-color", "#ff0000");
            $("#automatic_message").show();
            $("#mode_message").show();
        } else {
            $("body").css("background-color", "#000000");
            $("#automatic_message").hide();
            $("#mode_message").hide();
        }
        switch (data.mode){
            case "sd":
                $("#mode_message").text("De Single dance wordt uitgevoerd");
                break;
            case "ld":
                $("#mode_message").text("De line dance wordt uitgevoerd");
                break;
            case "trash":
                $("#mode_message").text("De robot pakt nu afval op");
                break;
            case "vision":
                $("#mode_message").text("De robot voert nu het vision onderdeel uit");
                break;
        }
        chartList.forEach((chart) => {
            chart.data.labels[0] = counter;
            chart.data.datasets.forEach((dataset) => {
                dataset.data[0] = data[chart.data.datasets.label];
            })
            chart.update();
        });
        counter++;
    })
}, 100)

function makeChart(element){
    let ctx = document.getElementById(element).getContext('2d');

    const labels = [];
    const data = {
        labels: labels,
        datasets: [{
            label: element,
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
            },
            responsive: true,
            aspectRatio: 0.5
        },
    };

    let returnChart = new Chart(ctx, config);
    return returnChart;
}