<template>
  <div class="sections-page">
    <NavBar />
    <div class="container-fluid mt-5">
      <h2 class="text-center mb-4">
        Sections 
        <button v-if="this.islibrarian" class="btn btn-outline-primary ms-3" @click="navigateToCreateSection()">Create New Section</button>
      </h2>
      <div class="sections mt-5">
        <div class="table-responsive">
          <table class="table table-bordered table-hover">
            <thead class="thead-light">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Content</th>
                <th>Action(s)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="section in sections" :key="section.id">
                <td>{{ section.id }}</td>
                <td>{{ section.name }}</td>
                <td>{{ section.content }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button v-if="this.islibrarian" class="btn btn-outline-primary" @click="navigateToUpdateSection(section.id)">Update</button>
                    <button v-if="this.islibrarian" class="btn btn-outline-danger" @click="deleteSection(section.id)">Delete</button>
                    <button class="btn btn-outline-secondary" @click="navigateToViewSectionBooks(section.id)">Books</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import userMixins from '../mixins/userMixin';
import NavBar from '../components/NavBar.vue';

export default {
  mixins: [userMixins],
  data() {
    return {
      sections: [],
    };
  },
  mounted() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      try {
        const response = await this.getSections();
        const data = await response.json();
        this.sections = data.sections;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async getSections() {
      const response = await fetch('http://127.0.0.1:5000/section', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      return response;
    },
    navigateToUpdateSection(sectionId) {
      this.$router.push({ name: 'update-section', params: { id: sectionId } });
    },
    navigateToCreateSection() {
      this.$router.push("/create-section");
    },
    navigateToViewSectionBooks(sectionId) {
      this.$router.push({ name: 'view-section-books', params: { id: sectionId } });
    },
    async deleteSection(sectionId) {
      try {
        await this.performDeleteSection(sectionId);
        console.log(`Section with ID ${sectionId} deleted successfully`);
        this.fetchSections();
      } catch (error) {
        console.error(`Error deleting section with ID ${sectionId}:`, error);
      }
    },
    async performDeleteSection(sectionId) {
      const response = await fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      return response;
    },
  }
}

</script>

<style scoped>
.sections-page {
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

.table {
  border-radius: 8px;
  background: #ffffff;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.table thead {
  background-color: #f8f9fa;
}

.table th {
  font-weight: 600;
}

.table td {
  font-size: 0.875rem;
}

.table-responsive {
  width: 100%;
}

.btn-group .btn {
  margin-right: 0.5rem;
}

.btn-outline-primary {
  border-color: #3182ce;
  color: #3182ce;
}

.btn-outline-primary:hover {
  background-color: #3182ce;
  color: #ffffff;
}

.btn-outline-danger {
  border-color: #e53e3e;
  color: #e53e3e;
}

.btn-outline-danger:hover {
  background-color: #e53e3e;
  color: #ffffff;
}

.btn-outline-secondary {
  border-color: #d4d4d4;
  color: #6b7280;
}

.btn-outline-secondary:hover {
  background-color: green;
  color: #000000;
}

@media (max-width: 768px) {
  .table td, .table th {
    font-size: 0.75rem;
  }
  
  .btn-group .btn {
    margin-bottom: 0.5rem;
  }
}
</style>
