import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const usePostStore = defineStore("post", {
  state: () => ({
    post: ref({}),
    posts: ref([]),
    loading: ref(false),
  }),

  getters: {
    getPost() {
      return this.post;
    },
    getPosts() {
      return this.posts;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addPost(postData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.post("post", postData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Post added!");
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 400) {
          let message = "Bad request";
          if (error.response.data.message) {
            message = error.response.data.message;
          }
          toast.error(message);
        }
      } finally {
        this.loading = false;
      }
    },

    async getPostAction(postId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        const response = await httpClient.get("post/" + postId, {
          headers,
        });
        this.post = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    async getPostsAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.get("post?page=" + page, {
          headers,
        });
        this.posts = response.data;
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async deletePost(postId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.delete("post/" + postId, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Post deleted!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async updatePost(postData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.put("post/" + postData.id, postData, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Post updated!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetPostData() {
      this.post = {};
      this.posts = [];
    },
  },
});
