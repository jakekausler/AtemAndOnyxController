// var ATEM = require('applest-atem');

// function sleep(ms) {
// 	return new Promise(resolve => {
// 		setTimeout(resolve, ms);
// 	});
// }

// var atem = new ATEM();
// atem.connect(process.argv[2]);
// // atem.connect("172.18.5.180");
// console.log("Attempting to connect...")
// atem.on('connect', function() {
// 	console.log("Connected")
// 	atem.changePreviewInput(parseInt(process.argv[3]));
// 	atem.autoTransition();
// 	for (var i=0; i < 4; i++) {
// 		atem.changeUpstreamKeyState(i, (i == parseInt(process.argv[4])));
// 	}
// 	// await sleep(100);
// 	console.log("Done with JS")
// 	process.exit(0);
// });

// atem.on("ping", function() {
// 	console.log("Pinged");
// })

const { Atem } = require('atem-connection')
const myAtem = new Atem({})

function sleep(ms) {
	return new Promise(resolve => {
		setTimeout(resolve, ms);
	});
}

myAtem.connect(process.argv[2])

myAtem.on('connected', async function () {
	myAtem.changePreviewInput(parseInt(process.argv[3]))
	myAtem.autoTransition()
	for (var i=0; i < 4; i++) {
		myAtem.setUpstreamKeyerOnAir((i == parseInt(process.argv[4])), 0, i);
	}
	sleep(1000);
	myAtem.disconnect();
});

myAtem.on('disconnected', function () {
	process.exit(0);
});