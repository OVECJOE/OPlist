function getSearchQuery() {
	var query = document.getElementById("input").value;

	let idx = query.search(/^([A-Z]*\/\s)?\{[a-zA-Z]+ ["']([a-zA-Z0-9]*.){1,}["']\}/g);
	if (idx)
	{
		alert("SyntaxError: Search Query (" + query + ") is Invalid!");
		return "";
	}
	
	return query;
}
