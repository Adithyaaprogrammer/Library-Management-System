<template>
  <div class="update-book">
    <NavBar />
    <div class="container mt-5">
      <h2>Update Book</h2>
      <form @submit.prevent="updateBook" class="mt-4">
        <div class="form-group row">
          <label for="book_name" class="col-sm-2 col-form-label">Book Name</label>
          <div class="col-sm-10">
            <input v-model="book_name" type="text" class="form-control" id="book_name" placeholder="Enter book name" required />
          </div>
        </div>
        <div class="form-group row">
          <label for="book_content" class="col-sm-2 col-form-label">Content</label>
          <div class="col-sm-10">
            <input v-model="book_content" type="text" class="form-control" id="book_content" placeholder="Enter book content" required />
          </div>
        </div>
        <div class="form-group row">
          <label for="authors" class="col-sm-2 col-form-label">Authors (comma separated)</label>
          <div class="col-sm-10">
            <input v-model="authors" type="text" class="form-control" id="authors" placeholder="Enter authors" required />
          </div>
        </div>
        <div class="form-group row">
          <label for="book_link" class="col-sm-2 col-form-label">Book Link</label>
          <div class="col-sm-10">
            <input v-model="book_link" type="text" class="form-control" id="book_link" placeholder="Enter book link" required />
          </div>
        </div>
        <div class="form-group row">
          <div class="col-sm-10">
            <button type="submit" class="btn btn-primary">Update Book</button>
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
      book_id: "",
      book_name: "",
      book_content: "",
      authors: "",
      book_link: "",
      section_id: "",
    };
  },
  mounted() {
    this.loadBookDetails();
  },
  methods: {
    async loadBookDetails() {
      const bookId = this.$route.params.id;
      const token = localStorage.getItem("access_token");

      if (!token) {
        console.error("Access token is null");
        return;
      }

      try {
        const response = await this.fetchBookDetails(bookId, token);
        const data = await response.json();
        this.setBookData(data.book);
      } catch (error) {
        console.error(`Error fetching book details for ID ${bookId}:`, error);
      }
    },
    async fetchBookDetails(bookId, token) {
      const response = await fetch(`http://127.0.0.1:5000/book/${bookId}`, {
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
    setBookData(book) {
      this.book_id = book.id;
      this.book_name = book.name;
      this.book_content = book.content;
      this.authors = book.authors;
      this.book_link = book.book_link;
      this.section_id = book.section_id;
    },
    async updateBook() {
      const bookId = this.$route.params.id;
      const token = localStorage.getItem('access_token');

      if (!token) {
        console.error("Access token is null");
        return;
      }

      try {
        await this.performUpdateBook(bookId, token);
        this.$router.push({ name: "view-section-books", params: { id: this.section_id } });
      } catch (error) {
        console.error(`Error updating book with ID ${bookId}:`, error);
      }
    },
    async performUpdateBook(bookId, token) {
      const response = await fetch(`http://127.0.0.1:5000/book/${bookId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.book_name,
          content: this.book_content,
          authors: this.authors,
          book_link: this.book_link,
          section_id: this.section_id,
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
.update-book {
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

.col-form-label {
  font-weight: 600;
}

.form-control {
  border-radius: 0.375rem;
  border-color: #d2d6dc;
}

.btn-primary {
  background-color: #3182ce;
  border-color: #3182ce;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #2b6cb0;
  border-color: #2b6cb0;
}

@media (max-width: 768px) {
  .form-control {
    font-size: 0.875rem;
  }
}
</style>
