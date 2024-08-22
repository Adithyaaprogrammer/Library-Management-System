<template>
  <div class="books-in-section">
    <NavBar />
    <div class="container-fluid mt-5">
      <h2 class="text-center mb-4">
        Books in {{ sectionName }} section
        <button v-if="this.islibrarian" class="btn btn-outline-primary ml-3" @click="createBook(sectionId)">Create New Book</button>
      </h2>
      <div class="table-responsive">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Content</th>
              <th>Authors</th>
              <th>Book Link</th>
              <th>Action(s)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="book in books" :key="book.id">
              <td>{{ book.id }}</td>
              <td>{{ book.name }}</td>
              <td>{{ book.content }}</td>
              <td>{{ book.authors }}</td>
              <td><a :href="book.book_link" target="_blank">Link</a></td>
              <td>
                <div class="btn-group" role="group">
                  <button v-if="this.islibrarian" class="btn btn-outline-primary" @click="updateBook(book.id)">Update</button>
                  <button v-if="this.islibrarian" class="btn btn-outline-danger" @click="deleteBook(book.id)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
      sectionName: "",
      books: [],
    };
  },
  mounted() {
    const sectionId = this.$route.params.id;
    this.loadSectionData(sectionId);
  },
  methods: {
    async loadSectionData(sectionId) {
      try {
        await this.getSectionName(sectionId);
        await this.getBooks(sectionId);
      } catch (error) {
        console.error("Error loading section data:", error);
      }
    },
    async fetchData(url, options) {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    },
    async getSectionName(sectionId) {
      try {
        const data = await this.fetchData(`http://127.0.0.1:5000/section/${sectionId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          }
        });
        this.sectionName = data.section.name;
      } catch (error) {
        console.error("Error fetching section name:", error);
      }
    },
    async getBooks(sectionId) {
      try {
        const data = await this.fetchData(`http://127.0.0.1:5000/book/section/${sectionId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          }
        });
        this.books = data.books;
      } catch (error) {
        console.error("Error fetching books:", error);
      }
    },
    createBook(sectionId) {
      this.$router.push({ name: "create-book", params: { id: sectionId } });
    },
    updateBook(bookId) {
      this.$router.push({ name: 'update-book', params: { id: bookId } });
    },
    async deleteBook(bookId) {
      const sectionId = this.$route.params.id;
      try {
        await this.fetchData(`http://127.0.0.1:5000/book/${bookId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          }
        });
        await this.getBooks(sectionId);
      } catch (error) {
        console.error(`Error deleting book with ID ${bookId}:`, error);
      }
    },
  }
}

</script>

<style scoped>
.books-in-section {
  font-family: 'Roboto', sans-serif;
  background-color: #f7fafc;
  min-height: 100vh;
  padding: 2rem;
}

h2 {
  font-size: 1.75rem;
  color: #2d3748;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.table {
  border-radius: 8px;
  background: #ffffff;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.table-hover tbody tr:hover {
  background-color: #f1f5f9;
}

.table thead {
  background-color: #343a40;
  color: #ffffff;
}

.table th, .table td {
  padding: 1rem;
  vertical-align: middle;
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

a {
  color: #3182ce;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
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
