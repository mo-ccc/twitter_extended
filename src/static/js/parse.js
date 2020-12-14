var tweets = document.querySelectorAll('.tweet');
for (i = 0; i < tweets.length; i++) {
	
	let li = tweets[i].innerHTML.split(":");
	for (j = 0; j < li.length; j++) {
		if (li[j].includes(" ") === false) {
			if (li[j]) {
				li[j] = `<img src="/static/emotes/${li[j]}.png" onerror="revert(this);" alt="${li[j]}">`;
			}
		}
	}
	
	string = li.join("");
	tweets[i].innerHTML = string;
}

var favourites = document.querySelectorAll('.favourite');
for (i = 0; i < favourites.length; i++) {
	console.log(favourites[i].innerHTML);
	favourites[i].innerHTML = `<img src="/static/emotes/${favourites[i].innerHTML}.png" onclick="redirect(this)" alt="${favourites[i].innerHTML}">`
}

function redirect(elem) {
	textbox = document.querySelector('#text');
	textbox.value = `${textbox.value}:${elem.alt}: `;
}

function revert(elem) {
	before = elem.src
	word = elem.alt
	word = `:${word}:`;
	texti = document.createTextNode(word);
	elem.parentNode.insertBefore(texti, elem);
	elem.parentNode.removeChild(elem);
}