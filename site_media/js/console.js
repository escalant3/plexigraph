var KEY_UP = 38;
var KEY_DOWN = 40;
var KEY_ENTER = 13;

var historyIndex = -1;
var historyLog = []

var terminalWidget = null;

function onKeyDown(e) {
    if (sessionStorage.getItem('historyLog') == "" || sessionStorage.getItem('historyLog') == null) {
        sessionStorage.setItem('historyLog', JSON.stringify([]));
    }
    historyLog = JSON.parse(sessionStorage.getItem('historyLog'));
    e = e ? e : window.event;
    var key = e.keyCode  ? e.keyCode : e.charCode ? e.charCode : e.which ? e.which : 0;
    switch (key) {
        case KEY_UP:
            if (historyIndex == -1) {
                historyIndex = historyLog.length - 1;
            } else {
                historyIndex = historyIndex -1;
            }
            if (historyIndex >= 0) {
                terminalWidget.value = historyLog[historyIndex];
            }
            break;
        case KEY_DOWN:
            if (historyIndex == -1) {
                historyIndex = 0;
            } else {
                historyIndex = historyIndex + 1;
            }
            if (historyIndex < historyLog.length) {
                terminalWidget.value = historyLog[historyIndex];
            }
            break;
        case KEY_ENTER:
            command = terminalWidget.value;
            if (command != "") {
                historyLog.push(command);
                sessionStorage.setItem('historyLog', JSON.stringify(historyLog));
                historyIndex = -1;
                execute_query();
            }
            break;
    }
}

