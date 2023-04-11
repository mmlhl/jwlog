var CryptoJS = require("crypto-js");
var http = require("http");
const url = require("url")
var server = http.createServer(function(request, response) {
	// 回调函数接收request和response对象,
	// 获得HTTP请求的method和url:
	console.log(request.method + ': ' + request.url);
	// 将HTTP响应200写入response, 同时设置Content-Type: text/html:
	response.writeHead(200, {
		'Content-Type': 'text/json'
	});
	const {query,pathname} = url.parse(request.url,true)
	if(pathname==='/encode'){
		const n = CryptoJS.enc.Base64.parse(query.key);
	const r=CryptoJS.DES.encrypt(query.psw, n, {
		mode: CryptoJS.mode.ECB,
		padding: CryptoJS.pad.Pkcs7
	}).toString();
	// 将HTTP响应的HTML内容写入response:
	response.end(r);
	}else{
		response.end("null");
	}
	
});

// 让服务器监听8080端口:
server.listen(5715);

console.log('Server is running at http://127.0.0.1:5715/');
