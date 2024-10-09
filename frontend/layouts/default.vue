<template>
  <div>
    <header>
      <h1>AI チャットアプリケーション</h1>
      <nav>
        <ul>
          <li><NuxtLink to="/">ホーム</NuxtLink></li>
          <li><NuxtLink to="/chat">チャット</NuxtLink></li>
        </ul>
      </nav>
    </header>

    <main>
      <slot />
    </main>

    <footer>
      <p>&copy; 2023 AI チャットアプリケーション</p>
    </footer>
  </div>
</template>

<script setup>
// 必要に応じてスクリプトを追加
</script>

<style scoped>
header {
  background-color: #333;
  color: white;
  padding: 1rem;
}

nav ul {
  list-style-type: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin-right: 1rem;
}

nav a {
  color: white;
  text-decoration: none;
}

main {
  padding: 2rem;
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>
