<template>
  <div class="books-page">
    <NavBar />
    <div class="container-fluid mt-5">
      <h2 class="text-center mb-4">All Books</h2>
      <div class="books mt-5">
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
                    <button v-if="this.isuser" class="btn btn-outline-primary" @click="requestBook(book.id)">Request Book</button>
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
      books: [],
      user: {},
    };
  },
  mounted() {
    this.getAllBooks();
  },
  methods: {
    async fetchData(url, options) {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    },
    async getAllBooks() {
      try {
        const data = await this.fetchData("http://127.0.0.1:5000/book", {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          }
        });
        this.books = data.books;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async requestBook(book_id) {
      try {
        const data = await this.fetchData(`http://127.0.0.1:5000/bookrequest/${this.userid}/${book_id}`, {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
          },
        });
        alert(data.message);
      } catch (error) {
        console.error("Error requesting book:", error);
        alert("An error occurred while requesting the book.");
      }
    },
  },
};

</script>

<style scoped>
.books-page {
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
  background-color: #343a40;
  color: #ffffff;
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
