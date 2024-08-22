<template>
  <div class="update-section">
    <NavBar />
    <div class="container mt-5">
      <h2>Update Section</h2>
      <form @submit.prevent="updateSection" class="mt-3">
        <div class="form-group row">
          <label for="section_name" class="col-sm-2 form-label">Section Name</label>
          <div class="col-sm-10">
            <input v-model="section_name" type="text" class="form-control" id="section_name" placeholder="Enter section name" required>
          </div>
        </div>
        <div class="form-group row">
          <label for="section_content" class="col-sm-2 form-label">Section Description</label>
          <div class="col-sm-10">
            <input v-model="section_content" type="text" class="form-control" id="section_content" placeholder="Enter section description" required>
          </div>
        </div>
        <div class="form-group row">
          <div class="col-sm-10">
            <button type="submit" class="btn btn-primary">Update Section</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      section_name: "",
      section_content: "",
    };
  },
  mounted() {
    this.fetchSectionDetails();
  },
  methods: {
    async fetchSectionDetails() {
      const sectionId = this.$route.params.id;
      const token = localStorage.getItem("access_token");

      if (!token) {
        console.error("Access token is null");
        return;
      }

      try {
        const response = await this.getSection(sectionId, token);
        const data = await response.json();
        this.section_name = data.section.name;
        this.section_content = data.section.content;
      } catch (error) {
        console.error(`Error fetching section details for ID ${sectionId}:`, error);
      }
    },
    async getSection(sectionId, token) {
      const response = await fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
        method: 'GET',
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response;
    },
    async updateSection() {
      const sectionId = this.$route.params.id;
      const token = localStorage.getItem('access_token');

      if (!token) {
        console.error("Access token is null");
        return;
      }

      try {
        await this.performUpdateSection(sectionId, token);
        console.log(`Section with ID ${sectionId} updated successfully`);
        this.$router.push('/view-sections');
      } catch (error) {
        console.error(`Error updating section with ID ${sectionId}:`, error);
      }
    },
    async performUpdateSection(sectionId, token) {
      const response = await fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.section_name,
          content: this.section_content,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response;
    },
  },
};

</script>

<style scoped>
.update-section {
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
