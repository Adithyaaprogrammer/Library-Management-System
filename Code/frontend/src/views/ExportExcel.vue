<template>
    <div class="Export Page">
      <NavBar />
    <div class="container-fluid mt-5">
      <h2 class="text-center mb-4">
        Click to Export Data to the Local Server
      </h2>
      <button @click="startExport">Start Export</button>
      <div v-if="taskStatus">
        <p>Task Status: {{ taskStatus }}</p>
      </div>
    </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        taskId: null,
        taskStatus: null,
      };
    },
    methods: {
      async startExport() {
        try {
          const response = await fetch('http://127.0.0.1:5000/start_export');
          const data = await response.json();
          this.taskId = data.task_id;
          this.checkTaskStatus();
        } catch (error) {
          console.error("Error starting export:", error);
        }
      },
      async checkTaskStatus() {
        if (!this.taskId) return;
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/start_export/${this.taskId}`);
          const data = await response.json();
          this.taskStatus = data.status;
  
          if (this.taskStatus !== "Completed") {
            setTimeout(this.checkTaskStatus, 2000); // Poll every 2 seconds
          }
        } catch (error) {
          console.error("Error checking task status:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f7fafc;
  font-family: 'Roboto', sans-serif;
  justify-content: center;
  align-items: center;
}

button {
  background-color: #3182ce;
  border-color: #3182ce;
  font-size: 1rem;
  padding: 0.75rem;
  font-weight: 600;
  color: #ffffff;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #2b6cb0;
  border-color: #2b6cb0;
}

p {
  font-size: 1.75rem;
  color: #2d3748;
  font-weight: 700;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  p {
    font-size: 1.5rem;
  }

  button {
    font-size: 0.875rem;
    padding: 0.5rem;
  }
}
</style>
