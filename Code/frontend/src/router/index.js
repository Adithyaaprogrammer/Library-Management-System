import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';
import RegisterPage from "../views/RegisterPage.vue";
import LoginPage from "../views/LoginPage.vue";
import SectionsView from "../views/SectionsView.vue";
import SectionCreate from "../views/SectionCreate.vue"
import SectionUpdate from "../views/SectionUpdate.vue";
import CreateBookpage from "../views/CreateBookpage.vue";
import UpdateBookpage from "../views/UpdateBookpage.vue";
import BookSectionpage from "../views/BookSectionpage.vue";
import Bookspage from "../views/Bookspage.vue";
import UserView from "../views/UserView.vue";
import LibrarianView from "../views/LibrarianRequestQueue.vue";
import RevokeBook from '../views/RevokeBook.vue';
import ExportExcel from '../views/ExportExcel.vue';
const routes = [
  {
    path: "/export-excel",
    name: "export-excel",
    component: ExportExcel,
  },
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/create-section",
    name: "create-section",
    component: SectionCreate,
  },
  {
    path: "/view-sections",
    name: "view-sections",
    component: SectionsView,
  },
  {
    path: "/update-section/:id",
    name: "update-section",
    component: SectionUpdate,
  },
  {
    path: "/create-book/:id",
    name: "create-book",
    component: CreateBookpage,
  },
  {
    path: "/view-section-books/:id",
    name: "view-section-books",
    component: BookSectionpage,
  },
  {
    path: "/update-book/:id",
    name: "update-book",
    component: UpdateBookpage,
  },
  {
    path: "/view-books",
    name: "view-books",
    component: Bookspage,
  },

  {
    path: "/book-request-user",
    name: "book-request-user",
    component: UserView,
  },
  {
    path: "/book-request-status",
    name: "book-request-status",
    component: LibrarianView,
  },
  {
    path: "/revoke-book",
    name: "revoke-book",
    component: RevokeBook,
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router;
