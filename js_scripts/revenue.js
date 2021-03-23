const ctx = document.getElementById('revenue-report').getContext('2d');
                                    const chart = new Chart(ctx, {
                                      // The type of chart we want to create
                                      type: 'bar',

                                      // The data for our dataset
                                      data: {
                                        labels: ['Cheese Pizza', 'Meat Lovers', 'Eggplant Parm', 'Chicken Parm', 'Meatball Parm', 'Eggplant Parm Calzone', 'Chicken Parm Calzone', 'Buffalo Chicken Calzone', 'BLT Chicken Salad', 'Cobb Salad'],
                                        datasets: [{
                                          label: 'Total Revenue',
                                          backgroundColor: 'rgb(255, 99, 132)',
                                          borderColor: 'rgb(255, 99, 132)',
                                          //CHANGE DATA TO REFLECT AVERAGE DAILY SALES
                                          data: [5495, 4325.67, 2997.70, 23, 9, 23, 17, 29, 16, 8]
                                        }]
                                      },
                                      });