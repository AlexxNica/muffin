const bp = require('bootprint');
const fs = require('fs-extra');
const swagger = require('bootprint-swagger');

// Create our target directory where all generated content is stored
// and uploaded
if (!fs.existsSync('target')) {
	fs.mkdirSync('target');
}

// Move our root index
fs.copySync('./docs/index.html', 'target/index.html');
fs.copySync('./docs/css', 'target/css');

// Generate the API documentation from the swagger file
var bootprint = bp
	.load(swagger)
	.merge({ /* Any other configuration */ })
	.build('./docs/api/swagger.yml', 'target/api')
	.generate()
	.done(console.log);