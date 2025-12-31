// ===============================
// INITIALIZATION
// ===============================

document.addEventListener('DOMContentLoaded', () => {
    console.log('PriceWise initialized');
    loadLocations();
    setupNavigation();
    setupForms();
    setupCarousel();
    setupSidebarToggle();
});

// ===============================
// NAVIGATION
// ===============================

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.section');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = item.dataset.section;
            switchSection(targetSection);
        });
    });
}

function switchSection(sectionId) {
    // Update sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');

    // Update nav items
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.dataset.section === sectionId) {
            item.classList.add('active');
        }
    });

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setupCarousel() {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const nextBtn = document.querySelector('.carousel-btn.next');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const dotsNav = document.querySelector('.carousel-dots');
    const dots = Array.from(dotsNav.children);
    const featureCards = document.querySelectorAll('.feature-card');

    let currentSlideIndex = 0;

    const updateCarousel = (index) => {
        track.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach(d => d.classList.remove('active'));
        dots[index].classList.add('active');
        currentSlideIndex = index;
    };

    nextBtn.addEventListener('click', () => {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length;
        updateCarousel(currentSlideIndex);
    });

    prevBtn.addEventListener('click', () => {
        currentSlideIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
        updateCarousel(currentSlideIndex);
    });

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            updateCarousel(index);
        });
    });

    // Handle card clicks to navigate to section
    featureCards.forEach(card => {
        card.addEventListener('click', (e) => {
            // Prevent navigation if dragging/swiping (optional future enhancement)
            const targetSection = card.dataset.goto;
            switchSection(targetSection);
        });
    });

    // Auto slide every 5 seconds
    setInterval(() => {
        currentSlideIndex = (currentSlideIndex + 1) % slides.length;
        updateCarousel(currentSlideIndex);
    }, 5000);
}
// ===============================
// FORM HANDLING
// ===============================

function setupForms() {
    // Car Form
    document.getElementById('carForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleCarPrediction();
    });

    // House Form
    document.getElementById('houseForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleHousePrediction();
    });

    // Laptop Form
    document.getElementById('laptopForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleLaptopPrediction();
    });
}

// ===============================
// CAR PREDICTION
// ===============================

async function handleCarPrediction() {
    const form = document.getElementById('carForm');
    const button = form.querySelector('.btn-predict');
    const resultDiv = document.getElementById('carResult');

    // Get form data
    const data = {
        year: parseInt(document.getElementById('car-year').value),
        present_price: parseFloat(document.getElementById('car-price').value),
        kms: parseInt(document.getElementById('car-kms').value),
        fuel: parseInt(document.getElementById('car-fuel').value),
        seller: parseInt(document.getElementById('car-seller').value),
        transmission: parseInt(document.getElementById('car-transmission').value),
        owner: parseInt(document.getElementById('car-owner').value)
    };

    // Show loading state
    button.classList.add('loading');
    button.disabled = true;
    resultDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/predict/car', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showResult(resultDiv, 'Estimated Market Value', `₹ ${result.price} ${result.currency}`, false);
        } else {
            showResult(resultDiv, 'Error', result.error, true);
        }
    } catch (error) {
        showResult(resultDiv, 'Error', 'Failed to connect to server. Please try again.', true);
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
}
// ===============================
// HOUSE PREDICTION
// ===============================

async function handleHousePrediction() {
    const form = document.getElementById('houseForm');
    const button = form.querySelector('.btn-predict');
    const resultDiv = document.getElementById('houseResult');

    // Get form data
    const data = {
        total_sqft: parseFloat(document.getElementById('house-sqft').value),
        bath: parseInt(document.getElementById('house-bath').value),
        bhk: parseInt(document.getElementById('house-bhk').value),
        location: document.getElementById('house-location').value
    };

    // Show loading state
    button.classList.add('loading');
    button.disabled = true;
    resultDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/predict/house', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showResult(resultDiv, 'Estimated Property Value', `₹ ${result.price} ${result.currency}`, false);
        } else {
            showResult(resultDiv, 'Error', result.error, true);
        }
    } catch (error) {
        showResult(resultDiv, 'Error', 'Failed to connect to server. Please try again.', true);
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// ===============================
// LAPTOP PREDICTION
// ===============================

async function handleLaptopPrediction() {
    const form = document.getElementById('laptopForm');
    const button = form.querySelector('.btn-predict');
    const resultDiv = document.getElementById('laptopResult');

    // Get form data
    const data = {
        ram: parseInt(document.getElementById('laptop-ram').value),
        weight: parseFloat(document.getElementById('laptop-weight').value),
        inches: parseFloat(document.getElementById('laptop-inches').value)
    };

    // Show loading state
    button.classList.add('loading');
    button.disabled = true;
    resultDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/predict/laptop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            const subtitle = `(Approx. € ${result.price_eur.toLocaleString()})`;
            showResult(resultDiv, 'Estimated Retail Price', `${result.currency} ${result.price.toLocaleString()}`, false, subtitle);
        } else {
            showResult(resultDiv, 'Error', result.error, true);
        }
    } catch (error) {
        showResult(resultDiv, 'Error', 'Failed to connect to server. Please try again.', true);
    } finally {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// ===============================
// LOAD LOCATIONS
// ===============================

async function loadLocations() {
    try {
        const response = await fetch('/api/locations');
        const result = await response.json();

        if (result.success) {
            const select = document.getElementById('house-location');
            select.innerHTML = '<option value="">Select Location</option>';

            result.locations.forEach(location => {
                const option = document.createElement('option');
                option.value = location;
                option.textContent = location;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Failed to load locations:', error);
    }
}

// ===============================
// RESULT DISPLAY
// ===============================

function showResult(resultDiv, title, value, isError = false, subtitle = '') {
    resultDiv.classList.remove('hidden', 'error');

    if (isError) {
        resultDiv.classList.add('error');
    }

    resultDiv.innerHTML = `
        <h3>${title}</h3>
        <div class="price">${value}</div>
        ${subtitle ? `<p class="subtitle">${subtitle}</p>` : ''}
    `;

    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ===============================
// SIDEBAR / HAMBURGER TOGGLE
// ===============================
function setupSidebarToggle() {
    const btn = document.getElementById('hamburgerBtn');
    const overlay = document.getElementById('sidebarOverlay');

    if (!btn) return;

    const toggle = () => {
        const isHidden = document.body.classList.toggle('sidebar-hidden');
        btn.setAttribute('aria-expanded', String(!isHidden));
    };

    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggle();
    });

    if (overlay) {
        overlay.addEventListener('click', () => {
            document.body.classList.remove('sidebar-hidden');
            btn.setAttribute('aria-expanded', 'true');
        });
    }

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.body.classList.remove('sidebar-hidden');
            btn.setAttribute('aria-expanded', 'true');
        }
    });

    // Desktop Toggle
    const desktopBtn = document.getElementById('desktopToggle');
    if (desktopBtn) {
        desktopBtn.addEventListener('click', () => {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }
}
