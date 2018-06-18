let days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

document.addEventListener("DOMContentLoaded", init);

function init() {

    let add_timetable = document.querySelector("#timetable");
    add_timetable.addEventListener("click", function() {
        addRow();
    })

    toggleNav();
}

function addRow() {
    for (let i = 0; i < 7; i++) {
        let section = "";
        section += '<div><input class="c-time__input" name="' + days[i] + '1" value="07:00"></div>';
        let day = document.getElementById(days[i]);
        day.innerHTML += section;
    }
}

function toggleNav() {
    let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
    for (let i = 0; i < toggleTrigger.length; i++) {
        toggleTrigger[i].addEventListener("click", function() {
            document.querySelector("body").classList.toggle("has-mobile-nav");
            })
    }
}