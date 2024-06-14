// //bar chart
// // var options = {
// //     series: [{
// //             // name: "High - 2013",
// //             data: [35, 41, 62, 42, 13, 18, 29, 37, 36, 51, 32, 35]
// //         },

// //         {
// //             // name: "Low - 2013",
// //             data: [87, 57, 74, 99, 75, 38, 62, 47, 82, 56, 45, 47]
// //         }
// //     ],

// //     chart: {
// //         toolbar: {
// //             show: false
// //         }
// //     },

// //     chart: {
// //         height: 320,
// //     },

// //     legend: {
// //         show: false,
// //     },

// //     colors: ['#e22454', '#2483e2'],

// //     markers: {
// //         size: 1,
// //     },

// //     // grid: {
// //     //     show: false,
// //     //     xaxis: {
// //     //         lines: {
// //     //             show: false
// //     //         }
// //     //     },
// //     // },

// //     xaxis: {
// //         categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
// //         labels: {
// //             show: false,
// //         }
// //     },

// //     responsive: [{
// //             breakpoint: 1400,
// //             options: {
// //                 chart: {
// //                     height: 300,
// //                 },
// //             },
// //         },

// //         {
// //             breakpoint: 992,
// //             options: {
// //                 chart: {
// //                     height: 210,
// //                     width: "100%",
// //                     offsetX: 0,
// //                 },
// //             },
// //         },

// //         {
// //             breakpoint: 578,
// //             options: {
// //                 chart: {
// //                     height: 200,
// //                     width: "105%",
// //                     offsetX: -20,
// //                     offsetY: 10,
// //                 },
// //             },
// //         },

// //         {
// //             breakpoint: 430,
// //             options: {
// //                 chart: {
// //                     width: "108%",
// //                 },
// //             },
// //         },

// //         {
// //             breakpoint: 330,
// //             options: {
// //                 chart: {
// //                     width: "112%",
// //                 },
// //             },
// //         },
// //     ],
// // };

// // var chart = new ApexCharts(document.querySelector("#bar-chart-earning"), options);
// // chart.render();

// // expenses cart
// // var options = {
// //     series: [{
// //         name: 'Actual',

// //         data: [{
// //                 x: '2011',
// //                 y: 1292,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 1400,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2012',
// //                 y: 4432,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 5400,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2013',
// //                 y: 5423,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 5200,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2014',
// //                 y: 6653,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 6500,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2015',
// //                 y: 8133,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 6600,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2016',
// //                 y: 7132,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 7500,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2017',
// //                 y: 7332,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 8700,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             },

// //             {
// //                 x: '2018',
// //                 y: 6553,
// //                 goals: [{
// //                     name: 'Expected',
// //                     value: 7300,
// //                     strokeWidth: 5,
// //                     strokeColor: '#775DD0'
// //                 }]
// //             }
// //         ]
// //     }],

// //     chart: {
// //         height: 320,
// //         type: 'bar'
// //     },

// //     plotOptions: {
// //         bar: {
// //             columnWidth: '40%'
// //         }
// //     },

// //     colors: ['#e22454'],
// //     dataLabels: {
// //         enabled: false
// //     },

// //     legend: {
// //         show: false,
// //     }
// // };

// var chart = new ApexCharts(document.querySelector("#report-chart"), options);
// chart.render();

// //pie chart for visitors
// var options = {
//     series: [44, 55, 41, 17],
//     labels: ['The Passersby', 'The Occasionals', 'The Regulars', 'The Superfans'],
//     chart: {
//         width: "100%",
//         height: 275,
//         type: 'donut',
//     },

//     legend: {
//         fontSize: '12px',
//         position: 'bottom',
//         offsetX: 1,
//         offsetY: -1,

//         markers: {
//             width: 10,
//             height: 10,
//         },

//         itemMargin: {
//             vertical: 2
//         },
//     },

//     colors: ['#4aa4d9', '#ef3f3e', '#9e65c2', '#6670bd', '#FF9800'],

//     plotOptions: {
//         pie: {
//             startAngle: -90,
//             endAngle: 270
//         }
//     },

//     dataLabels: {
//         enabled: false
//     },

//     responsive: [{
//             breakpoint: 1835,
//             options: {
//                 chart: {
//                     height: 245,
//                 },

//                 legend: {
//                     position: 'bottom',

//                     itemMargin: {
//                         horizontal: 5,
//                         vertical: 1
//                     },
//                 },
//             },
//         },

//         {
//             breakpoint: 1388,
//             options: {
//                 chart: {
//                     height: 330,
//                 },

//                 legend: {
//                     position: 'bottom',
//                 },
//             },
//         },

//         {
//             breakpoint: 1275,
//             options: {
//                 chart: {
//                     height: 300,
//                 },

//                 legend: {
//                     position: 'bottom',
//                 },
//             },
//         },

//         {
//             breakpoint: 1158,
//             options: {
//                 chart: {
//                     height: 280,
//                 },

//                 legend: {
//                     fontSize: '10px',
//                     position: 'bottom',
//                     offsetY: 10,
//                 },
//             },
//         },

//         {
//             theme: {
//                 mode: 'dark',
//                 palette: 'palette1',
//                 monochrome: {
//                     enabled: true,
//                     color: '#255aee',
//                     shadeTo: 'dark',
//                     shadeIntensity: 0.65
//                 },
//             },
//         },

//         {
//             breakpoint: 598,
//             options: {
//                 chart: {
//                     height: 280,
//                 },

//                 legend: {
//                     fontSize: '12px',
//                     position: 'bottom',
//                     offsetX: 5,
//                     offsetY: -5,

//                     markers: {
//                         width: 10,
//                         height: 10,
//                     },

//                     itemMargin: {
//                         vertical: 1
//                     },
//                 },
//             },
//         },
//     ],
// };

// var chart = new ApexCharts(document.querySelector("#pie-chart-visitors"), options);
// chart.render();