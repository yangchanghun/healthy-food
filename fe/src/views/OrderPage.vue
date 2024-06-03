<template>
    <div class="order-page">
      <h1 class="text-2xl font-bold mb-4">주문 생성</h1>
      <div class="order-summary">
        <p>총 금액: {{ totalPrice + 3000 }}원 (배송비 포함)</p>
        <button @click="createOrder" class="mt-4 bg-indigo-600 text-white px-4 py-2 rounded">주문하기</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  
  const products = ref(JSON.parse(sessionStorage.getItem('cart')) || [])
  const totalPrice = computed(() => {
    return products.value.reduce((sum, product) => sum + product.price * product.quantity, 0)
  })
  const router = useRouter()
  
  function createOrder() {
    // 주문 생성 로직
    const order = {
      products: products.value,
      totalPrice: totalPrice.value + 3000,
      createdAt: new Date()
    }
    // 서버에 주문을 전송하는 로직을 추가하세요.
    console.log('Order created:', order)
    // 주문이 성공적으로 생성되면 장바구니를 비우고 홈으로 이동
    sessionStorage.removeItem('cart')
    router.push('/')
  }
  </script>
  
  <style scoped>
  .order-page {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  .order-summary {
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 8px;
  }
  </style>