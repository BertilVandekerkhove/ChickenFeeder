console.log("javascript geladen");

document.addEventListener("DOMContentLoaded", init);

let days = {{ days|safe }};
let time = {{ time | safe }};
let weight = {{ weight | safe }};
let daySelect = '{{ dayselect | safe }}';

function init() {
    document.querySelector("#daySelect").innerHTML = loadDays(days);

    drawChart();
    toggleNav();
}

function loadDays(days) {
    let str = "";
    for (let i in days) {
        if (days[i]==daySelect) {
            str += '<option value=' + days[i] + ' selected>' + days[i] + '</option>';
        }
        else {
            str += '<option value=' + days[i] + '>' + days[i] + '</option>';
            }
    }
    return (str);
}

function toggleNav() {
    let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
    for (let i = 0; i < toggleTrigger.length; i++) {
        toggleTrigger[i].addEventListener("click", function() {
            document.querySelector("body").classList.toggle("has-mobile-nav");
            })
    }
}
function drawChart() {
    new Chart(document.getElementById("foodChart"), {
        responsive: true,
        type: 'line',
        data: {
            labels: time,
            datasets: [{
                data: weight,
                borderColor: "#ED0F27",
                borderWith: 2,
                fill: false,
                pointRadius: 3,
                pointBackgroundColor: "#ED0F27",
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 1000,
                        stepSize: 100,
                        callback: function(value, index, values) {
                            return value + 'g';
                            },
                        fontFamily: "Open Sans",
                        fontSize: "Semibold",
                        fontSize: 8,
                        fontColor: "#ED0F27",
                    },
                    gridLines: {
                        display: false,
                        color: "#ED0F27",
                        lineWidth: 2,
                    }
                    }],
                xAxes: [{
                    ticks: {
                        fontFamily: "Open Sans",
                        fontSize: "Semibold",
                        fontSize: 8,
                        fontColor: "#ED0F27",
                    },
                    gridLines: {
                        display: false,
                        color: "#ED0F27",
                        lineWidth: 2,
                    },
                }]
            },
            legend: {
                display: false
            },
        }
    });
}