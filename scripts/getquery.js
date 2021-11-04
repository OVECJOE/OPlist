function getSearchQuery() {
	var query = document.getElementById("input").value;

	let idx = query.search(/^([A-Z]*\/\s)?\{[a-zA-Z]+ '([a-zA-Z0-9]*.){1,}'\}/g);
	if (idx != 0)
		alert("Search Syntax Is Invalid; Try Again!");
	else
		alert("Success!");
		return query;
}