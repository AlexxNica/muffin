const ghpages = require('gh-pages');

ghpages.publish('target', {
  logger: function(message) {
    console.log(message);
  }
}, null);