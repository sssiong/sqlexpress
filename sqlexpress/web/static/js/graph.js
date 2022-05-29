var g = new dagreD3.graphlib.Graph({ compound: true })
    .setGraph({
        rankdir: 'LR',
        ranksep: 5,
        nodesep: 10,
    })
    .setDefaultEdgeLabel(function() { return {}; })
    .setDefaultNodeLabel(function() { return {}; });

nodes.forEach((val) => {
   g.setNode(val, {label: val, class: 'type'});
});

edges.forEach((val) => {
    g.setEdge(val[0], val[1], {
        curve: d3.curveBasis,
        arrowheadClass: 'arrowhead',
    });
})

// Create the renderer
var render = new dagreD3.render();

// Set up an SVG group so that we can translate the final graph.
var svg = d3.select("svg")
var svgGroup = svg.append("g")
var zoom = d3.zoom().on("zoom", function() {
  svgGroup.attr("transform", d3.event.transform);
});
svg.call(zoom);

// Run the renderer. This is what draws the final graph.
render(svgGroup, g);
