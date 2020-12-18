function remove(id){
	fetch(apiUrl + "/emotes/" + id, {
		method: 'DELETE'
	}).then(() => {
		console.log('removed');
	}).catch(err => {
		console.error(err)
	});
}