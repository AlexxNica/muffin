const ghpages = require('gh-pages');

ghpages.publish('target', {
	repo: 'https://' + process.env.GH_TOKEN + '@github.com/patissiere/muffin.git',
	message: 'Auto-generated docs',
	user: {
		name: 'Jake Shadle',
		email: 'jake.shadle@frostbite.com'
	},
	logger: function(message) {
		console.log(message);
	}
}, null);