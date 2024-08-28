<template>
  <div class="home">
    <NavBar />
    <div class="welcome-container">
      <h1 class="welcome-text">Welcome to your Library</h1>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HomePage from '@/components/HomePage.vue';
import NavBar from "@/components/NavBar.vue";

export default {
  name: 'Home',
  components: {
    HomePage,
    NavBar,
  },
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #f3f4f6, #e2e8f0), url('@/assets/background.jpg') no-repeat center center;
  background-size: cover;
  font-family: 'Roboto', sans-serif;
}

.welcome-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.welcome-text {
  font-size: 2.5rem;
  color: #2d3748;
  font-weight: 700;
  margin: 0;
}

@media (max-width: 768px) {
  .welcome-text {
    font-size: 2rem;
  }
}
</style>
