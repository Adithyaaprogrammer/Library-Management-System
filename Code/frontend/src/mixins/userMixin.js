export default {
  data() {
    return {
      user: null,
      islibrarian: false,
      isuser: false,
      loggedin: false,
      username: null,
      userid: null
    };
  },
  async created() {
    await this.checktoken();
  },
  methods: {
    async checktoken() {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) {
        this.loggedin = false;
        this.islibrarian = false;
        this.isuser = false;
        return;
      }
      try {
        this.user = await this.getuserinfo(access_token);
        this.loggedin = true;
        this.username = this.user.name
        this.userid = this.user.id
        if (this.user.role === 'librarian') {
          this.islibrarian = true;
        }
        else {
          this.isuser = true
          
        }

      } catch (error) {
        console.error("Error fetching user info:", error);
        this.loggedin = false;
      }
    },
    async getuserinfo(access_token) {
      const response = await fetch("http://localhost:5000/userinfo", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      if (response.status === 401) {
        this.loggedin = false;
        return null;
      }
      
      return await response.json();
    },
    logout() {
      fetch("http://localhost:5000/logout", {
        method: "POST",
        credentials: "include",
      })
        .then(() => {
          localStorage.removeItem("access_token");
          this.user = null;
          this.loggedin = false;
          this.$router.push("/login");
        })
        .catch((error) => {
          console.error("Logout error:", error);
        });
    },
  },
};
