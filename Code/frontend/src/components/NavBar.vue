<template>
<nav class="navbar navbar-expand-sm">
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li v-if="this.loggedin" class="nav-item">
          <a class="nav-link disabled" href="#">{{this.username}} Profile</a>
        </li>
        <li v-if="this.loggedin" class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li v-if="!this.loggedin" class="nav-item-register">
          <router-link class="nav-link" to="/register">User Register</router-link>
        </li>
        <li v-if="!this.loggedin" class="nav-item-login">
          <router-link class="nav-link" to="/login">User/Librarian Login</router-link>
        </li>
        <li v-if="this.islibrarian" class="nav-item-login">
          <router-link class="nav-link" to="/create-section">Create Section
          </router-link>
        </li>
        <li 
         class="nav-item-login">
          <router-link class="nav-link" to="/view-sections">View Sections
          </router-link>
        </li>
      <li v-if="this.isuser"
        class="nav-item-login">
          <router-link class="nav-link" to="/view-books">View Books
          </router-link>
      </li>
      <li v-if="this.isuser"
        class="nav-item-login">
        <router-link class="nav-link" to="/book-request-user">My Books </router-link>
      </li>
      <li v-if="this.islibrarian"
        class="nav-item-login">
        <router-link class="nav-link" to="/book-request-status">Librarian Dashboard </router-link>
      </li>
      <li v-if="this.islibrarian"
        class="nav-item-login">
        <router-link class="nav-link" to="/export-excel">Export Data</router-link>
      </li>
      <li v-if="this.islibrarian"
        class="nav-item-login">
        <router-link class="nav-link" to="/revoke-book">Revoke Check </router-link>
      </li>
     
       <li  v-if="this.loggedin" class="nav-item-logout">
          <a @click="logout" class="nav-link" > Logout </a>
        </li>
      </ul>
    </div>
</nav>
</template>

<script>
import UserMixin from "../mixins/userMixin";

export default {
  mixins: [UserMixin],
  
};

</script>

<style>
.navitems {
  display: flex;
  align-items: center;
}

.navitems a {
  margin-left: 15px;
}
</style>
