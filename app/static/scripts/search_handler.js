$(document).ready(function () {
	/**
	 * validateSearchQuery - validate the query string entered by the user.
	 * query follows a particular rule or syntax.
	 * @returns query if query is valid, else ""
	 */
	function validateSearchQuery() {
		const query = $("input").val();

		let idx = query.search(/^([A-Z]*\/\s)?\{[a-zA-Z]+ ["']([a-zA-Z0-9]*.){1,}["']\}$/g);
		if (idx) {
			const message = 'Query does not follow OPlist\'s syntax!!! Consult docs.'
			$('#errmsg').text(message).css(
				'color', 'red').css('text-align', 'center');
			return "";
		}

		return query;
	}

	/**
	 * tokenizeQuery - This function parses the query obtained from the user into
	 * a king, head and body preparing it for the backend.
	 * @returns an object containing the parsed data on success, else ""
	 */
	function tokenizeQuery() {
		const query = validateSearchQuery();
		let king, disciple;
		if (query === "")
			return query;

		if (query.search(/^([A-Z]*\/\s)/g) == 0) {
			king = query.slice(0, query.indexOf(" ") - 1);
			disciple = query.slice(king.length + 2).slice(1, -1);
		} else {
			king = 'SEARCH';
			disciple = query.slice(1, query.length - 1);
		}

		return {
			"king": king,
			"head": disciple.slice(0, disciple.indexOf(" ")),
			"body": disciple.slice(disciple.indexOf(" ") + 2, -1)
		};
	}

	$("button").click(function () {
		const data = tokenizeQuery();
		if (data !== '') {
			document.querySelector("input").value =
				`${data.king}|${data.head}|${data.body}`;
			$('#errmsg').text();
		}
		else
			return false;
	});
});