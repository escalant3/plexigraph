var GraphLayout = {

/* Random layout: Distributes node positions randomly
    into a canvas with the size specified */
'random_layout' : function(nodes, width, height) {
    for (var node in nodes) {
        nodes[node].xpos = this.rand(width);
        nodes[node].ypos = this.rand(height);
    }
},

/* Circular layout: Distributes node positions with
    a circular shape into a canvas with the size specified */
'circular_layout' : function(nodes, width, height) {
    N = this.len(nodes);
    step = 2.0*Math.PI/N;
    points = Array();
    for(i=0;i<2*Math.PI;i=i+step) {
        points.push(i);
    }
    scale_x = width/2;
    offset_x = width/2;
    scale_y = height/2;
    offset_y = height/2;
    for(var i in nodes) {
        point = points.pop()
        nodes[i].xpos = Math.cos(point) * scale_x + offset_x;
        nodes[i].ypos = Math.sin(point) * scale_y + offset_y;
    }
},

/* Spring layout: Distribute node positions using the Spring
    algorithm into a canvas with the size specified*/
'spring_layout' : function(nodes, edges, iterations, width, height) {
    for (var node in nodes) {
        nodes[node].xspeed = 0;
        nodes[node].yspeed = 0;
    }
    N = this.len(nodes);
    k = Math.sqrt(height*width/N);
    for (var iteration=0;iteration<iterations;iteration=iteration+1) {
        for (var i in nodes) {
            for (var j in nodes) {
                this.coulombRepulsion(k, nodes[i], nodes[j]);
            }
        }
        for (var i in edges) {
            this.hookeAttraction(k, nodes, edges[i]);
        }
        for (var i in nodes) {
            node = nodes[i];
            var xmove = 0.001 * node.xspeed;
            var ymove = 0.001 * node.yspeed;
            node.xpos += xmove;
            node.ypos += ymove;
            if (node.xpos > width) node.xpos=width-5;
            if (node.xpos < 0) node.xpos=5;
            if (node.ypos > height) node.ypos=height-5;
            if (node.ypos < 0) node.ypos=5;
        }
    }
},

/* ARF layout: Distribute node positions using the ARF
    algorithm into a canvas with the size specified*/
'ARF_layout' : function(nodes, edges, iterations, width, height) {
    var tension = 5;
    var radius = width/2;
    var b1 = radius * 10;
    var b2 = b1 * Math.sqrt(2) * height / width;
    var K = 0;
    for(iteration=0;iteration<iterations;iteration++) {
        for (var i in nodes) {
            var s1 = 0;
            var s2 = 0;
            for (var j in nodes) {
                if (i != j) {
                    if (this.is_edge(i, j, edges)) {
                        K = tension;
                    } else {
                        K = 0;
                    }
                    d = this.fdistance(nodes[i], nodes[j]);
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
            if (xcor>0 && xcor<width) {nodes[i].xpos = xcor;}
            if (ycor>0 && ycor<height) {nodes[i].ypos = ycor;}
        }
    }
},

/* Returns the size of an object */
'len' : function(object) {
    counter = 0;
    for (i in object) counter++;
    return counter;
},

/* Returns a number between 0 and n */
'rand' : function(n) {
    return (Math.floor(Math.random( ) * n + 1 ));
},

/* Returns the distance between two nodes */
'distance' : function(node1, node2) {
    dx = node2.xpos - node1.xpos;
    dy = node2.ypos - node1.ypos;
    return Math.sqrt(dx*dx + dy*dy);
},

/* Returns an aproximate value for the distance without
    computing sqrt to be faster */
'fdistance' : function(node1, node2) {
    dx = node2.xpos - node1.xpos;
    dy = node2.ypos - node1.ypos;
    return (dx*dx + dy*dy);
},

/* Returns if two nodes are a edge of the graph */
'is_edge' :function(node1, node2, edges) {
    for (var i in edges) {
        if (edges[i].node1 == node1 && edges[i].node2 == node2 || 
            edges[i].node1 == node2 && edges[i].node2 == node1) {
            return true;
        }
    }
    return false
},

/* Repulsion function for the spring algorithm */
'coulombRepulsion' : function(k, node1, node2) {
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
},

/* Atraction function for the spring algorithm */
'hookeAttraction' : function(k, nodes, edge) {
    var node1 = nodes[edge["node1"]];
    var node2 = nodes[edge["node2"]];
    var dx = node2.xpos - node1.xpos;
    var dy = node2.ypos - node1.ypos;
    var d2 = dx * dx + dy * dy;
    var attractiveForce = d2 / k;
    var d = Math.sqrt(d2);
    if (d>0) {
        node2.xspeed -= attractiveForce * dx / d;
        node2.yspeed -= attractiveForce * dy / d;
        node1.xspeed += attractiveForce * dx / d;
        node1.yspeed += attractiveForce * dy / d;
    }
}
}




