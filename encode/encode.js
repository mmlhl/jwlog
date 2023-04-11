const CryptoJS = require("crypto-js");
const http = require("http");
const url = require("url")
const args = process.argv.splice(2);
let port=5715
let end='/encode'

if (args.length === 2) {
	port=args[0]
	end=args[1]
}

const server = http.createServer(function (request, response) {
	// 回调函数接收request和response对象,
	// 获得HTTP请求的method和url:
	console.log(request.method + ': ' + request.url);
	// 将HTTP响应200写入response, 同时设置Content-Type: text/html:
	response.writeHead(200, {
		'Content-Type': 'text/json'
	});
	const {query, pathname} = url.parse(request.url, true)
	if (pathname === end) {
		const n = CryptoJS.enc.Base64.parse(query.key);
		const r = CryptoJS.DES.encrypt(query.psw, n, {
			mode: CryptoJS.mode.ECB,
			padding: CryptoJS.pad.Pkcs7
		}).toString();
		// 将HTTP响应的HTML内容写入response:
		response.end(r);
	} else {
		response.end("null");
	}

});

server.listen(port);

console.log('Server is running at http://127.0.0.1:'+port);
