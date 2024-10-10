<template>
  <div class="container">
    <h1>飲食店オーダーシステム</h1>
    <SpeechButton />
  </div>
</template>

<script setup>
import SpeechButton from '~/components/SpeechButton.vue'
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}
h1 {
  margin-bottom: 20px;
}
</style>
