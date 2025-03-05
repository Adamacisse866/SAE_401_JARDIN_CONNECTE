// app.js
fetch('http://localhost:5000/api/events')
    .then(response => response.json())
    .then(events => {
        const carouselInner = document.querySelector('.carousel-inner');
        events.forEach((event, index) => {
            const carouselItem = document.createElement('div');
            carouselItem.classList.add('carousel-item');
            if (index === 0) {
                carouselItem.classList.add('active');
            }

            carouselItem.innerHTML = `
                <div class="row">
                    <div class="col-12 col-md-6">
                        <div class="event-text">
                            <h3>${event.title}</h3>
                            <p>${event.description}</p>
                            ${event.link ? `<a href="${event.link}">${event.date}</a>` : ''}
                        </div>
                    </div>
                    <div class="col-12 col-md-6">
                        <div class="event-image" style="background-image: url('${event.image_url}'); height: 250px; background-size: cover;"></div>
                    </div>
                </div>
            `;

            carouselInner.appendChild(carouselItem);
        });
    })
    .catch(error => console.log('Error fetching events:', error));
