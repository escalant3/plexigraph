var MenuControl = 
{
    //Window displaying function
    toggle : function(option) {
        element = document.getElementById(option);
        display = element.style.display;
        if (display == "block") {
            element.style.display = "none";
        } else {
            element.style.display = "block";
            element.style.top = "75px";
            element.style.left = "200px";
        }
    },

    //Window movement functions
    push_move_button : function(element) {
        var moz = document.getElementById && !document.all;
        var dragging = false;
        var object_dragged; 
        function move_pointer(e){
            if (dragging) {
                newLeft = moz ? e.clientX : event.clientX;
                newTop = moz ? e.clientY : event.clientY;
                object_dragged.style.left = newLeft - 25;
                object_dragged.style.top = newTop - 25;
                return false;
            }
        }
        function release_move_button(e) {
            dragging = false;
        }
        object_dragged = document.getElementById(element);
        dragging = true;
        object_dragged.onmousemove = move_pointer;
        object_dragged.onmouseup = release_move_button;
        return false;
    },

    //Populating method
    render_controls : function(menu_class) {
        menus = $(menu_class);
        for(i=0;i<menus.length;i++) {
            firstElement = menus[i].firstElementChild;
            window_id = menus[i].id;
            $(firstElement).before('<div><span class="control" onMouseDown="MenuControl.push_move_button(\'' + window_id +'\')">&oplus;</span><span class="control" onClick="MenuControl.toggle(\''+ window_id +'\')">&otimes;</div>');
        }
    }
}
