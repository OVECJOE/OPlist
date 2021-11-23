const button = document.querySelector('button');

function validateSearchQuery() {
	var query = document.getElementById("input").value;

	let idx = query.search(/^([A-Z]*\/\s)?\{[a-zA-Z]+ ["']([a-zA-Z0-9]*.){1,}["']\}$/g);
	if (idx) {
		alert(`SyntaxError: (${query}) is an invalid search query!`);
		return "";
	}

	return query;
}

function tokenizeQuery() {
	query = validateSearchQuery();
	if (query == "")
		return;

	if (query.search(/^([A-Z]*\/\s)/g) == 0) {
		king = query.slice(0, query.indexOf(" ") - 1);
		disciple = query.slice(king.length + 2).slice(1, -1);
	}
	else {
		king = 'SEARCH';
		disciple = query.slice(1, query.length - 1);
	}

	command_set = {
		"king": king,
		"head": disciple.slice(0, disciple.indexOf(" ")),
		"body": disciple.slice(disciple.indexOf(" ") + 2, -1)
	};

	return JSON.stringify(command_set);
}

button.addEventListener('click', tokenizeQuery);
