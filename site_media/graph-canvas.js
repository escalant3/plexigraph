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
    this.width = screen.width * 0.95;
    this.height = screen.height * 0.75;
    this.paper = Raphael("canvas", this.width, this.height);
    this.data = _data;
    this.elements = {};
    this.draw = draw;
    this.render = render;
    this.draw_node = draw_node;
    this.draw_edge = draw_edge;
    this.remove_node = remove_node;
    this.remove_edge = remove_edge;
    this.update = update;
    this.set_size = set_size;
    raphael_object = this;
    this.paper.raphael_object = this;
}

function draw(layout) {
    nodes = this.data.nodes;
    edges = this.data.edges;
    width = this.width;
    height = this.height;
    switch (layout) {
        case "random": random_layout(nodes, width, height);break;
        case "spring": spring_layout(nodes,edges,25,width,height);break;
        case "circular": circular_layout(nodes, width, height);break;
        case "ARF":ARF_layout(nodes,edges,25,width,height);break;
    }
    this.render();
}

function render() {
    this.paper.clear();
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
            toggle('element_info');
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
        e.attr("stroke", "black");
    };
    e.attr("stroke", "black");
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
    document.getElementById('floating_node_menu').style.display='block';
    document.getElementById('floating_edge_menu').style.display='none';
};

function show_edge_action_box(xpos, ypos) {
    document.getElementById('floating_edge_menu').style.display='block';
    document.getElementById('floating_node_menu').style.display='none';
};

function show_node_multiselection_box() {
    document.getElementById('floating_multinode_menu').style.top = "10px";
    document.getElementById('floating_multinode_menu').style.left = "10px";
    document.getElementById('floating_multinode_menu').style.display = "block";
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
    raphael_object.render()
}

function remove_node(node) {
    node_edges = this.elements[node]["edges"];
    for (var i in node_edges) {
        node_edges[i].remove();
    }
    this.elements[node]["object"].remove();
}

function remove_edge(node1, node2) {
    this.elements[node1]["edges"][node2].remove();
    delete this.elements[node1]["edges"][node2];
    delete this.elements[node2]["edges"][node1];
}

function update(_data) {
    random_layout(_data.nodes, this.width, this.height);
    for (var i in _data.nodes) {
        if (this.data.nodes[i] == undefined) {
            this.data.nodes[i]= _data.nodes[i];
        }
    }
    this.data.edges = _data.edges;
    this.render();
}

function set_size(width, height) {
    this.width = width;
    this.height = height;
    this.paper.setSize(width, height);
}
