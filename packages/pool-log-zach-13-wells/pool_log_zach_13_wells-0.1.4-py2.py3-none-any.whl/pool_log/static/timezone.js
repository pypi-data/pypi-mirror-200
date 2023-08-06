let data = new FormData();
let tzOffset = new Date().getTimezoneOffset();
console.log(tzOffset);

data.append("offset", tzOffset);
fetch('/tz', {
	"method": "POST",
	"body": data,
}).then((response) => response.text())
	.then((data) => console.log(data));

