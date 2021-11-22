const button = document.querySelector('button');

function validateSearchQuery() {
	var query = document.getElementById("input").value;

	let idx = query.search(/^([A-Z]*\/\s)?\{[a-zA-Z]+ ["']([a-zA-Z0-9]*.){1,}["']\}$/g);
	if (idx)
	{--
		alert(`SyntaxError: (${query}) is an invalid search query!`);
		return "";
	}
	
	return query;
}

function tokenizeQuery() {
	query = validateSearchQuery();

	if (query == "")
		return;
	
	king = query.slice(0, query.indexOf(" ")-1);
	disciple = query.slice(king.length+2).slice(1, -1);

	command_set = [
		king,
		disciple.slice(0, disciple.indexOf(" ")),
		disciple.slice(disciple.indexOf(" ")+2, -1)
	];

	alert(command_set);
}

button.addEventListener('click', tokenizeQuery);
