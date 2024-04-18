$(document).ready(function () {
	const selectedAmenities = {};
	$('input[type="checkbox"]').change(function () {
		const amenityId = $(this).data('id');
		const amenityName = $(this).data('name');

		if ($(this).is(':checked')) {
			selectedAmenities[amenityId] = amenityName;
		} else {
			delete selectedAmenities[amenityId];
		}
		const selectedAmenitiesList = Object.values(selectedAmenities).join(', ');
		$('.amenities h4').text(selectedAmenitiesList)
	})
	apiUrl = "http://localhost:5001/api/v1/status";
		$.ajax({
			url: apiUrl,
			method: "GET",
			success: (response)	=> {
				if (response && response.status == "OK")
				{
					$('div#api-status').css('background-color', '');	
					$('div#api-status').addClass('available');
				} else {
					$('div#api-status').removeClass('available');
				}
			}
		})
})