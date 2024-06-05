<template>
    <main>
        <p>sales page</p>
    </main>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SalesView',
  data() {
    return {
      sales: [], // 판매 데이터를 저장할 배열
    };
  },
  mounted() {
    this.getSales();
  },
  methods: {
    getSales() {
      axios
        .get('api/seller/sales/');
        .then(response => {
          this.sales = response.data; // 백엔드로부터 받은 데이터를 sales 배열에 저장
        })
      .catch (error => {
        console.error('Sales data fetch failed:', error);
      });
    },
  },
}
</script>
