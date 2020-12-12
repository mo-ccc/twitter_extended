var tweets = document.querySelectorAll('.tweet');
for (i = 0; i < tweets.length; i++) {
	console.log(tweets[i].innerHTML);
	
	let li = tweets[i].innerHTML.split(":");
	for (j = 0; j < li.length; j++) {
		if (li[j].includes(" ") === false) {
			if (li[j]) {
				li[j] = `<img src=\"http://127.0.0.1:5000/static/${li[j]}.png\">`;
			}
		}
	}
	
	string = li.join("");
	console.log(string);
	tweets[i].innerHTML = string;
}