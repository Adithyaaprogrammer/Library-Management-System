<template>
  <div class="create-book">
    <NavBar />
    <div class="container mt-5">
      <h2>Create Book</h2>
      <form @submit.prevent="createBook" class="mt-4">
        <div class="form-group row">
          <label for="book_name" class="col-sm-2 col-form-label">Book Name</label>
          <div class="col-sm-10">
            <input v-model="book_name" type="text" class="form-control" id="book_name" required />
          </div>
        </div>
        <div class="form-group row">
          <label for="book_content" class="col-sm-2 col-form-label">Content</label>
          <div class="col-sm-10">
            <input v-model="book_content" type="text" class="form-control" id="book_content" required />
          </div>
        </div>
        <div class="form-group row">
          <label for="authors" class="col-sm-2 col-form-label">Authors(if multiple seperated by comma)</label>
          <div class="col-sm-10">
            <input v-model="authors" type="text" class="form-control" id="authors" required />
          </div>
        </div>
        <div class="form-group row">
          <label for="book_link" class="col-sm-2 col-form-label">Book Link</label>
          <div class="col-sm-10">
            <input v-model="book_link" type="text" class="form-control" id="book_link" required />
          </div>
        </div>
        <div class="form-group row">
          <div class="col-sm-10">
            <button type="submit" class="btn btn-primary">Create Book</button>
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
      book_name: "",
      book_content: "",
      authors: "",
      book_link: "",
    };
  },
  methods: {
    async createBook() {
      try {
        const section_id = this.$route.params.id;
        const bookData = {
          name: this.book_name,
          content: this.book_content,
          authors: this.authors,
          book_link: this.book_link,
        };

        const response = await this.submitBookData(section_id, bookData);

        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          this.$router.push({ name: "view-section-books", params: { id: section_id } });
        } else {
          const data = await response.json();
          alert('Error: ' + data.error);
        }
      } catch (error) {
        console.error('Create book error:', error);
        alert('An error occurred while creating the book.');
      }
    },
    async submitBookData(section_id, bookData) {
      return fetch(`http://127.0.0.1:5000/book/${section_id}`, {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
      });
    },
  },
};

</script>

<style scoped>
.create-book {
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
