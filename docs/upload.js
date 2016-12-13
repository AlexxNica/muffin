const ghpages = require('gh-pages');

ghpages.publish('target', {
	message: 'Auto-generated docs',
	logger: function(message) {
		console.log(message);
	}
}, null);