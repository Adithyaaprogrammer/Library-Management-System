<template>
  <div class="user-request-queue">
    <NavBar />
    <div class="container mt-5">
      <h2>User Request Queue</h2>
      <div class="requests mt-4">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Book ID</th>
              <th>User ID</th>
              <th>Status</th>
              <th>Issue</th>
              <th>Due</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="bookreq in bookrequest" :key="bookreq.id">
              <td>{{ bookreq.book_id }}</td>
              <td>{{ bookreq.user_id }}</td>
              <td>{{ bookreq.status }}</td>
              <td>{{ bookreq.issue }}</td>
              <td>{{ bookreq.due }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button v-if="this.islibrarian && (bookreq.status === 'renew' || bookreq.status === 'request')" class="btn btn-outline-primary" @click="approveBook(bookreq.id)">Issue</button>
                  <button v-if="this.islibrarian && (bookreq.status === 'request' || bookreq.status === 'renew')" class="btn btn-outline-danger" @click="rejectBook(bookreq.id)">Reject</button>
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
      bookrequest: [],
    };
  },
  mounted() {
    this.fetchBookRequests();
  },
  methods: {
    async fetchBookRequests() {
      try {
        const data = await this.fetchData('http://127.0.0.1:5000/bookrequest/status');
        this.bookrequest = data.bookrequest;
      } catch (error) {
        console.error('Error fetching book requests:', error);
      }
    },
    async approveBook(req_id) {
      try {
        await this.updateBookRequestStatus(req_id, 'approve');
        this.$router.push('/book-request-status');
      } catch (error) {
        console.error('Book request could not be approved:', error);
      }
    },
    async rejectBook(req_id) {
      try {
        await this.updateBookRequestStatus(req_id, 'reject');
        this.$router.push('/book-request-status');
      } catch (error) {
        console.error('Book request could not be rejected:', error);
      }
    },
    async fetchData(url) {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        }
      });
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.json();
    },
    async updateBookRequestStatus(req_id, status) {
      const response = await fetch(`http://127.0.0.1:5000/bookrequest/status/${req_id}`, {
        method: 'PUT',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
    },
  },
};

</script>

<style scoped>
.user-request-queue {
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
  background-color: #ffffff;
  border-radius: 0.375rem;
  overflow: hidden;
}

.table-dark {
  background-color: #343a40;
  color: #ffffff;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}

.btn-outline-primary {
  color: #3182ce;
  border-color: #3182ce;
}

.btn-outline-primary:hover {
  background-color: #3182ce;
  color: #ffffff;
}

.btn-outline-danger {
  color: #e53e3e;
  border-color: #e53e3e;
}

.btn-outline-danger:hover {
  background-color: #e53e3e;
  color: #ffffff;
}

.btn-group {
  display: flex;
  gap: 0.5rem;
}
</style>
