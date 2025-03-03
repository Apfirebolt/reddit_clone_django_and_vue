import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useSubRedditStore = defineStore("subreddit", {
  state: () => ({
    subreddit: ref({}),
    subreddits: ref([]),
    loading: ref(false),
  }),

  getters: {
    getSubreddit() {
      return this.subreddit;
    },
    getSubreddits() {
      return this.subreddits;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addSubreddit(subredditData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.post("subreddit", subredditData, {
          headers,
        });
        if (response.status === 201) {
          toast.success("Subreddit added!");
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

    async getSubredditAction(subredditId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        const response = await httpClient.get("subreddit/" + subredditId, {
          headers,
        });
        this.subreddit = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    async getSubredditsAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.get("subreddit?page=" + page, {
          headers,
        });
        this.subreddits = response.data;
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async deleteSubreddit(subredditId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.delete("subreddit/" + subredditId, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Subreddit deleted!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    async updateSubreddit(subredditData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.token}`,
        };
        this.loading = true;
        const response = await httpClient.put(
          "subreddit/" + subredditData.id,
          subredditData,
          {
            headers,
          }
        );
        if (response.status === 200) {
          toast.success("Subreddit updated!");
        }
      } catch (error) {
        console.log(error);
        return error;
      } finally {
        this.loading = false;
      }
    },

    resetSubredditData() {
      this.subreddit = {};
      this.subreddits = [];
    },
  },
});
