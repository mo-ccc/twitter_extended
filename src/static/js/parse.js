// this section of code replaces all emote syntax in all tweets with an img for that emote
var tweets = document.querySelectorAll('.tweet');
for (i = 0; i < tweets.length; i++) {
	// skips to next tweet if there are no : in the tweet
	if (tweets[i].innerHTML.includes(":") === false) {
		continue;
	}
	
	// splits the text content of the tweet using :
	let splited = tweets[i].innerHTML.split(":");
	
	for (j = 0; j < splited.length; j++) {
		// if there is a space in the split skip this iteration
		if (splited[j].includes(" ") === true) {
			continue;
		}
		// convert the text to an img
		if (splited[j]) {
			splited[j] = `<a href="/emotes/search/${splited[j]}"><img src="/static/emotes/${splited[j]}.png" onerror="revert(this);" alt="${splited[j]}"><a>`;
		}
	}
	
	// rejoin tweet
	string = splited.join("");
	tweets[i].innerHTML = string;
}

// favourite emotes bar where users can click a favourited emote to add it to the tweet
var favourites = document.querySelectorAll('.favourite');
for (i = 0; i < favourites.length; i++) {
	favourites[i].innerHTML = `<img src="/static/emotes/${favourites[i].innerHTML}.png" onclick="add_to_textarea(this)" alt="${favourites[i].innerHTML}">`
}

// adds emote to the textarea
function add_to_textarea(elem) {
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