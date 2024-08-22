<template>
  <div class="user-dashboard">
    <NavBar />
    <div class="container mt-5">
      <h2>User Dashboard</h2>
      <div class="books mt-5">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Book ID</th>
              <th>Status</th>
              <th>Request</th>
              <th>Issue</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="bookreq in bookrequest" :key="bookreq.book_id">
              <td>{{ bookreq.book_id }}</td>
              <td>{{ bookreq.status }}</td>
              <td>{{ bookreq.request }}</td>
              <td>{{ bookreq.issue }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button v-if="isuser && bookreq.status !== 'request' && bookreq.status!='revoke'" class="btn btn-outline-primary" @click="returnBook(bookreq.id)">Return</button>
                  <button v-if="isuser && bookreq.status !== 'request'&& bookreq.status!='revoke'" class="btn btn-outline-primary" @click="renewBook(bookreq.id)">Renew</button>
                  <button v-if="isuser && bookreq.status !== 'request'&& bookreq.status!='revoke'" class="btn btn-outline-primary" @click="">Review</button>
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
    this.loadUserBookRequests();
  },
  methods: {
    async loadUserBookRequests() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.error("Access token is null");
          return;
        }

        const response = await this.fetchUserBookRequests(token);
        const data = await response.json();
        this.bookrequest = data.bookrequest;
      } catch (error) {
        console.error('Error loading book requests:', error);
      }
    },

    async fetchUserBookRequests(token) {
      const response = await fetch('http://127.0.0.1:5000/bookrequest/user', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      return response;
    },

    async updateBookRequest(req_id, status) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.error("Access token is null");
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/bookrequest/status/${req_id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ status }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        console.log(`Book request ${status}d`);
        this.$router.push('/book-request-user');
      } catch (error) {
        console.log(`Book request could not be ${status}d`);
        console.error(error);
      }
    },

    returnBook(req_id) {
      this.updateBookRequest(req_id, 'return');
    },

    renewBook(req_id) {
      this.updateBookRequest(req_id, 'renew');
    },
  },
};

</script>

<style scoped>
.user-dashboard {
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

.books {
  margin-top: 2rem;
}

.table {
  margin-top: 1rem;
}

.table-dark {
  background-color: #343a40;
  color: #fff;
}

.table th,
.table td {
  text-align: center;
}

.btn-group .btn {
  margin: 0.25rem;
}

.btn-outline-primary {
  border-color: #3182ce;
  color: #3182ce;
}

.btn-outline-primary:hover {
  background-color: #3182ce;
  color: #fff;
}
</style>
