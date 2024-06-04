<template>
  <div>
    <h1>Order History</h1>
    <div v-if="orders.length">
      <div v-for="order in orders" :key="order.id" class="order-item">
        <h2>Order #{{ order.id }}</h2>
        <p>Date: {{ new Date(order.created_at).toLocaleString() }}</p>
        <p>Total: {{ order.get_total_price + 3000}}원</p>
        <div v-for="item in order.order_items" :key="item.product.id" class="order-product">
          <p>Product: {{ item.product.name }}</p>
          <p>Quantity: {{ item.quantity }}</p>
          <p>Price: {{ item.get_total_item_price }}원</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No orders found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: []
    };
  },
  created() {
    this.fetchOrderHistory();
  },
  methods: {
    fetchOrderHistory() {
      axios
        .get('/api/orders/history/')
        .then(response => {
          this.orders = response.data.orders;
        })
        .catch(error => {
          console.error('Error fetching order history', error);
        });
    }
  }
};
</script>

<style scoped>
.order-item {
  border: 1px solid #ccc;
  padding: 16px;
  margin-bottom: 16px;
}
.order-product {
  margin-left: 16px;
}
</style>
