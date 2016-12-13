const ghpages = require('gh-pages');

ghpages.publish('target', {
	message: 'Auto-generated docs',
	user: {
		name: 'Jake Shadle',
		email: 'jake.shadle@frostbite.com'
	},
	logger: function(message) {
		console.log(message);
	}
}, null);