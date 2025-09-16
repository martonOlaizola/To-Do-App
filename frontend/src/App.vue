<template>
<div>
  <Header/>
  <RouterView/>
  <Footer/>
</div>
</template>
<script setup>
  import Header from './components/Header.vue'
  import Footer from './components/Footer.vue'
import { RouterView } from 'vue-router';
</script>
