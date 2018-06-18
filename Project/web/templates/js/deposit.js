document.addEventListener("DOMContentLoaded", init);

    function init() {

        toggleNav();
        table = document.getElementById('table');
        table.innerHTML = createTable();
    }

    function toggleNav() {
        let toggleTrigger = document.querySelectorAll(".js-toggle-nav");
        for (let i = 0; i < toggleTrigger.length; i++) {
            toggleTrigger[i].addEventListener("click", function () {
                document.querySelector("body").classList.toggle("has-mobile-nav");
            })
        }
    }

    function createTable() {
        let date;
        let idlist = {{ idlist }};
        let momentlist = {{ momentlist | safe }};
        str = "<table>";
        for(let i=0; i<idlist.length;i++){
            str+= "<tr><td>" + idlist[i] + "</td><td>" + momentlist [0] + "</td></tr>";
        }
        str += "</table>";
        return str;
    }