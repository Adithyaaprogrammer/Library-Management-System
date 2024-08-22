<template>
  <div class="login-page">
    <NavBar />
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow-lg">
            <div class="card-body">
              <h2 class="card-title text-center mb-4">Login</h2>
              <form @submit.prevent="login"> 
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    type="email"
                    id="email"
                    class="form-control"
                    v-model="email"
                    required
                  />
                </div>
                
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input
                    type="password"
                    id="password"
                    class="form-control"
                    v-model="password"
                    required
                  />
                </div>
                <button type="submit" class="btn btn-primary w-100">Login</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  components: {
    NavBar,
  },
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      const formData = {
        email: this.email,
        password: this.password,
      };

      try {
        const response = await this.postLoginData(formData);
        const data = await response.json();

        if (response.ok) {
          alert(data.message);
          localStorage.setItem("access_token", data.access_token);
          this.$router.push("/");
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred while attempting to login.");
      }
    },
    async postLoginData(formData) {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      return response;
    },
  },
};

</script>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f7fafc;
  font-family: 'Roboto', sans-serif;
}

.card {
  border-radius: 10px;
  background: #ffffff;
}

.card-body {
  padding: 2rem;
}

.card-title {
  font-size: 1.75rem;
  color: #2d3748;
  font-weight: 700;
}

.form-label {
  font-weight: 600;
  color: #4a5568;
}

.form-control {
  border-radius: 5px;
  font-size: 1rem;
}

.btn-primary {
  background-color: #3182ce;
  border-color: #3182ce;
  font-size: 1rem;
  padding: 0.75rem;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #2b6cb0;
  border-color: #2b6cb0;
}

@media (max-width: 768px) {
  .card-body {
    padding: 1.5rem;
  }
  
  .card-title {
    font-size: 1.5rem;
  }
}
</style>
