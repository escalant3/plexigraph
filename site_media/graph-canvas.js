var raphael_object = null;
var NODE_SIZE = 10;
var HALF_NODE = NODE_SIZE / 2;
var NODE_ANIMATION_TIME = 250;
var XMARGIN = 5;
var YMARGIN = 5;
var show_labels = false;
var node_label_field = "";
var multiselection = false;
var multiselection_table = []

function RaphaelGraph(_data) {
    this.paper = Raphael("canvas", 800, 800);
    this.width = this.paper.width;
    this.height = this.paper.height;
    this.data = _data;
    this.elements = {};
    this.draw = draw;
    this.render = render;
    this.draw_node = draw_node;
    this.draw_edge = draw_edge;
    this.len = len;
    this.spring_layout = spring_layout;
    this.random_layout = random_layout;
    this.circular_layout = circular_layout;
    this.ARF_layout = ARF_layout;
    this.paper.raphael_object = this;
}

function rand (n) {
    return (Math.floor(Math.random( ) * n + 1 ));
}

function len(object) {
    counter = 0;
    for (i in object) counter++;
    return counter;
}

function distance(node1, node2) {
    dx = node2.xpos - node1.xpos;
    dy = node2.ypos - node1.ypos;
    return Math.sqrt(Math.pow(node2.xpos - node1.xpos, 2) + Math.pow(node2.ypos - node1.ypos, 2));
}

function fdistance(node1, node2) {
    dx = node2.xpos - node1.xpos;
    dy = node2.ypos - node1.ypos;
    return (dx*dx + dy*dy);
}

function is_edge(node1, node2, edges) {
    for (var i in edges) {
        if (edges[i].node1 == node1 && edges[i].node2 == node2 || 
            edges[i].node1 == node2 && edges[i].node2 == node1) {
            return true;
        }
    }
    return false
}

function coulombRepulsion(k, node1, node2) {
    var dx = node2.xpos - node1.xpos;
    var dy = node2.ypos - node1.ypos;
    var d2 = dx * dx + dy * dy;
    var d = Math.sqrt(d2);
    if(d > 0) {
            var repulsiveForce = k * k / d;
            node2.xspeed += repulsiveForce * dx / d;
            node2.yspeed += repulsiveForce * dy / d;
            node1.xspeed -= repulsiveForce * dx / d;
            node1.yspeed -= repulsiveForce * dy / d;
    }
}

function hookeAttraction(k, nodes, edge) {
    var node1 = nodes[edge["node1"]];
    var node2 = nodes[edge["node2"]];
    var dx = node2.xpos - node1.xpos;
    var dy = node2.ypos - node1.ypos;
    var d2 = dx * dx + dy * dy;
    var attractiveForce = 2 * d2 / k;
    var d = Math.sqrt(d2);
    if (d>0) {
        node2.xspeed -= attractiveForce * dx / d;
        node2.yspeed -= attractiveForce * dy / d;
        node1.xspeed += attractiveForce * dx / d;
        node1.yspeed += attractiveForce * dy / d;
    }
}

function random_layout() {
    for (var node in this.data.nodes) {
        this.data.nodes[node].xpos = rand(this.width);
        this.data.nodes[node].ypos = rand(this.height);
    }
}

function spring_layout() {
    for (var node in this.data.nodes) {
        this.data.nodes[node].xspeed = 0;
        this.data.nodes[node].yspeed = 0;
    }
    N = this.len(this.data.nodes);
    k = Math.sqrt(this.height*this.width/N);
    for (var iteration=0;iteration<50;iteration=iteration+1) {
        for (var i in this.data.nodes) {
            for (var j in this.data.nodes) {
                coulombRepulsion(k, this.data.nodes[i], this.data.nodes[j]);
            }
        }
        for (var i in this.data.edges) {
            hookeAttraction(k, this.data.nodes, this.data.edges[i]);
        }
        for (var i in this.data.nodes) {
            node = this.data.nodes[i];
            var xmove = 0.001 * node.xspeed;
            var ymove = 0.001 * node.yspeed;
            node.xpos += xmove;
            node.ypos += ymove;
            if (node.xpos > this.width) node.xpos=this.width-5;
            if (node.xpos < 0) node.xpos=5;
            if (node.ypos > this.height) node.ypos=this.height-5;
            if (node.ypos < 0) node.ypos=5;
        }
    }
}

function circular_layout() {
    N = this.len(this.data.nodes);
    step = 2.0*Math.PI/N;
    points = Array();
    for(i=0;i<2*Math.PI;i=i+step) {
        points.push(i);
    }
    scale_x = this.width/2;
    offset_x = this.width/2;
    scale_y = this.height/2;
    offset_y = this.height/2;
    for(var i in this.data.nodes) {
        point = points.pop()
        this.data.nodes[i].xpos = Math.cos(point) * scale_x + offset_x;
        this.data.nodes[i].ypos = Math.sin(point) * scale_y + offset_y;
    }
}

function ARF_layout() {
    var tension = 5;
    var radius = this.width/2;
    var nodes = this.data.nodes;
    var edges = this.data.edges;
    var b1 = radius * 10;
    var b2 = b1 * Math.sqrt(2) * this.height / this.width;
    var K = 0;
    for(iteration=0;iteration<25;iteration++) {
        for (var i in nodes) {
            var s1 = 0;
            var s2 = 0;
            for (var j in nodes) {
                if (i != j) {
                    if (is_edge(i, j, edges)) {
                        K = tension;
                    } else {
                        K = 0;
                    }
                    d = fdistance(nodes[i], nodes[j]);
                    if (d > 0) {
                        v1 = (K - b1 / d) * (nodes[j].xpos - nodes[i].xpos);
                        v2 = (K - b2 / d) * (nodes[j].ypos - nodes[i].ypos);
                    }
                    s1 = s1 + v1;
                    s2 = s2 + v2;
                }
            }
            var xcor = nodes[i].xpos + s1 / 500;
            var ycor = nodes[i].ypos + s2 / 500;
            if (xcor>0 && xcor<this.width) {nodes[i].xpos = xcor;}
            if (ycor>0 && ycor<this.height) {nodes[i].ypos = ycor;}
        }
    }
}

function draw(layout) {
    switch (layout) {
        case "random": this.random_layout();break;
        case "spring": this.spring_layout();break;
        case "circular": this.circular_layout();break;
        case "ARF":this.ARF_layout();break;
    }
    this.render();
}

function render() {
    NODE_SIZE = this.width*this.height/4000;
    NODE_SIZE /= this.len(this.data.nodes);
    this.paper.clear();
    var r = this.paper.rect(0, 0, this.width, this.height, 10);
    for (var node in this.data.nodes) {
        if (this.data.nodes[node]['_visible'] == true) {
            this.draw_node(this.data.nodes[node]);
        }
    };
    for (var e in this.data.edges) {
        edge = this.data.edges[e]
        if (this.data.nodes[edge.node1]['_visible'] && this.data.nodes[edge.node2]['_visible']) {
            this.draw_edge(edge);
        }
    };
}

function draw_node(node) {
    var c = this.paper.circle(node.xpos, node.ypos, NODE_SIZE);
    this.elements[node.ID] = {};
    this.elements[node.ID]["object"] = c;
    this.elements[node.ID]["edges"] = {};
    c.attr("fill", node["color"]);
    c.node.onclick = function() {
        reset_data();
        selected_node = node.ID;
        selected_edge = null;
        info_html = info_as_table(node);
        if (!multiselection) {
            show_node_action_box(node.xpos + XMARGIN, node.ypos + YMARGIN);
        } else {
            multiselection_table.push(selected_node);
            show_node_multiselection_box();
        };
    };
    c.node.onmouseover = function () {
        c.animate({"scale": "2 2"}, NODE_ANIMATION_TIME);
    };
    c.node.onmouseout = function () {
        c.animate({"scale": "1 1"}, NODE_ANIMATION_TIME);
    };

    function move(dx, dy) {
        this.update(dx - (this.dx || 0), dy - (this.dy || 0));
        this.dx = dx;
        this.dy = dy;
    }

    function up() {
        this.dx = this.dy = 0;
    }

    c.update = function (dx, dy) {
        x = this.attr("cx") + dx;
        y = this.attr("cy") + dy;
        this.attr({cx: x, cy: y});
        node_dragged = this.paper.raphael_object.data.nodes[node.ID]
        node_dragged.xpos = x;
        node_dragged.ypos = y;
        edges = this.paper.raphael_object.elements[node.ID].edges;
        for (var node_id in edges) {
            edges[node_id].remove();
            edge.node1 = node.ID;
            edge.node2 = node_id;
            this.paper.raphael_object.draw_edge(edge, false);
        }
    }
    c.drag(move, up);
    if (show_labels == true) {
        var t = this.paper.text(node.xpos-NODE_SIZE,
                                node.ypos-NODE_SIZE,
                                node[node_label_field]);
    }
};

function draw_edge(edge) {
    node1 = this.data.nodes[edge.node1];
    node2 = this.data.nodes[edge.node2];
    string_path = "M" + node1.xpos + " " + node1.ypos + 
                    "L" + node2.xpos + " " + node2.ypos;
    var e = this.paper.path(string_path);
    this.elements[edge.node1]["edges"][edge.node2] = e;
    this.elements[edge.node2]["edges"][edge.node1] = e;
    e.node.onclick = function (event) {
        reset_data();
        selected_node = null;
        selected_edge = edge.ID;
        info_html = info_as_table(edge);
        xpos = event.clientX;
        ypos = event.clientY;
        show_edge_action_box(xpos, ypos);
    }
    e.node.onmouseover = function () {
        e.attr("stroke", "red");
    };
    e.node.onmouseout = function () {
        e.attr("stroke", "white");
    };
    e.attr("stroke", "white");
    e.toBack();
};

function reset_data() {
    table = document.getElementById("info");
    cells = table.getElementsByTagName("td");
    for (var c in cells) {
        cells[c].textContent = "";
    }
};

function key_check(e) {
    var evt = window.event ? event : e;
    var charcode = evt.charCode ? evt.charCode : evt.keyCode;
    var key_pressed = String.fromCharCode(charcode)
    switch (key_pressed) {
        case "l": show_labels = !show_labels;
    }
    raphael_object.paper.clear();
    raphael_object.draw();
};

function show_node_action_box(xpos, ypos) {
    document.getElementById('delete_node').value = "Delete node " + selected_node;
    document.getElementById('expand_node').value = "Expand node " + selected_node;
    document.getElementById('multiselect_node').value = "Start multiselection";
    document.getElementById('floating_node_menu').style.top = (ypos)+"px";
    document.getElementById('floating_node_menu').style.left = (xpos)+"px";
    document.getElementById('floating_node_menu').style.display='block';
    return;
};

function show_edge_action_box(xpos, ypos) {
    document.getElementById('delete_edge').value = "Delete edge " + selected_edge;
    document.getElementById('floating_edge_menu').style.top = ypos+"px";
    document.getElementById('floating_edge_menu').style.left = xpos+"px";
    document.getElementById('floating_edge_menu').style.display='block';
};

function show_node_multiselection_box() {
    document.getElementById('delete_node').value = "Delete selected nodes";
    document.getElementById('expand_node').value = "Expand selected nodes";
    document.getElementById('multiselect_node').value = "Cancel multiselection";
    document.getElementById('floating_node_menu').style.top = "10px";
    document.getElementById('floating_node_menu').style.left = "1000px";
    document.getElementById('floating_node_menu').style.display = "block";
}

function info_as_table(element) {
    html_table = "<table>";
    for (var field in element) {
        if (field.length && field[0]!="_") {
            html_table += "<tr><td class=\"label\">" + field +
                        ":</td><td class=\"data\">" + element[field] + 
                        "</td></tr>";
            }
    }
    html_table += "</table>";
    document.getElementById("infoTable").innerHTML = html_table;
}

function toggle_labels(label_field) {
    node_label_field = label_field;
    show_labels = !show_labels;
    raphael_object.draw()
}
