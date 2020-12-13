var tweets = document.querySelectorAll('.tweet');
for (i = 0; i < tweets.length; i++) {
	console.log(tweets[i].innerHTML);
	
	let li = tweets[i].innerHTML.split(":");
	for (j = 0; j < li.length; j++) {
		if (li[j].includes(" ") === false) {
			if (li[j]) {
				li[j] = `<img src=\"/static/emotes/${li[j]}.png\" onerror=\"revert(this);">`;
			}
		}
	}
	
	string = li.join("");
	console.log(string);
	tweets[i].innerHTML = string;
}

function revert(elem) {
	before = elem.src
	words = elem.src.slice(before.lastIndexOf('/'), -4);
	words = `:${words}:`;
	texti = document.createTextNode(words);
	elem.parentNode.insertBefore(texti, elem);
	elem.parentNode.removeChild(elem);
}