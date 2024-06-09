<template>
  <main class="p-6">
    <h1 class="text-2xl font-bold mb-4">Sales Page</h1>
    <p class="mb-6">sales: {{ sales }}</p>
    <p class="mb-6">sales.monthly_sales: {{ sales.monthly_sales }}</p>
    <p class="mb-6">sales.total_revenue: {{ sales.total_revenue }}</p>


    <div class="mb-6">
      <label for="year-select" class="mr-2">Year:</label>
      <select id="year-select" v-model="selectedYear" @change="getSales">
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>
    <table class="min-w-full border-collapse border border-slate-400">
      <thead>
        <tr class="bg-gray-100">
          <th class="px-4 py-2 border border-slate-300">월별</th>
          <th class="px-4 py-2 border border-slate-300">판매건수</th>
          <th class="px-4 py-2 border border-slate-300">판매금액</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="monthly in filteredSales" :key="monthly.month" class="bg-white even:bg-gray-50">
          <td class="px-4 py-2 border border-slate-300 text-center">{{ formatMonth(monthly.month) }}</td>
          <td class="px-4 py-2 border border-slate-300 text-right">{{ monthly.total_count }}</td>
          <td class="px-4 py-2 border border-slate-300 text-right">{{ monthly.total_sales }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'SalesView',
  data() {
    return {
      sales: { monthly_sales: []},
      selectedYear: new Date().getFullYear(), // Set the current year as the default
      years: []
    };
  },
  mounted() {
    this.getSales();
  },
    computed: {
    // 필터링된 판매 데이터를 반환하는 computed 속성
    filteredSales() {
      return this.sales.monthly_sales.filter(sale => moment(sale.month).year() === this.selectedYear);
    }
  },
  watch: {
    // Watch the sales data for changes and update the years array accordingly
    'sales.monthly_sales': function(newVal) {
      this.years = [...new Set(newVal.map(data => moment(data.month).year()))].sort();
      if (!this.years.includes(this.selectedYear)) {
        // If the current selected year is not in the new years array, update it
        this.selectedYear = this.years[0] || new Date().getFullYear();
      }
    }
  },
  methods: {
    getSales() {
      axios
        .get('api/seller/sales/')
        .then(response => {
          this.sales = response.data;
        })
        .catch(error => {
          console.error('Sales data fetch failed:', error);
        })
    },
    formatMonth(dateString) {
      return moment(dateString).format('MM');
    },
  },
}
</script>

<style scoped>
.table-container {
  overflow-x: auto;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th, .table td {
  padding: 8px;
  text-align: left;
  border: 1px solid #ddd;
}
.table th {
  background-color: #f3f3f3;
}
.table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>

