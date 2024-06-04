<template>
    <div class="flex-center-both">
      <h1>농작물 취급 안내사항</h1>
    </div>
    <div class="image-container">
        <img :src="imageUrl" alt="External Image">
    </div>
  </template>
  
  <script>
  
  export default {
    name: 'FlexCenterBoth'
  };


  </script>
  
  <style>
  .flex-center-both {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .flex-center-both h1 {
    font-size : 30px;
    font-weight: 600;
  }

  </style>
  