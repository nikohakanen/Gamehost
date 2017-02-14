for (game in a) {
  var dates = [];
  var sales = [];
    //window.alert(typeof ([game].toString()));
    for (var i = 0; i < a[game].length; i++) {
      dates.push(a[game][i][0]);
      sales.push(a[game][i][1])
    }
    Highcharts.chart([game].toString(), {
        chart: {
            type: 'column'
        },
        title: {
            text: [game].toString() + ' sales'
        },
        xAxis: {
            categories: dates,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Sold (units)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:1.0f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Sold',
            data: sales

        }]
    });

}
