var ctx = document.getElementById('sales-by-product').getContext('2d');
 var sales_by_product_chart = new Chart(ctx, {
                                      // The type of chart we want to create
                                      type: 'bar',

                                      // The data for our dataset
                                      data: {
                                        labels: ['Cheese Pizza', 'Meat Lovers', 'Eggplant Parm', 'Chicken Parm', 'Meatball Parm', 'Eggplant Parm Calzone', 'Chicken Parm Calzone', 'Buffalo Chicken Calzone', 'BLT Chicken Salad', 'Cobb Salad'],
                                        datasets: [{
                                          label: 'Sales by Product',
                                          backgroundColor: 'rgb(255, 99, 132)',
                                          borderColor: 'rgb(255, 99, 132)',
                                          data: [500, 333, 250, 325, 120, 330, 245, 415, 235, 120]
                                        }]
                                      },
                                      });
 };