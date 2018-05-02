function drawChart() {
    Papa.parse("https://danwong.nz/fantasypl/data/gameweek_cumulative_points.csv", {
      download: true,
      complete: function(results) {
        var data = new google.visualization.DataTable();
        data.addRows(results.data.length)
        console.log(results.data);
        for (var i = 0; i < results.data.length; i++) {
          if (i == 0) {
            for (var j = 0; j < 4; j++) {
              data.addColumn('number', results.data[i][j]);
            }
          } else {
            for (var j = 0; j < 4; j++) {
              data.setCell(i, j, results.data[i][j]);
            }
          }
        }

        var options = {
          title: 'Points Through the Season',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('cumulative-graph-div'));

        chart.draw(data, options);
      }
    });

    Papa.parse("https://danwong.nz/fantasypl/data/gameweek_points.csv", {
      download: true,
      complete: function(results) {
        // var data = new google.visualization.DataTable();
        // data.addRows(results.data.length)
        // for (var i = 0; i < results.data.length; i++) {
        //   if (i == 0) {
        //     for (var j = 0; j < 4; j++) {
        //       data.addColumn('number', results.data[i][j]);
        //     }
        //   } else {
        //     for (var j = 0; j < 4; j++) {
        //       data.setCell(i, j, results.data[i][j]);
        //     }
        //   }
        // }
        var data = google.visualization.arrayToDataTable([
          ["Element", "Density", { role: "style" } ],
          ["Copper", 8.94, "#b87333"],
          ["Silver", 10.49, "silver"],
          ["Gold", 19.30, "gold"],
          ["Platinum", 21.45, "color: #e5e4e2"]
        ]);

        var options = {
          title: 'Points Through the Season',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('points-gameweek-div'));

        chart.draw(data, options);
      }
    });
  }