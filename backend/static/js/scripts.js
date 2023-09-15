// Sidebar Toggle 

var sidebarOpen = false;

var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen=false;
    }
}    


// Charts using ApexCharts

// Area Chart

var areaChartOptions = {
  series: [{
    name: 'CPU Utilization',
    data: [57, 75, 41, 67, 51, 53, 44, 61, 51, 67, 43, 56]
  }, {
    name: 'RAM Utilization',
    data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43, 46]
  }],
  chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false,
    },
  },
  colors: ["#4f35a1", "#246dec"],
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth'
  },
  labels: ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
  markers: {
    size: 0
  },
  yaxis: [
    {
      title: {
        text: '',
      },
    },
    {
      opposite: true,
      title: {
        text: '',
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
  }
};

var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
areaChart.render();