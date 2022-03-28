<template>
    <div class="container">
        <pie-chart :data="chartData"></pie-chart>
    </div>
</template>

<script>
export default {
data() {
    return {
        chartData: {     
            labels: [
                'Red',
                'Blue',
                'Yellow'
            ],
       
            datasets: [{
                labels: ['a', 'b', 'c', 'd', 'e' ],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)'
                ],
                data: [45, 55, 48, 35, 12]
            }]
        }
    };
}
}
</script>