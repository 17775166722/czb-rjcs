/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 95.94593217471767, "KoPercent": 4.054067825282334};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.6587478064499035, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.0, 500, 1500, "登录"], "isController": false}, {"data": [0.6486666666666666, 500, 1500, "反序列化获取登录验证码"], "isController": false}, {"data": [0.23683333333333334, 500, 1500, "获取验证码"], "isController": false}, {"data": [1.0, 500, 1500, "随机获取编号"], "isController": false}, {"data": [1.0, 500, 1500, "调试取样器"], "isController": false}, {"data": [0.001026324765123562, 500, 1500, "新增会员"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 490643, 19891, 4.054067825282334, 3611.6081448222194, 0, 20906, 39.0, 15182.0, 15534.95, 15978.960000000006, 483.0499380241977, 161.8070856703478, 68.18769665872155], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["登录", 3000, 208, 6.933333333333334, 9753.881666666655, 1, 20906, 9722.5, 14868.5, 17838.95, 20712.719999999994, 7.069519296252919, 45.779606520865684, 1.878388766710576], "isController": false}, {"data": ["反序列化获取登录验证码", 3000, 0, 0.0, 1647.2646666666706, 13, 5066, 166.0, 4846.0, 4938.95, 5011.99, 7.245974257468788, 0.0, 0.0], "isController": false}, {"data": ["获取验证码", 3000, 14, 0.4666666666666667, 4915.5686666666725, 1, 15484, 3831.0, 11435.7, 11848.649999999998, 14958.839999999997, 7.247462180326522, 24.27729496174548, 0.9298833702148631], "isController": false}, {"data": ["随机获取编号", 161588, 0, 0.0, 24.864680545585053, 0, 387, 19.0, 51.0, 91.0, 262.0, 161.5445445175248, 0.0, 0.0], "isController": false}, {"data": ["调试取样器", 158800, 0, 0.0, 11.29074307304776, 0, 368, 6.0, 32.0, 45.0, 271.0, 163.64672505598304, 78.47509634243643, 0.0], "isController": false}, {"data": ["新增会员", 161255, 19669, 12.197451241821959, 10649.277889057747, 0, 17511, 14268.0, 15462.0, 15691.95, 16045.980000000003, 162.71044492989796, 59.253462653119655, 68.69196722495221], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset", 2968, 14.921321200542959, 0.6049204818982438], "isController": false}, {"data": ["Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset by peer", 1458, 7.329948217786939, 0.2971610723071561], "isController": false}, {"data": ["500/Internal Server Error", 15368, 77.26107284701624, 3.132216295758831], "isController": false}, {"data": ["Non HTTP response code: java.net.SocketException/Non HTTP response message: Broken pipe", 94, 0.47257553667487806, 0.019158532782491546], "isController": false}, {"data": ["Non HTTP response code: org.apache.http.NoHttpResponseException/Non HTTP response message: localhost:5173 failed to respond", 3, 0.015082197978985471, 6.114425356114324E-4], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 490643, 19891, "500/Internal Server Error", 15368, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset", 2968, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset by peer", 1458, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Broken pipe", 94, "Non HTTP response code: org.apache.http.NoHttpResponseException/Non HTTP response message: localhost:5173 failed to respond", 3], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": ["登录", 3000, 208, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset by peer", 140, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset", 54, "500/Internal Server Error", 14, "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["获取验证码", 3000, 14, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset", 8, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset by peer", 4, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Broken pipe", 2, "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": ["新增会员", 161255, 19669, "500/Internal Server Error", 15354, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset", 2906, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Connection reset by peer", 1314, "Non HTTP response code: java.net.SocketException/Non HTTP response message: Broken pipe", 92, "Non HTTP response code: org.apache.http.NoHttpResponseException/Non HTTP response message: localhost:5173 failed to respond", 3], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
