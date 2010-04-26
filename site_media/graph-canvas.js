var raphael_object = null;
var NODE_SIZE = 10;
var HALF_NODE = NODE_SIZE / 2;
var NODE_ANIMATION_TIME = 250;
var show_labels = true;

function RaphaelGraph(_data, _node_fields_shown, _edge_fields_shown) {
    this.paper = Raphael("canvas", 800, 600);
    this.node_fields_shown = _node_fields_shown;
    this.edge_fields_shown = _edge_fields_shown;
    this.width = this.paper.width;
    this.height = this.paper.height;
    this.data = _data;
    this.draw = draw;
    this.draw_node = draw_node;
    this.draw_edge = draw_edge;
    raphael_object = this;
}

function draw() {
    var r = this.paper.rect(0, 0, this.width, this.height, 10);
    for (var node in this.data.nodes) {
        if (this.data.nodes[node]['_visible'] == true) {
            this.draw_node(this.data.nodes[node], this.node_fields_shown);
        }
    };
    for (var e in this.data.edges) {
        edge = this.data.edges[e]
        if (this.data.nodes[edge.node1]['_visible'] && this.data.nodes[edge.node2]['_visible']) {
            this.draw_edge(edge, this.edge_fields_shown);
        }
    };
}

function draw_node(node, fields) {
    if (node["size"])
        node_size = NODE_SIZE * parseFloat(node["size"]);
    else
        node_size = NODE_SIZE;
    var c = this.paper.circle(node.xpos, node.ypos, node_size);
    c.attr("fill", node["color"]);
    c.node.onclick = function() {
        reset_data();
        selected_node = node.ID;
        document.getElementById("ID").textContent = node.ID;
        document.getElementById("id-label").textContent = "Node ID";
        document.getElementById("info-header").textContent = "Node Info";
        for (var f in fields) {
            field_key = fields[f];
            document.getElementById("info-" + f + "-label").textContent = field_key;
            document.getElementById("info-" + f).textContent = node[field_key];
        }
    show_action_box(node.xpos, node.ypos);
    };
    c.node.onmouseover = function () {
        c.animate({"scale": "2 2"}, NODE_ANIMATION_TIME);
    };
    c.node.onmouseout = function () {
        c.animate({"scale": "1 1"}, NODE_ANIMATION_TIME);
    };
    if (show_labels == true) {
        var t = this.paper.text(node.xpos-NODE_SIZE, node.ypos-NODE_SIZE, node["text"]);
    }
};

function draw_edge(edge, fields) {
    string_path = "M" + this.data.nodes[edge.node1].xpos + " " + 
                    this.data.nodes[edge.node1].ypos + 
                    "L" + this.data.nodes[edge.node2].xpos + " " + 
                    this.data.nodes[edge.node2].ypos;
    var e = this.paper.path(string_path);
    e.node.onclick = function (e) {
        console.log(e);
        reset_data();
        selected_node = null;
        document.getElementById("ID").textContent = edge.ID;
        document.getElementById("id-label").textContent = "Edge ID";
        document.getElementById("info-header").textContent = "Edge Info";
        for (var f in fields) {
            field_key = fields[f];
            document.getElementById("info-" + f + "-label").textContent = field_key;
            document.getElementById("info-" + f).textContent = edge[field_key];
        }
        document.getElementById("delete").disabled = true;
        document.getElementById("expand").disabled = true;
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

function show_action_box(xpos, ypos) {
    xmargin=200;
    ymargin=5;
    document.getElementById('floating').style.top = (ypos+ymargin)+"px";
    document.getElementById('floating').style.left = (xpos+xmargin)+"px";
    document.getElementById('floating').style.display='block';
    return;
    }
