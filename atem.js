var ATEM = require('applest-atem');

function sleep(ms) {
	return new Promise(resolve => {
		setTimeout(resolve, ms);
	});
}

var atem = new ATEM();
atem.connect(process.argv[2]);
atem.on('connect', async function() {
	atem.changePreviewInput(parseInt(process.argv[3]));
	atem.autoTransition();
	for (var i=0; i < 4; i++) {
		atem.changeUpstreamKeyState(i, (i == parseInt(process.argv[4])));
	}
	await sleep(100);
	process.exit(0);
});