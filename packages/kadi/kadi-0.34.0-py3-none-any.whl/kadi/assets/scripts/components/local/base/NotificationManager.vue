<!-- Copyright 2022 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div v-for="notification in notifications" :key="notification.id">
      <notification-toast class="mb-4"
                          :title="notification.data.title"
                          :body="notification.data.body"
                          :timestamp="notification.created_at"
                          :dismiss-endpoint="notification._actions.dismiss">
      </notification-toast>
    </div>
  </div>
</template>

<script>
import NotificationToast from 'scripts/components/local/base/NotificationToast.vue';

export default {
  components: {
    NotificationToast,
  },
  data() {
    return {
      notifications: [],
      title: null,
      lastNotificationDate: null,
      currentTimeout: null,
      baseTimeout: 5_000,
      maxTimeout: 10_000,
      pollTimeoutHandle: null,
    };
  },
  props: {
    endpoint: String,
  },
  methods: {
    resetTimeout() {
      this.currentTimeout = this.baseTimeout;
    },
    getNotifications(scrollTo = false, resetTimeout = true) {
      this.lastNotificationDate = new Date();

      if (resetTimeout) {
        this.resetTimeout();
      }

      axios.get(this.endpoint)
        .then((response) => {
          this.notifications = response.data;

          const numNotifications = this.notifications.length;
          if (scrollTo && numNotifications > 0) {
            this.$nextTick(() => kadi.utils.scrollIntoView(this.$el, 'bottom'));
          }

          if (numNotifications > 0) {
            document.title = `(${numNotifications}) ${this.title}`;
          } else {
            document.title = this.title;
          }
        });
    },
    beforeUnload() {
      window.clearTimeout(this.pollTimeoutHandle);
    },
  },
  mounted() {
    this.title = document.title;
    this.resetTimeout();

    // Setup basic notification polling. If possible in the future, this should ideally be replaced using some kind of
    // bidirectional communication.
    const pollNotifications = () => {
      this.pollTimeoutHandle = window.setTimeout(pollNotifications, this.currentTimeout);

      // Slowly increase the polling timeout up to the maximum.
      if (this.currentTimeout < this.maxTimeout) {
        this.currentTimeout += 1_000;
      }

      // Only actually retrieve the notifications if at least the time of the base notification timeout has passed since
      // the last retrieval.
      if (this.lastNotificationDate === null || new Date() - this.lastNotificationDate >= this.baseTimeout) {
        this.getNotifications(false, false);
      }
    };

    // Do not poll the notifications at all when the window is not in focus.
    window.addEventListener('blur', () => {
      window.clearTimeout(this.pollTimeoutHandle);
    });
    // Reset the timeout and start polling for notifications again when the window is in focus.
    window.addEventListener('focus', () => {
      // Also clear any previous timeout again, just in case.
      window.clearTimeout(this.pollTimeoutHandle);
      this.resetTimeout();
      pollNotifications();
    });

    if (document.hasFocus()) {
      pollNotifications();
    }

    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
};
</script>
