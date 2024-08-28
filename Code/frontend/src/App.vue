<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: 'Roboto', sans-serif;
  background-color: #f7fafc;
  min-height: 100vh;
  text-align: center;
  color: #2d3748;
  margin: 0;
  padding: 0;
}

nav {
  padding: 20px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
}

nav a {
  font-weight: bold;
  color: #2d3748;
  text-decoration: none;
  margin: 0 15px;
  transition: color 0.3s;
}

nav a:hover {
  color: #3182ce;
}

nav a.router-link-exact-active {
  color: #3182ce;
}
</style>
