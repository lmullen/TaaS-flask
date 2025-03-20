document.getElementById('eventForm').addEventListener('submit', function (e) {
	e.preventDefault();

	// Get form values
	const year = document.getElementById('year').value;
	const event = document.getElementById('event').value;

	// Create JSON payload
	const data = {
		year: parseInt(year),
		event: event
	};

	const url = "/events/new";

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	});
	// 
	setTimeout(() => {
		window.location.href = '/events';
	}, 300);

})
