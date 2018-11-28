/**
 * Created by harchn 2018.11
 */
$(document).ready(function () {
    var width_static = document.getElementById('static_graph').clientWidth, height_static = 400;
    var dataset = {};
    var padding = {top: 20, right: 20, bottom: 20, left: 20};
    var xAxisWidth = width_static - 2 * padding.left;
    var yAxiWidth = height_static - 2 * padding.bottom;

    var svg_static = d3.select("#static_graph").append("svg")
        .attr("width", width_static)
        .attr("height", height_static);

    d3.json("/graph", function (error, login_graph) {
        console.log(login_graph.nodes);
        update_static(login_graph.nodes)
    });


    function update_static(nodes) {
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            dataset[node['label']] = 0;
            for (var j = 0; j < nodes.length; j++) {
                if (nodes[j]['label'] == node['label'])
                    dataset[node['label']] += 1;
            }
        }
        var data = [];
        var labels = [];
        for (var key in dataset) {
            data.push(dataset[key]);
            labels.push(key);
        }
        var xAxisScale = d3.scale.ordinal()
            .domain(d3.range(labels.length))
            .rangeRoundBands([0, xAxisWidth]);

        var yAxisScale = d3.scale.linear()
            .domain([0, d3.max(data)])
            .range([yAxiWidth, 0]);

        var xAxis = d3.svg.axis()
            .scale(xAxisScale)
            .orient("bottom")
            .tickFormat(function (d) {
                return labels[d];
            });

        var yAxis = d3.svg.axis()
            .scale(yAxisScale)
            .orient("left");

        var xScale = d3.scale.ordinal()
            .domain([0, 1, 2])
            .rangeRoundBands([0, 50], 0.05);

        var yScale = d3.scale.linear()
            .domain([0, d3.max(data)])
            .range([0, yAxiWidth]);

        var rect = svg_static.selectAll("rect")
            .data(data);

        rect.append("rect")
            .attr("y", function (d, i) {
                return height_static - padding.bottom;
            })
            .attr("height", 0)
            .attr("fill", "red")
            .transition()
            .duration(3000)
            .ease("bounce")
            .delay(function (d, i) {
                return 200 * i;
            })
            .attr("x", function (d, i) {
                x = xAxisWidth / 6 * (2 * i + 1)
                    - xScale.rangeBand() / 2 + padding.left;
                return x;
            })
            .attr("y", function (d, i) {
                return height_static - padding.bottom - yScale(d);
            })
            .attr("width", function (d, i) {
                return xScale.rangeBand();
            })
            .attr("height", yScale)
            .attr("fill", "steelblue");

        rect.enter()
            .append("rect")
            .attr("y", function (d, i) {
                return height_static - padding.bottom;
            })
            .attr("height", 0)
            .attr("fill", "red")
            .transition()
            .duration(3000)
            .ease("bounce")
            .delay(function (d, i) {
                return 200 * i;
            })
            .attr("x", function (d, i) {
                x = xAxisWidth / 6 * (2 * i + 1)
                    - xScale.rangeBand() / 2 + padding.left;
                return x;
            })
            .attr("y", function (d, i) {
                return height_static - padding.bottom - yScale(d);
            })
            .attr("width", function (d, i) {
                return xScale.rangeBand();
            })
            .attr("height", yScale)
            .attr("fill", "steelblue");
        rect.exit().remove();

        text = svg_static.selectAll("text")
            .data(data);
        text.append("text")
            .attr("x", function (d, i) {
                x = xAxisWidth / 6 * (2 * i + 1)
                    - xScale.rangeBand() / 2 + padding.left;
                return x;
            })
            .attr("y", function (d, i) {
                return height_static - padding.bottom - yScale(d);
            })
            .attr("dx", function (d, i) {
                return xScale.rangeBand() / 4;
            })
            .attr("dy", -2)
            .attr("text-anchor", "begin")
            .attr("font-size", 14)
            .attr("fill", "black")
            .text(function (d, i) {
                return d;
            });
        text.enter().append("text")
            .attr("x", function (d, i) {
                x = xAxisWidth / 6 * (2 * i + 1)
                    - xScale.rangeBand() / 2 + padding.left;
                return x;
            })
            .attr("y", function (d, i) {
                return height_static - padding.bottom - yScale(d);
            })
            .attr("dx", function (d, i) {
                return xScale.rangeBand() / 4;
            })
            .attr("dy", -2)
            .attr("text-anchor", "begin")
            .attr("font-size", 14)
            .attr("fill", "black")
            .text(function (d, i) {
                return d;
            });
        text.remove();

        svg_static.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + padding.left + "," +
                (height_static - padding.bottom) + ")")
            .call(xAxis);

        svg_static.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + padding.left + "," +
                (height_static - yAxiWidth - padding.bottom) + ")")
            .call(yAxis);
    }
});



