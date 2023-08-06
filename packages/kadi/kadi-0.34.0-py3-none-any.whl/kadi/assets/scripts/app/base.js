/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import BroadcastMessage from 'scripts/components/local/base/BroadcastMessage.vue';
import FlashMessage from 'scripts/components/local/base/FlashMessage.vue';
import FlashMessages from 'scripts/components/local/base/FlashMessages.vue';
import LocaleChooser from 'scripts/components/local/base/LocaleChooser.vue';
import NotificationManager from 'scripts/components/local/base/NotificationManager.vue';
import QuickSearch from 'scripts/components/local/base/QuickSearch.vue';
import RecentlyVisited from 'scripts/components/local/base/RecentlyVisited.vue';

// Stop the logo animation once the site is loaded and the current animation iteration is finished.
document.querySelectorAll('.kadi-logo').forEach((el) => {
  el.addEventListener('animationiteration', () => el.style.animation = 'none');
  el.addEventListener('webkitAnimationIteration', () => el.style.animation = 'none');
});

// Scroll required inputs to a more sensible location, also taking different page layouts into account.
window.addEventListener('invalid', (e) => kadi.utils.scrollIntoView(e.target), true);

// Namespace for global base functionality and utility methods of base Vue components.
kadi.base = {
  newVue(options) {
    return new Vue({el: '#base-content', ...options});
  },
};

// Vue instance for the locale chooser in the navigation footer.
new Vue({el: '#base-locale-chooser', components: {LocaleChooser}});

// Vue instance for handling flash messages.
const flashMessages = new Vue({el: '#base-flash-messages', components: {FlashMessage, FlashMessages}});
const fmComponent = flashMessages.$refs.component;

Object.assign(kadi.base, {
  flashDanger: fmComponent.flashDanger,
  flashInfo: fmComponent.flashInfo,
  flashSuccess: fmComponent.flashSuccess,
  flashWarning: fmComponent.flashWarning,
});

// Vue instance for handling recently visited resources.
const recentlyVisited = new Vue({el: '#base-recently-visited', components: {RecentlyVisited}});
const rvComponent = recentlyVisited.$refs.component;

kadi.base.visitItem = rvComponent.addItem;

// Initializations that should only be performed for active users.
if (kadi.globals.user_active) {
  // Register global keyboard shortcuts.
  const keyMap = {
    'H': '',
    'R': 'records',
    'C': 'collections',
    'T': 'templates',
    'U': 'users',
    'G': 'groups',
  };

  window.addEventListener('keydown', (e) => {
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName) || e.target.contentEditable === 'true') {
      return;
    }

    if (e.shiftKey && !e.ctrlKey && !e.altKey && !e.metaKey) {
      for (const [key, endpoint] of Object.entries(keyMap)) {
        if (e.key === key) {
          e.preventDefault();
          window.location.href = `/${endpoint}`;
          return;
        }
      }
    }
  });

  // Vue instance for the quick search in the navigation bar.
  new Vue({el: '#base-quick-search', components: {QuickSearch}});
  // Vue instance for the global broadcast message.
  new Vue({el: '#base-broadcast-message', components: {BroadcastMessage}});

  // Vue instance for handling notifications.
  const notificationManager = new Vue({el: '#base-notification-manager', components: {NotificationManager}});
  const nmComponent = notificationManager.$refs.component;

  kadi.base.getNotifications = nmComponent.getNotifications;
}
