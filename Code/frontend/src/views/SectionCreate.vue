<template>
  <div class="create-section">
    <NavBar />
    <div class="container mt-5">
      <h2>Create Section</h2>
      <form @submit.prevent="createSection" class="mt-3">
        <div class="form-group row">
          <label for="section_name" class="col-sm-2 form-label">Section Name</label>
          <div class="col-sm-10">
            <input v-model="section_name" type="text" class="form-control" id="section_name" placeholder="Enter section name" required>
          </div>
        </div>
        <div class="form-group row">
          <label for="section_desc" class="col-sm-2 form-label">Section Description</label>
          <div class="col-sm-10">
            <input v-model="section_desc" type="text" class="form-control" id="section_desc" placeholder="Enter section description" required>
          </div>
        </div>
        <div class="form-group row">
          <div class="col-sm-10">
            <button type="submit" class="btn btn-primary">Create Section</button>
          </div>
        </div>
      </form>
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
      section_name: '',
      section_desc: '',
    };
  },
  methods: {
    async createSection() {
      try {
        const response = await this.sendSectionData({
          name: this.section_name,
          content: this.section_desc,
        });
        const data = await response.json();

        if (response.ok) {
          alert(data.message);
          this.$router.push('/view-sections');
        } else {
          alert('Error: ' + data.error);
        }
      } catch (error) {
        console.error('Create section error:', error);
        alert('An error occurred while creating the section.');
      }
    },
    async sendSectionData(sectionData) {
      const response = await fetch('http://127.0.0.1:5000/section', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sectionData),
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
.create-section {
  font-family: 'Roboto', sans-serif;
  background-color: #f7fafc;
  min-height: 100vh;
  padding: 2rem;
}

h2 {
  font-size: 1.75rem;
  color: #2d3748;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  font-weight: 500;
  color: #2d3748;
}

.form-control {
  border-radius: 0.375rem;
  border: 1px solid #ced4da;
}

.btn-primary {
  background-color: #3182ce;
  border-color: #3182ce;
}

.btn-primary:hover {
  background-color: #2b6cb0;
  border-color: #2b6cb0;
}
</style>
