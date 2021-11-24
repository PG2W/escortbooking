let request = new XMLHttpRequest();
var availableTimes = new Array();
var hoursarr = new Array();
var timeselect = document.getElementById("timeinput");

window.onload = datetimeChangeListener;
document.getElementById("escort").oninput = datetimeChangeListener;
document.getElementById("dateinput").oninput = datetimeChangeListener;
document.getElementById("timeinput").oninput = updateHours;

function rightindex(element){
    var selectedtime = timeselect.value
    return element == selectedtime
}

function updateHours(){
    $("#hoursinput").empty();
    //hoursselect = document.getElementById("hoursinput");
    /*
    if (hoursselect.options.length > 0) {
        for (a in hoursselect.options) {
            hoursselect.options.remove(0)
        }
    */  
    arrlength = availableTimes.length; 
    index = availableTimes.findIndex(rightindex)
    arrlengthfromindex = arrlength - index;
    lasthour = parseInt(availableTimes[index].substr(0, 2))
    var hours = 0
    for (i = 0; i <= arrlengthfromindex; i++) {
      if (availableTimes[index] == undefined) {
        break
      }
      suck = parseInt(availableTimes[index].substr(0, 2));
      if (lasthour == suck) {
        lasthour = parseInt(availableTimes[index].substr(0, 2)) + 1;
        hours++;
        index++;
      }
      else {
       break 
      }
    }

    for (i = 1; i <= hours; i++) {
      var hopt = document.createElement("option");
      hopt.value = i;
      hopt.innerHTML = i;
      hoursinput.appendChild(hopt);
    }
}


function datetimeChangeListener() {
  var date = document.getElementById("dateinput").value;
  var escort = document.getElementById("escort").value;
  var params = "?type=reserve" + "&escort=" + escort + "&date=" + date;

  request.open("POST", "http://134.122.62.11:80/gettimes" + params, true);
  request.send();
  request.onload = () => {
    if (request.responseText == "[]"){
      $("#hoursinput").empty();
      $("#timeinput").empty();
      $("#hoursinput").prop('disabled', true);
      $("#timeinput").prop('disabled', true);

      var opt = document.createElement("option");
      opt.value = "No available times";
      opt.innerHTML = "No available times";
      timeselect.appendChild(opt);

      var hopt = document.createElement("option");
      hopt.value = "-";
      hopt.innerHTML = "-";
      hoursinput.appendChild(hopt);
    }
    else{
      $("#hoursinput").prop('disabled', false);
      $("#timeinput").prop('disabled', false);
      availableTimes = eval(request.responseText);
      var i = timeselect.options.length - 1;
      for (i; i >= 0; i--) {
        timeselect.remove(i);
      }
      for (x in availableTimes) {
        var opt = document.createElement("option");
        opt.value = availableTimes[x];
        opt.innerHTML = availableTimes[x];
        timeselect.appendChild(opt);
      }
      updateHours();
    }
  };
}
