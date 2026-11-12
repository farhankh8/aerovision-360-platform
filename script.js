/*
 * AEROVISION 360 — Enterprise Portfolio JavaScript
 * Navigation, scroll animations, accordions, dashboard zoom, and Power BI live embedding
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initScrollAnimations();
    initSmoothScroll();
    initTypeWriter();
    initAccordions();
    initDashboardZoom();
    initNavbarScroll();
    initPowerBI();
    initDashboard();
});

/* ============================================================================
   Power BI Configuration
   ============================================================================ */

// Power BI embedding configuration.
// To enable live embedding, publish your report to the Power BI Service and
// fill in the values below. Never commit access tokens or client secrets.
//
// Embed URL example (Publish to web):
//   https://app.powerbi.com/reportEmbed?reportId=...&...
//
// Secure embed (organisation):
//   Requires an access token acquired server-side (never in frontend JS).
//   See: https://learn.microsoft.com/en-us/power-bi/developer/embedded/
const POWERBI_CONFIG = {
    // Set to true when you have a valid embed URL configured below
    enabled: false,
    // Full embed URL from Power BI Service (Publish to web or Secure embed)
    embedUrl: '',
    // Report GUID (from the embed URL)
    reportId: '',
    // Workspace GUID (required for secure organisation embedding)
    workspaceId: '',
    // Embed type: 'publish-to-web' or 'secure-embed'
    embedType: 'publish-to-web',
    // Default page to load on first render
    defaultPage: 'Executive Overview',
    // Whether to show the Power BI nav pane / filter pane
    navContentPaneEnabled: false,
    // Whether to allow editing
    editMode: false
};

// Mapping from portfolio page labels to Power BI report page names.
// Update these values to match the exact page names in your .pbix / published report.
const POWERBI_PAGE_MAP = {
    'Executive Overview': 'Executive Overview',
    'Operations & Disruption': 'Operations & Disruption',
    'Revenue & Finance': 'Revenue & Finance',
    'Cost & Financial Intelligence': 'Cost & Financial Intelligence',
    'Customer & Service Intelligence': 'Customer & Service Intelligence'
};

/* ============================================================================
   Power BI Live Embedding
   ============================================================================ */

let powerbiEmbedInstance = null;
let powerbiIsEmbedded = false;
let resizeTimeout = null;

function initPowerBI() {
    const configNotice = document.getElementById('pb-embed-config');
    const statusDot = document.querySelector('.pbix-status-dot');
    const statusText = document.getElementById('pbix-status-text');

    if (!POWERBI_CONFIG.enabled || !POWERBI_CONFIG.embedUrl) {
        // Not configured — show configuration notice, keep fallback visible
        if (configNotice) configNotice.style.display = 'flex';
        if (statusDot) statusDot.className = 'pbix-status-dot config';
        if (statusText) statusText.textContent = 'Live embedding not configured';
        return;
    }

    // Configuration is present — attempt to load the Power BI SDK and embed
    if (configNotice) configNotice.style.display = 'none';
    if (statusDot) statusDot.className = 'pbix-status-dot live';
    if (statusText) statusText.textContent = 'Live report embedded';

    loadPowerBISDK().then(() => {
        embedReport();
    }).catch((err) => {
        console.error('Power BI SDK load failed:', err);
        showEmbedError('Power BI SDK could not be loaded. Falling back to specification view.');
    });
}

/**
 * Load the Power BI JavaScript SDK from Microsoft's CDN.
 * Returns a promise that resolves when window.powerbi is available.
 */
function loadPowerBISDK() {
    return new Promise((resolve, reject) => {
        if (window.powerbi) {
            resolve(window.powerbi);
            return;
        }

        const scriptId = 'powerbi-sdk';
        if (document.getElementById(scriptId)) {
            const check = setInterval(() => {
                if (window.powerbi) {
                    clearInterval(check);
                    resolve(window.powerbi);
                }
            }, 50);
            setTimeout(() => { clearInterval(check); reject(new Error('SDK timeout')); }, 10000);
            return;
        }

        const script = document.createElement('script');
        script.id = scriptId;
        script.src = 'https://microsoft.github.io/PowerBI-JavaScript/powerbi.min.js';
        script.async = true;
        script.onload = () => resolve(window.powerbi);
        script.onerror = () => reject(new Error('Failed to load Power BI SDK'));
        document.head.appendChild(script);
    });
}

/**
 * Embed the Power BI report into the iframe container.
 */
function embedReport() {
    const embedWrap = document.getElementById('pbix-embed-wrap');
    const fallback = document.getElementById('pbix-fallback');
    const iframe = document.getElementById('pbix-embed-iframe');

    if (!embedWrap || !iframe) return;

    try {
        // For Publish to web, use the embed URL directly in an iframe.
        // For secure embed, use the powerbi.embed() API with an access token.
        if (POWERBI_CONFIG.embedType === 'publish-to-web' && POWERBI_CONFIG.embedUrl) {
            iframe.src = POWERBI_CONFIG.embedUrl;
            iframe.style.display = 'block';
            if (fallback) fallback.style.display = 'none';
            powerbiIsEmbedded = true;

            // Setup responsive resize listener (debounced)
            window.addEventListener('resize', onEmbedResize);

            // Setup page navigation buttons
            setupPageNavigation(null);

            return;
        }

        // Secure embed path — requires powerbi.embed() with access token.
        // This is a placeholder architecture; the owner must supply the token
        // from their own backend (never hardcoded in frontend JS).
        if (POWERBI_CONFIG.embedType === 'secure-embed') {
            if (!window.powerbi) {
                showEmbedError('Secure embed requires the Power BI JavaScript SDK and a server-issued access token.');
                return;
            }

            const embedConfig = {
                type: 'report',
                tokenType: models.TokenType.Embed,
                accessToken: '', // Owner must supply via their backend
                embedUrl: POWERBI_CONFIG.embedUrl,
                id: POWERBI_CONFIG.reportId,
                settings: {
                    navContentPaneEnabled: POWERBI_CONFIG.navContentPaneEnabled,
                    editMode: POWERBI_CONFIG.editMode
                }
            };

            if (POWERBI_CONFIG.workspaceId) {
                embedConfig.workspaceId = POWERBI_CONFIG.workspaceId;
            }

            powerbiEmbedInstance = window.powerbi.embed(embedWrap, embedConfig);

            powerbiEmbedInstance.on('loaded', () => {
                iframe.style.display = 'none';
                if (fallback) fallback.style.display = 'none';
                powerbiIsEmbedded = true;
                setupPageNavigation(powerbiEmbedInstance);
                window.addEventListener('resize', onEmbedResize);
            });

            powerbiEmbedInstance.on('error', (event) => {
                console.error('Power BI embed error:', event);
                showEmbedError('Power BI report failed to load: ' + (event.detail || 'unknown error'));
            });

            powerbiEmbedInstance.on('pageChanged', (event) => {
                updateActiveNavButton(event.detail.newPage.name);
            });

            return;
        }

        showEmbedError('No valid embed type configured.');
    } catch (err) {
        console.error('Embed failed:', err);
        showEmbedError('Embedding failed: ' + err.message);
    }
}

/**
 * Setup click handlers for the five page navigation buttons.
 * When live embedding is active (secure), uses powerbi.report.navigateToPage.
 * When in publish-to-web iframe mode, navigation is handled by the iframe itself
 * (the buttons remain as visual reference / fallback anchors).
 */
function setupPageNavigation(reportInstance) {
    const btns = document.querySelectorAll('.pb-nav-btn');
    btns.forEach(btn => {
        btn.addEventListener('click', function() {
            const pageLabel = this.getAttribute('data-page');
            const pageName = POWERBI_PAGE_MAP[pageLabel] || pageLabel;

            // Update active button state
            btns.forEach(b => {
                b.classList.remove('pb-nav-active');
                b.setAttribute('aria-pressed', 'false');
            });
            this.classList.add('pb-nav-active');
            this.setAttribute('aria-pressed', 'true');

            // Navigate in the live report (secure embed only)
            if (reportInstance && reportInstance.navigateToPage) {
                reportInstance.navigateToPage(pageName);
            }
            // In publish-to-web iframe mode, the iframe handles its own navigation.
            // Buttons remain as a visual navigation aid and fallback reference.
        });
    });
}

function updateActiveNavButton(pageName) {
    const btns = document.querySelectorAll('.pb-nav-btn');
    btns.forEach(btn => {
        const label = btn.getAttribute('data-page');
        const mapped = POWERBI_PAGE_MAP[label] || label;
        if (mapped === pageName) {
            btns.forEach(b => b.classList.remove('pb-nav-active'));
            btn.classList.add('pb-nav-active');
        }
    });
}

/**
 * Debounced resize handler — prevents repeatedly destroying/recreating
 * the embed on every window resize event.
 */
function onEmbedResize() {
    if (resizeTimeout) clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // For iframe embeds, the iframe already resizes via CSS (100% width/height).
        // For secure embed, call the SDK resize method if available.
        if (powerbiEmbedInstance && typeof powerbiEmbedInstance.resize === 'function') {
            powerbiEmbedInstance.resize();
        }
    }, 200);
}

/**
 * Show the embed error state and hide the live viewer.
 */
function showEmbedError(message) {
    const errorBox = document.getElementById('pbix-error');
    const errorMsg = document.getElementById('pbix-error-message');
    const statusDot = document.querySelector('.pbix-status-dot');
    const statusText = document.getElementById('pbix-status-text');

    if (errorBox) errorBox.style.display = 'flex';
    if (errorMsg) errorMsg.textContent = message;
    if (statusDot) statusDot.className = 'pbix-status-dot error';
    if (statusText) statusText.textContent = 'Embed error — see below';

    console.error('Power BI embed error:', message);
}

/* ============================================================================
   Existing functionality (preserved)
   ============================================================================ */

/**
 * Mobile menu toggle
 */
function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (!navToggle || !navLinks) return;

    navToggle.addEventListener('click', function() {
        const isActive = navLinks.classList.contains('active');
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', !isActive);
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            navToggle.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });
}

/**
 * Navbar background on scroll
 */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    window.addEventListener('scroll', function() {
        if (window.scrollY > 20) {
            navbar.style.boxShadow = '0 1px 3px 0 rgb(0 0 0 / 0.1)';
        } else {
            navbar.style.boxShadow = 'none';
        }
    });
}

/**
 * Scroll animation observer
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -60px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll(
        '.overview-card, .tech-card, .arch-step, .dashboard-page, ' +
        '.accordion-item, .de-card, .excel-card, .tm-card, .deliverable-card, ' +
        '.release-card, .feature-card, .metric-card, .stat-card, .scope-item, ' +
        '.pbix-analytic-card'
    ).forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#') && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

/**
 * Typing effect for hero title
 */
function initTypeWriter() {
    const heroTitle = document.querySelector('.hero h1');
    if (!heroTitle) return;

    const originalText = heroTitle.textContent;
    heroTitle.textContent = '';
    heroTitle.style.opacity = '1';

    let i = 0;
    const speed = 45;

    function typeWriter() {
        if (i < originalText.length) {
            heroTitle.textContent = originalText.slice(0, i + 1);
            i++;
            setTimeout(typeWriter, speed);
        }
    }

    setTimeout(typeWriter, 400);
}

/**
 * Accordion toggle for dashboard deep dive
 */
function initAccordions() {
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', function() {
            const item = this.parentElement;
            const isOpen = item.classList.contains('open');

            // Close all other accordion items
            document.querySelectorAll('.accordion-item.open').forEach(openItem => {
                openItem.classList.remove('open');
                const arrow = openItem.querySelector('.accordion-arrow');
                if (arrow) arrow.style.transform = 'rotate(0deg)';
            });

            // Toggle current item
            if (!isOpen) {
                item.classList.add('open');
                const arrow = this.querySelector('.accordion-arrow');
                if (arrow) arrow.style.transform = 'rotate(180deg)';
                const content = this.nextElementSibling;
                if (content) content.style.display = 'block';
            }
        });
    });
}

function toggleAccordion(header) {
    header.click();
}

/**
 * Click-to-zoom for dashboard mockup cards
 */
function initDashboardZoom() {
    document.querySelectorAll('.dashboard-page').forEach(page => {
        page.addEventListener('click', function(e) {
            // Don't trigger if clicking links or accordion controls
            if (e.target.closest('a') || e.target.closest('.accordion-header')) return;

            const mockup = this.querySelector('.dp-mockup');
            if (!mockup) return;

            createZoomViewer(mockup.innerHTML, this.querySelector('h3').textContent);
        });
    });
}

/**
 * Full-screen image/content viewer
 */
function createZoomViewer(contentHTML, title) {
    // Remove existing viewer
    const existing = document.querySelector('.zoom-viewer');
    if (existing) existing.remove();

    const viewer = document.createElement('div');
    viewer.className = 'zoom-viewer';
    viewer.innerHTML = `
        <div class="zoom-backdrop"></div>
        <div class="zoom-container">
            <div class="zoom-header">
                <span class="zoom-title">${escapeHtml(title)} — Dashboard View</span>
                <button class="zoom-close" aria-label="Close">✕</button>
            </div>
            <div class="zoom-content">
                ${contentHTML}
            </div>
            <p class="zoom-hint">Press ESC or click outside to close</p>
        </div>
    `;

    document.body.appendChild(viewer);
    document.body.style.overflow = 'hidden';

    // Animate in
    requestAnimationFrame(() => {
        viewer.classList.add('open');
    });

    const closeViewer = () => {
        viewer.classList.remove('open');
        setTimeout(() => {
            viewer.remove();
            document.body.style.overflow = '';
        }, 250);
    };

    viewer.querySelector('.zoom-close').addEventListener('click', closeViewer);
    viewer.querySelector('.zoom-backdrop').addEventListener('click', closeViewer);

    document.addEventListener('keydown', function escHandler(e) {
        if (e.key === 'Escape') {
            closeViewer();
            document.removeEventListener('keydown', escHandler);
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/* ============================================================================
   Native Power BI Dashboard Engine
   ============================================================================ */

const DASHBOARD_CONFIG = {
    dataPath: 'deliverables/data/',
    fileCache: {},
    chartInstances: {},
    fullscreenActive: false
};

// Column mappings for each fact table
const FACT_COLUMNS = {
    fact_flight_operations: [
        'FlightOperationKey', 'FlightLegID', 'FlightNumber', 'AirlineKey', 'RouteKey',
        'AircraftKey', 'ScheduledDepartureTimestampUTC', 'ActualDepartureTimestampUTC',
        'ScheduledArrivalTimestampUTC', 'ActualArrivalTimestampUTC', 'ScheduledDepartureDateKey',
        'ScheduledArrivalDateKey', 'AvailableSeats', 'BookedPassengers', 'RevenuePassengers',
        'NonRevenuePassengers', 'FlightDistanceKM', 'FlightStatus', 'DepartureDelayMinutes',
        'ArrivalDelayMinutes', 'BlockMinutes', 'CancellationFlag', 'CompletionFlag',
        'OnTimeFlag', 'OnTimeArrivalFlag'
    ],
    fact_disruptions: [
        'DisruptionKey', 'DisruptionID', 'FlightOperationKey', 'AirlineKey', 'RouteKey',
        'EventLocationAirportKey', 'DisruptionTypeKey', 'EventSequence', 'EventDateKey',
        'EventStartTimestampUTC', 'EventEndTimestampUTC', 'DelayMinutes', 'PrimaryCauseFlag',
        'ReactionaryFlag', 'ReactionaryEvidenceID', 'RecoveryStatus'
    ],
    fact_customer_feedback: [
        'FeedbackKey', 'FeedbackID', 'CustomerKey', 'AirlineKey', 'FlightOperationKey',
        'RouteKey', 'FeedbackDateKey', 'FeedbackType', 'SatisfactionScore', 'ComplaintCategory',
        'ServiceRecoveryFlag', 'ResolutionStatus', 'ResolutionDateKey', 'FeedbackChannel'
    ],
    fact_booking_transactions: [
        'BookingTransactionKey', 'BookingReference', 'TicketNumber', 'TicketCouponNumber',
        'CustomerKey', 'AirlineKey', 'FlightOperationKey', 'RouteKey', 'FareClassKey',
        'BookingChannelKey', 'BookingDateKey', 'TravelDateKey', 'PassengerCount',
        'IsRevenuePassenger', 'BaseFareUSD', 'DiscountAmount', 'TaxAmount', 'FeeAmount',
        'AncillaryRevenueAmount', 'RefundAmount', 'AncillaryRefundAmount', 'FeeRefundAmount',
        'CancellationFeeAmount', 'NoShowFeeUSD', 'NetPassengerRevenueUSD', 'NetFeeRevenueUSD',
        'NetAncillaryRevenueUSD', 'TransactionStatus', 'IsRefunded'
    ],
    fact_operating_costs: [
        'OperatingCostKey', 'CostLineID', 'FlightOperationKey', 'AirlineKey', 'RouteKey',
        'CostDateKey', 'CostCategory', 'CostSubcategory', 'CostAmountUSD', 'CostDescription'
    ]
};

// Dimension column mappings
const DIM_COLUMNS = {
    dim_airline: ['AirlineKey', 'AirlineId', 'AirlineIATACode', 'AirlineICAOCode', 'AirlineName', 'HomeCountry'],
    dim_booking_channel: ['BookingChannelKey', 'ChannelCode', 'ChannelName'],
    dim_disruption_type: ['DisruptionTypeKey', 'DisruptionCode', 'DisruptionName', 'DisruptionCategory'],
    dim_fare_class: ['FareClassKey', 'FareClassCode', 'FareClassName', 'CabinClass'],
    dim_route: ['RouteKey', 'RouteCode', 'OriginAirportKey', 'DestinationAirportKey', 'DistanceKM'],
    dim_currency: ['CurrencyKey', 'CurrencyCode'],
    dim_customer: ['CustomerKey', 'CustomerID', 'CustomerSegment', 'LoyaltyTier']
};

/**
 * Parse CSV text into array of objects
 */
function parseCSV(text) {
    const lines = text.trim().split(/\r?\n/);
    if (lines.length === 0) return [];
    const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
    const rows = [];
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim().replace(/^"|"$/g, ''));
        const row = {};
        headers.forEach((h, idx) => {
            row[h] = idx < values.length ? values[idx] : '';
        });
        rows.push(row);
    }
    return rows;
}

/**
 * Load a CSV file and cache it
 */
async function loadCSV(filename) {
    if (DASHBOARD_CONFIG.fileCache[filename]) {
        return DASHBOARD_CONFIG.fileCache[filename];
    }
    try {
        const response = await fetch(DASHBOARD_CONFIG.dataPath + filename);
        if (!response.ok) throw new Error(`Failed to load ${filename}: ${response.status}`);
        const text = await response.text();
        const data = parseCSV(text);
        DASHBOARD_CONFIG.fileCache[filename] = data;
        return data;
    } catch (err) {
        console.error(`Error loading ${filename}:`, err);
        return [];
    }
}

/**
 * Convert string to number safely
 */
function toNum(val) {
    const n = parseFloat(val);
    return isNaN(n) ? 0 : n;
}

/**
 * Convert string date key (YYYYMMDD) to Date object
 */
function parseDateKey(key) {
    const s = String(key);
    if (s.length === 8) {
        return new Date(s.substring(0, 4), s.substring(4, 6) - 1, s.substring(6, 8));
    }
    return null;
}

/**
 * Dashboard state - filters
 */
const DASHBOARD_STATE = {
    airline: 'all',
    dateRange: 'all',
    channel: 'all',
    data: null,
    dims: null,
    loaded: false
};

// Root element for chart rendering (defaults to document; set to fullscreen clone when fullscreen is active)
let _currentRenderRoot = document;

/**
 * Load all dashboard data
 */
async function loadDashboardData() {
    if (DASHBOARD_STATE.loaded) return;

    const loadPromises = {
        flights: loadCSV('fact_flight_operations.csv'),
        disruptions: loadCSV('fact_disruptions.csv'),
        feedback: loadCSV('fact_customer_feedback.csv'),
        bookings: loadCSV('fact_booking_transactions.csv'),
        costs: loadCSV('fact_operating_costs.csv'),
        airlines: loadCSV('dim_airline.csv'),
        channels: loadCSV('dim_booking_channel.csv'),
        disruptionTypes: loadCSV('dim_disruption_type.csv'),
        fareClasses: loadCSV('dim_fare_class.csv')
    };

    const results = await Promise.allSettled(Object.values(loadPromises));
    const keys = Object.keys(loadPromises);
    const data = {};

    keys.forEach((key, idx) => {
        if (results[idx].status === 'fulfilled') {
            data[key] = results[idx].value;
        } else {
            console.error(`Failed to load ${key}:`, results[idx].reason);
            data[key] = [];
        }
    });

    DASHBOARD_STATE.data = data;
    DASHBOARD_STATE.dims = {
        airlines: data.airlines,
        channels: data.channels,
        disruptionTypes: data.disruptionTypes,
        fareClasses: data.fareClasses
    };
    DASHBOARD_STATE.loaded = true;

    // Populate slicer dropdowns
    populateSlicers();

    // Initialize dashboard
    initDashboardNavigation();
    renderDashboard();
}

/**
 * Populate slicer dropdown options
 */
function populateSlicers() {
    const { airlines, channels } = DASHBOARD_STATE.dims;

    const airlineSelect = document.getElementById('dash-slicer-airline');
    const channelSelect = document.getElementById('dash-slicer-channel');

    if (airlineSelect && airlines) {
        airlines.forEach(a => {
            const opt = document.createElement('option');
            opt.value = a.AirlineKey;
            opt.textContent = a.AirlineName || a.AirlineIATACode || 'Unknown';
            airlineSelect.appendChild(opt);
        });
    }

    if (channelSelect && channels) {
        channels.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.BookingChannelKey;
            opt.textContent = c.ChannelName || c.ChannelCode || 'Unknown';
            channelSelect.appendChild(opt);
        });
    }
}

/**
 * Apply filters to a fact table row
 */
function passesFilters(row, tableType) {
    const { airline, dateRange, channel } = DASHBOARD_STATE;

    // Airline filter
    if (airline !== 'all') {
        const rowAirline = row.AirlineKey;
        if (rowAirline != airline) return false;
    }

    // Booking channel filter (only applies to bookings)
    if (channel !== 'all' && tableType === 'bookings') {
        if (row.BookingChannelKey != channel) return false;
    }

    // Date range filter
    if (dateRange !== 'all') {
        let dateKey = null;
        if (tableType === 'flights') {
            dateKey = row.ScheduledDepartureDateKey;
        } else if (tableType === 'disruptions') {
            dateKey = row.EventDateKey;
        } else if (tableType === 'feedback') {
            dateKey = row.FeedbackDateKey;
        } else if (tableType === 'bookings') {
            dateKey = row.TravelDateKey;
        } else if (tableType === 'costs') {
            dateKey = row.CostDateKey;
        }

        if (dateKey) {
            const date = parseDateKey(dateKey);
            if (date) {
                const year = date.getFullYear();
                const month = date.getMonth() + 1;
                let inRange = false;

                if (dateRange === 'q1' && month >= 1 && month <= 3 && year === 2026) inRange = true;
                if (dateRange === 'q2' && month >= 4 && month <= 6 && year === 2026) inRange = true;
                if (dateRange === 'q3' && month >= 7 && month <= 9 && year === 2026) inRange = true;
                if (dateRange === 'q4' && month >= 10 && month <= 12 && year === 2025) inRange = true;

                if (!inRange) return false;
            }
        }
    }

    return true;
}

/**
 * Get filtered data for a table type
 */
function getFilteredData(tableType) {
    const { data } = DASHBOARD_STATE;
    let source;

    switch (tableType) {
        case 'flights': source = data.flights; break;
        case 'disruptions': source = data.disruptions; break;
        case 'feedback': source = data.feedback; break;
        case 'bookings': source = data.bookings; break;
        case 'costs': source = data.costs; break;
        default: return [];
    }

    return source.filter(row => passesFilters(row, tableType));
}

/**
 * KPI Computations
 */
function computeKPIs() {
    const flights = getFilteredData('flights');
    const disruptions = getFilteredData('disruptions');
    const feedback = getFilteredData('feedback');
    const bookings = getFilteredData('bookings');
    const costs = getFilteredData('costs');
    const airlines = DASHBOARD_STATE.dims.airlines;

    const airlineMap = {};
    airlines.forEach(a => { airlineMap[a.AirlineKey] = a.AirlineName || a.AirlineIATACode; });

    // FL01: Flights Operated
    const fl01 = flights.filter(f => f.FlightStatus === 'Operated').length;

    // FL02: Revenue Passengers
    const fl02 = flights.reduce((sum, f) => sum + toNum(f.RevenuePassengers), 0);

    // FL03: Average Departure Delay
    const fl03Valid = flights.filter(f => f.CompletionFlag === 'True' && f.DepartureDelayMinutes !== '');
    const fl03 = fl03Valid.length > 0
        ? fl03Valid.reduce((sum, f) => sum + toNum(f.DepartureDelayMinutes), 0) / fl03Valid.length
        : 0;

    // FL04: Cancellation Rate
    const fl04Total = flights.length;
    const fl04Cancelled = flights.filter(f => f.CancellationFlag === 'True').length;
    const fl04 = fl04Total > 0 ? (fl04Cancelled / fl04Total) * 100 : 0;

    // DS01: Total Disruptions
    const ds01 = disruptions.length;

    // OP01: On-Time Performance
    const op01Valid = flights.filter(f => f.CompletionFlag === 'True' && f.DepartureDelayMinutes !== '');
    const op01OnTime = op01Valid.filter(f => f.OnTimeFlag === 'True').length;
    const op01 = op01Valid.length > 0 ? (op01OnTime / op01Valid.length) * 100 : 0;

    // OP03: Average Arrival Delay
    const op03Valid = flights.filter(f => f.CompletionFlag === 'True' && f.ArrivalDelayMinutes !== '');
    const op03 = op03Valid.length > 0
        ? op03Valid.reduce((sum, f) => sum + toNum(f.ArrivalDelayMinutes), 0) / op03Valid.length
        : 0;

    // OP04: Flight Completion Rate
    const op04 = fl04Total > 0
        ? (flights.filter(f => f.CompletionFlag === 'True').length / fl04Total) * 100
        : 0;

    // Revenue measures
    const rvTotal = bookings.reduce((sum, b) => sum + toNum(b.NetPassengerRevenueUSD) + toNum(b.NetFeeRevenueUSD) + toNum(b.NetAncillaryRevenueUSD), 0);
    const rvPassenger = bookings.reduce((sum, b) => sum + toNum(b.NetPassengerRevenueUSD), 0);
    const rvFee = bookings.reduce((sum, b) => sum + toNum(b.NetFeeRevenueUSD), 0);
    const rvAncillary = bookings.reduce((sum, b) => sum + toNum(b.NetAncillaryRevenueUSD), 0);
    const rvPassengers = bookings.reduce((sum, b) => (b.IsRevenuePassenger === 'True' ? sum + toNum(b.PassengerCount) : sum), 0);
    const rvAvg = rvPassengers > 0 ? rvTotal / rvPassengers : 0;

    // Cost measures
    const cxTotal = costs.reduce((sum, c) => sum + toNum(c.CostAmountUSD), 0);
    const cxPositive = costs.reduce((sum, c) => toNum(c.CostAmountUSD) > 0 ? sum + toNum(c.CostAmountUSD) : sum, 0);
    const cxReversals = costs.reduce((sum, c) => toNum(c.CostAmountUSD) < 0 ? sum + toNum(c.CostAmountUSD) : sum, 0);
    const cxNet = cxTotal;
    const cxPerFlight = fl01 > 0 ? cxTotal / fl01 : 0;
    const cxPerPass = rvPassengers > 0 ? cxTotal / rvPassengers : 0;

    // NC measures
    const ncContribution = rvTotal - cxTotal;
    const ncRatio = cxTotal > 0 ? rvTotal / cxTotal : 0;

    // Customer measures
    const cfTotal = feedback.length;
    const cfComplaints = feedback.filter(f => f.FeedbackType === 'Complaint').length;
    const cfComplaintRate = cfTotal > 0 ? (cfComplaints / cfTotal) * 100 : 0;
    const cfSatisfactionValid = feedback.filter(f => f.SatisfactionScore !== '');
    const cfSatisfaction = cfSatisfactionValid.length > 0
        ? cfSatisfactionValid.reduce((sum, f) => sum + toNum(f.SatisfactionScore), 0) / cfSatisfactionValid.length
        : 0;
    const cfActive = new Set(feedback.filter(f => f.CustomerKey).map(f => f.CustomerKey)).size;
    const cfCompliment = feedback.filter(f => f.FeedbackType === 'Compliment').length;
    const cfClaim = feedback.filter(f => f.FeedbackType === 'Claim').length;
    const cfSurvey = feedback.filter(f => f.FeedbackType === 'Survey').length;

    return {
        fl01, fl02, fl03, fl04, ds01,
        op01, op03, op04,
        rvTotal, rvPassenger, rvFee, rvAncillary, rvPassengers, rvAvg,
        cxTotal, cxPositive, cxReversals, cxNet, cxPerFlight, cxPerPass,
        ncContribution, ncRatio,
        cfTotal, cfComplaintRate, cfSatisfaction, cfActive, cfComplaints, cfCompliment, cfClaim, cfSurvey,
        scheduled: fl04Total,
        blockMinutes: flights.reduce((sum, f) => sum + toNum(f.BlockMinutes), 0)
    };
}

/**
 * Format number with commas
 */
function formatNum(n, decimals = 0) {
    return n.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Format currency
 */
function formatCurrency(n) {
    return '$' + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Format percentage
 */
function formatPercent(n) {
    return n.toFixed(1) + '%';
}

/**
 * Update KPI displays
 */
function updateKPIs(kpis, pageId) {
    const el = (id, val) => {
        const elem = document.getElementById(id);
        if (elem) elem.textContent = val;
    };

    if (pageId === 'page01' || pageId === 'all') {
        el('kpi-fl01', formatNum(kpis.fl01));
        el('kpi-fl02', formatNum(kpis.fl02));
        el('kpi-fl03', kpis.fl03.toFixed(1) + ' min');
        el('kpi-fl04', formatPercent(kpis.fl04));
        el('kpi-ds01', formatNum(kpis.ds01));
    }
    if (pageId === 'page02' || pageId === 'all') {
        el('kpi-op01', formatPercent(kpis.op01));
        el('kpi-op03-dep', kpis.fl03.toFixed(1) + ' min');
        el('kpi-op03-arr', kpis.op03.toFixed(1) + ' min');
        el('kpi-op04', formatPercent(kpis.op04));
        el('kpi-sched', formatNum(kpis.scheduled));
        el('kpi-block', formatNum(kpis.blockMinutes));
    }
    if (pageId === 'page03' || pageId === 'all') {
        el('kpi-rv-total', formatCurrency(kpis.rvTotal));
        el('kpi-rv-passenger', formatCurrency(kpis.rvPassenger));
        el('kpi-rv-fee', formatCurrency(kpis.rvFee));
        el('kpi-rv-ancillary', formatCurrency(kpis.rvAncillary));
        el('kpi-rv-passengers', formatNum(kpis.rvPassengers));
        el('kpi-rv-avg', formatCurrency(kpis.rvAvg));
    }
    if (pageId === 'page04' || pageId === 'all') {
        el('kpi-cx-total', formatCurrency(kpis.cxTotal));
        el('kpi-cx-positive', formatCurrency(kpis.cxPositive));
        el('kpi-cx-reversals', formatCurrency(Math.abs(kpis.cxReversals)));
        el('kpi-cx-net', formatCurrency(kpis.cxNet));
        el('kpi-cx-perflight', formatCurrency(kpis.cxPerFlight));
        el('kpi-cx-perpass', formatCurrency(kpis.cxPerPass));
        el('kpi-nc-contribution', formatCurrency(kpis.ncContribution));
        el('kpi-nc-ratio', kpis.ncRatio.toFixed(4));
    }
    if (pageId === 'page05' || pageId === 'all') {
        el('kpi-cf-total', formatNum(kpis.cfTotal));
        el('kpi-cf-complaint', formatPercent(kpis.cfComplaintRate));
        el('kpi-cf-satisfaction', kpis.cfSatisfaction.toFixed(2) + ' / 5');
        el('kpi-cf-active', formatNum(kpis.cfActive));
        el('kpi-cf-complaint-count', formatNum(kpis.cfComplaints));
        el('kpi-cf-compliment', formatNum(kpis.cfCompliment));
        el('kpi-cf-claim', formatNum(kpis.cfClaim));
        el('kpi-cf-survey', formatNum(kpis.cfSurvey));
    }
}

/**
 * Chart color palette
 */
const CHART_COLORS = {
    primary: '#63B3A5',
    accent: '#D6A45D',
    teal: '#63B3A5',
    navy: '#78A9C8',
    blueLight: '#A99BCB',
    red: '#DF8C82',
    orange: '#E3B45F',
    green: '#79B88C',
    purple: '#A99BCB',
    gray: '#87959E'
};

const CHART_COLORS_ARRAY = [
    '#63B3A5', '#D6A45D', '#78A9C8', '#A99BCB', '#DF8C82',
    '#79B88C', '#E3B45F', '#7CC8B9', '#5C8FA8', '#4A6B5A'
];

/**
 * Destroy existing chart if present
 */
function destroyChart(chartId) {
    if (DASHBOARD_CONFIG.chartInstances[chartId]) {
        DASHBOARD_CONFIG.chartInstances[chartId].destroy();
        DASHBOARD_CONFIG.chartInstances[chartId] = null;
    }
}

/**
 * Create or update a chart
 */
function createChart(chartId, type, data, options = {}) {
    destroyChart(chartId);
    const ctx = _currentRenderRoot.querySelector('#' + chartId);
    if (!ctx) return;

    // Wrap canvas in a positioned container so Chart.js has a definite
    // height to measure. Without this, canvas height -> panel height ->
    // grid row height -> canvas height feedback loop grows without bound.
    let wrap = ctx.parentElement;
    if (!wrap.classList.contains('chart-wrap')) {
        wrap = document.createElement('div');
        wrap.className = 'chart-wrap';
        ctx.parentNode.insertBefore(wrap, ctx);
        wrap.appendChild(ctx);
    }

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        animations: {
            colors: false,
            x: false,
            y: false
        },
        transitions: {
            active: { animation: { duration: 0 } },
            resize: { animation: { duration: 0 } },
            show: { animations: { colors: false, x: false, y: false } },
            hide: { animations: { colors: false, x: false, y: false } }
        },
        plugins: {
            legend: {
                position: 'bottom',
                labels: { color: '#B6C0C5', font: { size: 11 }, usePointStyle: true, boxWidth: 8 }
            },
            tooltip: {
                backgroundColor: 'rgba(16, 24, 32, 0.95)',
                titleColor: '#F4F1E8',
                bodyColor: '#B6C0C5',
                borderColor: '#34434D',
                borderWidth: 1,
                padding: 10,
                cornerRadius: 4
            }
        },
        scales: {
            x: {
                ticks: { color: '#87959E', font: { size: 10 } },
                grid: { color: 'rgba(52, 67, 77, 0.45)' },
                border: { color: '#34434D' }
            },
            y: {
                ticks: { color: '#87959E', font: { size: 10 } },
                grid: { color: 'rgba(52, 67, 77, 0.45)' },
                border: { color: '#34434D' }
            }
        },
        ...options
    };

    // Merge caller-supplied scales with theme defaults (caller wins per axis,
    // but inherits tick/grid colours so every chart stays on-theme)
    if (options && options.scales) {
        const themeScales = {
            x: { ticks: { color: '#87959E', font: { size: 10 } }, grid: { color: 'rgba(52, 67, 77, 0.45)' }, border: { color: '#34434D' } },
            y: { ticks: { color: '#87959E', font: { size: 10 } }, grid: { color: 'rgba(52, 67, 77, 0.45)' }, border: { color: '#34434D' } }
        };
        const merged = {};
        const axes = new Set([...Object.keys(themeScales), ...Object.keys(options.scales)]);
        axes.forEach(axis => {
            merged[axis] = {
                ...(themeScales[axis] || {}),
                ...(options.scales[axis] || {})
            };
        });
        defaultOptions.scales = merged;
    }

    // Pie/doughnut charts have no axes — hide scale rendering entirely
    if (type === 'pie' || type === 'doughnut') {
        defaultOptions.scales = {};
        defaultOptions.plugins.legend.position = 'bottom';
    }

    // Chart.js defaults for dark theme
    Chart.defaults.color = '#B6C0C5';
    Chart.defaults.borderColor = 'rgba(52, 67, 77, 0.45)';
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.font.size = 11;
    Chart.defaults.plugins.legend.labels.color = '#B6C0C5';
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(16, 24, 32, 0.95)';
    Chart.defaults.plugins.tooltip.titleColor = '#F4F1E8';
    Chart.defaults.plugins.tooltip.bodyColor = '#B6C0C5';
    Chart.defaults.plugins.tooltip.borderColor = '#34434D';

    DASHBOARD_CONFIG.chartInstances[chartId] = new Chart(ctx, {
        type,
        data,
        options: defaultOptions
    });
}

/**
 * Render charts for current page
 */
function renderCharts(pageId, root = document) {
    _currentRenderRoot = root;
    const flights = getFilteredData('flights');
    const disruptions = getFilteredData('disruptions');
    const feedback = getFilteredData('feedback');
    const bookings = getFilteredData('bookings');
    const costs = getFilteredData('costs');
    const airlines = DASHBOARD_STATE.dims.airlines;
    const airlineMap = {};
    airlines.forEach(a => { airlineMap[a.AirlineKey] = a.AirlineName || a.AirlineIATACode || 'Unknown'; });

    const channelMap = {};
    DASHBOARD_STATE.dims.channels.forEach(c => { channelMap[c.BookingChannelKey] = c.ChannelName || c.ChannelCode; });

    const disruptionTypeMap = {};
    DASHBOARD_STATE.dims.disruptionTypes.forEach(d => { disruptionTypeMap[d.DisruptionTypeKey] = d.DisruptionName || d.DisruptionCode; });

    if (pageId === 'page01' || pageId === 'all') {
        // Monthly trend
        const monthly = {};
        flights.forEach(f => {
            const d = parseDateKey(f.ScheduledDepartureDateKey);
            if (d) {
                const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
                if (!monthly[key]) monthly[key] = { flights: 0, passengers: 0 };
                monthly[key].flights += f.CompletionFlag === 'True' ? 1 : 0;
                monthly[key].passengers += toNum(f.RevenuePassengers);
            }
        });
        const months = Object.keys(monthly).sort();
        createChart('chart-trend', 'line', {
            labels: months.map(m => {
                const [y, mo] = m.split('-');
                return new Date(y, mo - 1).toLocaleDateString('en-US', { month: 'short' });
            }),
            datasets: [
                { label: 'Flights Operated', data: months.map(m => monthly[m].flights), borderColor: CHART_COLORS.primary, fill: false, tension: 0.3 },
                { label: 'Revenue Passengers', data: months.map(m => monthly[m].passengers), borderColor: CHART_COLORS.accent, fill: false, tension: 0.3, yAxisID: 'y1' }
            ]
        }, {
            scales: { y: { beginAtZero: true, title: { display: true, text: 'Flights' } }, y1: { beginAtZero: true, title: { display: true, text: 'Passengers' }, position: 'right', grid: { drawOnChartArea: false } } }
        });

        // Disruptions by Airline
        const disruptionByAirline = {};
        disruptions.forEach(d => {
            const name = airlineMap[d.AirlineKey] || 'Unknown';
            disruptionByAirline[name] = (disruptionByAirline[name] || 0) + 1;
        });
        const dlabels = Object.keys(disruptionByAirline);
        createChart('chart-disruptions-airline', 'bar', {
            labels: dlabels,
            datasets: [{ label: 'Disruptions', data: dlabels.map(l => disruptionByAirline[l]), backgroundColor: CHART_COLORS_ARRAY }]
        });

        // Disruptions by Category
        const disruptionByCategory = {};
        disruptions.forEach(d => {
            const name = disruptionTypeMap[d.DisruptionTypeKey] || 'Unknown';
            disruptionByCategory[name] = (disruptionByCategory[name] || 0) + 1;
        });
        const clabels = Object.keys(disruptionByCategory);
        createChart('chart-disruptions-category', 'bar', {
            labels: clabels,
            datasets: [{ label: 'Disruptions', data: clabels.map(l => disruptionByCategory[l]), backgroundColor: CHART_COLORS.primary }]
        }, { indexAxis: 'y' });

        // Disruptions Donut (Controllable vs Non-controllable)
        const controllable = disruptions.filter(d => d.PrimaryCauseFlag === 'True').length;
        const nonControllable = disruptions.length - controllable;
        createChart('chart-disruptions-donut', 'doughnut', {
            labels: ['Controllable', 'Non-Controllable'],
            datasets: [{ data: [controllable, nonControllable], backgroundColor: [CHART_COLORS.red, CHART_COLORS.gray] }]
        }, { cutout: '70%', plugins: { legend: { position: 'bottom' } } });
    }

    if (pageId === 'page02' || pageId === 'all') {
        // OTP Trend (mock monthly)
        const monthlyOTP = {};
        flights.forEach(f => {
            const d = parseDateKey(f.ScheduledDepartureDateKey);
            if (d) {
                const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
                if (!monthlyOTP[key]) monthlyOTP[key] = { total: 0, ontime: 0 };
                monthlyOTP[key].total += f.CompletionFlag === 'True' ? 1 : 0;
                monthlyOTP[key].ontime += (f.CompletionFlag === 'True' && f.OnTimeFlag === 'True') ? 1 : 0;
            }
        });
        const otpMonths = Object.keys(monthlyOTP).sort();
        createChart('chart-otp-trend', 'line', {
            labels: otpMonths.map(m => {
                const [y, mo] = m.split('-');
                return new Date(y, mo - 1).toLocaleDateString('en-US', { month: 'short' });
            }),
            datasets: [{ label: 'OTP %', data: otpMonths.map(m => monthlyOTP[m].total > 0 ? ((monthlyOTP[m].ontime / monthlyOTP[m].total) * 100).toFixed(1) : 0), borderColor: CHART_COLORS.primary, fill: false, tension: 0.3 }]
        }, { scales: { y: { beginAtZero: true, max: 100, title: { display: true, text: 'OTP %' } } } });

        // Flights by Status
        const statusCounts = {};
        flights.forEach(f => {
            const status = f.FlightStatus || 'Unknown';
            statusCounts[status] = (statusCounts[status] || 0) + 1;
        });
        createChart('chart-flight-status', 'doughnut', {
            labels: Object.keys(statusCounts),
            datasets: [{ data: Object.values(statusCounts), backgroundColor: CHART_COLORS_ARRAY }]
        }, { cutout: '70%' });

        // Block Minutes by Airline
        const blockByAirline = {};
        flights.forEach(f => {
            const name = airlineMap[f.AirlineKey] || 'Unknown';
            blockByAirline[name] = (blockByAirline[name] || 0) + toNum(f.BlockMinutes);
        });
        const baLabels = Object.keys(blockByAirline);
        createChart('chart-block-minutes', 'bar', {
            labels: baLabels,
            datasets: [{ label: 'Block Minutes', data: baLabels.map(l => blockByAirline[l]), backgroundColor: CHART_COLORS.primary }]
        });

        // Ops by Route (top 10)
        const routeOps = {};
        flights.forEach(f => {
            routeOps[f.RouteKey] = (routeOps[f.RouteKey] || 0) + 1;
        });
        const topRoutes = Object.entries(routeOps).sort((a, b) => b[1] - a[1]).slice(0, 10);
        createChart('chart-ops-route', 'bar', {
            labels: topRoutes.map(r => 'Route ' + r[0]),
            datasets: [{ label: 'Flights', data: topRoutes.map(r => r[1]), backgroundColor: CHART_COLORS.teal }]
        }, { indexAxis: 'y' });

        // Status by Month
        const statusByMonth = {};
        flights.forEach(f => {
            const d = parseDateKey(f.ScheduledDepartureDateKey);
            if (d) {
                const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
                if (!statusByMonth[key]) statusByMonth[key] = {};
                statusByMonth[key][f.FlightStatus] = (statusByMonth[key][f.FlightStatus] || 0) + 1;
            }
        });
        const smMonths = Object.keys(statusByMonth).sort();
        const statuses = ['Operated', 'Cancelled', 'Diverted'];
        createChart('chart-status-month', 'bar', {
            labels: smMonths.map(m => {
                const [y, mo] = m.split('-');
                return new Date(y, mo - 1).toLocaleDateString('en-US', { month: 'short' });
            }),
            datasets: statuses.map((s, i) => ({
                label: s,
                data: smMonths.map(m => statusByMonth[m][s] || 0),
                backgroundColor: CHART_COLORS_ARRAY[i % CHART_COLORS_ARRAY.length]
            }))
        }, { stacked: true });
    }

    if (pageId === 'page03' || pageId === 'all') {
        // Revenue Trend
        const monthlyRev = {};
        bookings.forEach(b => {
            const d = parseDateKey(b.TravelDateKey);
            if (d) {
                const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
                monthlyRev[key] = (monthlyRev[key] || 0) + toNum(b.NetPassengerRevenueUSD) + toNum(b.NetFeeRevenueUSD) + toNum(b.NetAncillaryRevenueUSD);
            }
        });
        const revMonths = Object.keys(monthlyRev).sort();
        createChart('chart-revenue-trend', 'line', {
            labels: revMonths.map(m => {
                const [y, mo] = m.split('-');
                return new Date(y, mo - 1).toLocaleDateString('en-US', { month: 'short' });
            }),
            datasets: [{ label: 'Revenue (USD)', data: revMonths.map(m => monthlyRev[m]), borderColor: CHART_COLORS.primary, fill: false, tension: 0.3 }]
        });

        // Revenue Composition (Donut)
        createChart('chart-revenue-composition', 'doughnut', {
            labels: ['Passenger Revenue', 'Fee Revenue', 'Ancillary Revenue'],
            datasets: [{ data: [flights.length > 0 ? bookings.reduce((s, b) => s + toNum(b.NetPassengerRevenueUSD), 0) : 0, bookings.reduce((s, b) => s + toNum(b.NetFeeRevenueUSD), 0), bookings.reduce((s, b) => s + toNum(b.NetAncillaryRevenueUSD), 0)], backgroundColor: [CHART_COLORS.primary, CHART_COLORS.accent, CHART_COLORS.teal] }]
        }, { cutout: '70%' });

        // Revenue by Channel
        const revByChannel = {};
        bookings.forEach(b => {
            const name = channelMap[b.BookingChannelKey] || 'Unknown';
            revByChannel[name] = (revByChannel[name] || 0) + toNum(b.NetPassengerRevenueUSD) + toNum(b.NetFeeRevenueUSD) + toNum(b.NetAncillaryRevenueUSD);
        });
        const chLabels = Object.keys(revByChannel);
        createChart('chart-revenue-channel', 'bar', {
            labels: chLabels,
            datasets: [{ label: 'Revenue', data: chLabels.map(l => revByChannel[l]), backgroundColor: CHART_COLORS_ARRAY }]
        }, { indexAxis: 'y' });

        // Revenue by Fare Class
        const revByFare = {};
        bookings.forEach(b => {
            revByFare[b.FareClassKey] = (revByFare[b.FareClassKey] || 0) + toNum(b.NetPassengerRevenueUSD);
        });
        const fareLabels = Object.keys(revByFare);
        createChart('chart-revenue-fare', 'bar', {
            labels: fareLabels.map(l => 'Class ' + l),
            datasets: [{ label: 'Revenue', data: fareLabels.map(l => revByFare[l]), backgroundColor: CHART_COLORS.primary }]
        }, { indexAxis: 'y' });

        // Revenue by Airline
        const revByAirline = {};
        bookings.forEach(b => {
            const name = airlineMap[b.AirlineKey] || 'Unknown';
            revByAirline[name] = (revByAirline[name] || 0) + toNum(b.NetPassengerRevenueUSD) + toNum(b.NetFeeRevenueUSD) + toNum(b.NetAncillaryRevenueUSD);
        });
        const arLabels = Object.keys(revByAirline);
        createChart('chart-revenue-airline', 'bar', {
            labels: arLabels,
            datasets: [{ label: 'Revenue', data: arLabels.map(l => revByAirline[l]), backgroundColor: CHART_COLORS.primary }]
        });

        // Revenue by Route (top 10)
        const revByRoute = {};
        bookings.forEach(b => {
            revByRoute[b.RouteKey] = (revByRoute[b.RouteKey] || 0) + toNum(b.NetPassengerRevenueUSD) + toNum(b.NetFeeRevenueUSD) + toNum(b.NetAncillaryRevenueUSD);
        });
        const topRevRoutes = Object.entries(revByRoute).sort((a, b) => b[1] - a[1]).slice(0, 10);
        createChart('chart-revenue-route', 'bar', {
            labels: topRevRoutes.map(r => 'Route ' + r[0]),
            datasets: [{ label: 'Revenue', data: topRevRoutes.map(r => r[1]), backgroundColor: CHART_COLORS.accent }]
        }, { indexAxis: 'y' });
    }

    if (pageId === 'page04' || pageId === 'all') {
        // Cost Trend
        const monthlyCost = {};
        costs.forEach(c => {
            const d = parseDateKey(c.CostDateKey);
            if (d) {
                const key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0');
                monthlyCost[key] = (monthlyCost[key] || 0) + toNum(c.CostAmountUSD);
            }
        });
        const costMonths = Object.keys(monthlyCost).sort();
        createChart('chart-cost-trend', 'line', {
            labels: costMonths.map(m => {
                const [y, mo] = m.split('-');
                return new Date(y, mo - 1).toLocaleDateString('en-US', { month: 'short' });
            }),
            datasets: [{ label: 'Costs (USD)', data: costMonths.map(m => monthlyCost[m]), borderColor: CHART_COLORS.primary, fill: false, tension: 0.3 }]
        });

        // Costs by Category
        const costByCategory = {};
        costs.forEach(c => {
            const cat = c.CostCategory || 'Unknown';
            costByCategory[cat] = (costByCategory[cat] || 0) + toNum(c.CostAmountUSD);
        });
        const catLabels = Object.keys(costByCategory);
        createChart('chart-cost-category', 'bar', {
            labels: catLabels,
            datasets: [{ label: 'Costs', data: catLabels.map(l => costByCategory[l]), backgroundColor: CHART_COLORS_ARRAY }]
        }, { indexAxis: 'y' });

        // Costs by Airline
        const costByAirline = {};
        costs.forEach(c => {
            const name = airlineMap[c.AirlineKey] || 'Unknown';
            costByAirline[name] = (costByAirline[name] || 0) + toNum(c.CostAmountUSD);
        });
        const caLabels = Object.keys(costByAirline);
        createChart('chart-cost-airline', 'bar', {
            labels: caLabels,
            datasets: [{ label: 'Costs', data: caLabels.map(l => costByAirline[l]), backgroundColor: CHART_COLORS.primary }]
        });

        // Route Cost Composition
        const costByRoute = {};
        costs.forEach(c => {
            costByRoute[c.RouteKey] = (costByRoute[c.RouteKey] || 0) + toNum(c.CostAmountUSD);
        });
        const topCostRoutes = Object.entries(costByRoute).sort((a, b) => b[1] - a[1]).slice(0, 10);
        createChart('chart-cost-route', 'bar', {
            labels: topCostRoutes.map(r => 'Route ' + r[0]),
            datasets: [{ label: 'Costs', data: topCostRoutes.map(r => r[1]), backgroundColor: CHART_COLORS.teal }]
        }, { indexAxis: 'y' });

        // Cost Geographic Distribution (mock by airline region)
        createChart('chart-cost-geo', 'pie', {
            labels: Object.keys(airlineMap).slice(0, 5).map(k => airlineMap[k]),
            datasets: [{ data: Object.keys(airlineMap).slice(0, 5).map(k => costByAirline[k] || 0), backgroundColor: CHART_COLORS_ARRAY }]
        });

        // Cost Efficiency vs Contribution (scatter)
        createChart('chart-cost-efficiency', 'scatter', {
            datasets: [{
                label: 'Airline Efficiency',
                data: Object.keys(airlineMap).map(k => ({
                    x: costByAirline[k] || 0,
                    y: flights.filter(f => f.AirlineKey == k).length * 100,
                    label: airlineMap[k]
                })),
                backgroundColor: CHART_COLORS.primary
            }]
        }, {
            scales: {
                x: { title: { display: true, text: 'Total Costs (USD)' } },
                y: { title: { display: true, text: 'Flights Operated' } }
            },
            plugins: { tooltip: { callbacks: { label: ctx => ctx.raw.label + ': Cost $' + ctx.raw.x + ', Flights ' + ctx.raw.y } } }
        });
    }

    if (pageId === 'page05' || pageId === 'all') {
        // Feedback by Channel
        const fbByChannel = {};
        feedback.forEach(f => {
            const ch = f.FeedbackChannel || 'Unknown';
            fbByChannel[ch] = (fbByChannel[ch] || 0) + 1;
        });
        const fbcLabels = Object.keys(fbByChannel);
        createChart('chart-feedback-channel', 'bar', {
            labels: fbcLabels,
            datasets: [{ label: 'Feedback', data: fbcLabels.map(l => fbByChannel[l]), backgroundColor: CHART_COLORS_ARRAY }]
        }, { indexAxis: 'y' });

        // Feedback by Type
        const fbByType = {};
        feedback.forEach(f => {
            const t = f.FeedbackType || 'Unknown';
            fbByType[t] = (fbByType[t] || 0) + 1;
        });
        const fbtLabels = Object.keys(fbByType);
        createChart('chart-feedback-type', 'pie', {
            labels: fbtLabels,
            datasets: [{ data: fbtLabels.map(l => fbByType[l]), backgroundColor: CHART_COLORS_ARRAY }]
        });

        // Satisfaction by Airline
        const satByAirline = {};
        const satCountByAirline = {};
        feedback.forEach(f => {
            if (f.SatisfactionScore) {
                const name = airlineMap[f.AirlineKey] || 'Unknown';
                satByAirline[name] = (satByAirline[name] || 0) + toNum(f.SatisfactionScore);
                satCountByAirline[name] = (satCountByAirline[name] || 0) + 1;
            }
        });
        const satLabels = Object.keys(satByAirline);
        createChart('chart-satisfaction-airline', 'bar', {
            labels: satLabels,
            datasets: [{ label: 'Avg Satisfaction', data: satLabels.map(l => (satByAirline[l] / satCountByAirline[l]).toFixed(2)), backgroundColor: CHART_COLORS.primary }]
        }, { indexAxis: 'y' });

        // Positive vs Negative
        const positive = feedback.filter(f => f.FeedbackType === 'Compliment').length;
        const negative = feedback.filter(f => f.FeedbackType === 'Complaint').length;
        createChart('chart-feedback-sentiment', 'doughnut', {
            labels: ['Compliments (Positive)', 'Complaints (Negative)'],
            datasets: [{ data: [positive, negative], backgroundColor: [CHART_COLORS.green, CHART_COLORS.red] }]
        }, { cutout: '70%' });

        // Complaint Category Breakdown
        const complaintByCategory = {};
        feedback.forEach(f => {
            if (f.FeedbackType === 'Complaint') {
                const cat = f.ComplaintCategory || 'Unknown';
                complaintByCategory[cat] = (complaintByCategory[cat] || 0) + 1;
            }
        });
        const ccLabels = Object.keys(complaintByCategory);
        createChart('chart-complaint-category', 'bar', {
            labels: ccLabels,
            datasets: [{ label: 'Complaints', data: ccLabels.map(l => complaintByCategory[l]), backgroundColor: CHART_COLORS.red }]
        }, { indexAxis: 'y' });

        // Customer Segment Distribution
        const segmentDist = {};
        feedback.forEach(f => {
            const seg = f.CustomerKey ? 'Segmented' : 'Unknown';
            segmentDist[seg] = (segmentDist[seg] || 0) + 1;
        });
        const sdLabels = Object.keys(segmentDist);
        createChart('chart-customer-segment', 'pie', {
            labels: sdLabels,
            datasets: [{ data: sdLabels.map(l => segmentDist[l]), backgroundColor: CHART_COLORS_ARRAY }]
        });
    }
    _currentRenderRoot = document;
}

/**
 * Initialize dashboard navigation buttons
 */
function initDashboardNavigation() {
    const btns = document.querySelectorAll('.dash-nav-item');
    btns.forEach(btn => {
        btn.addEventListener('click', function() {
            const pageId = this.getAttribute('data-page');

            // Update active button
            btns.forEach(b => {
                b.classList.remove('dash-nav-active');
                b.setAttribute('aria-pressed', 'false');
            });
            this.classList.add('dash-nav-active');
            this.setAttribute('aria-pressed', 'true');

            // Update page title
            const titleMap = {
                page01: ['Executive Overview', 'Is the airline network performing well overall?'],
                page02: ['Operations & Disruption', 'How efficiently are airline operations performing?'],
                page03: ['Revenue & Finance', 'Where does airline revenue come from?'],
                page04: ['Cost & Financial Intelligence', 'Where is the airline spending money, and how efficiently?'],
                page05: ['Customer & Service Intelligence', 'How satisfied are customers, and where does service need improvement?']
            };
            const [title, subtitle] = titleMap[pageId] || ['Dashboard', ''];
            document.getElementById('dash-page-title').textContent = title;
            document.getElementById('dash-page-subtitle').textContent = subtitle;

            // Switch pages
            document.querySelectorAll('.dash-page').forEach(p => p.classList.remove('dash-page-active'));
            const targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('dash-page-active');
                targetPage.scrollTop = 0;
                renderCharts(pageId);
            }

            // Close mobile sidebar if open
            const sidebar = document.querySelector('.dash-sidebar');
            const backdrop = document.querySelector('.dash-sidebar-backdrop');
            if (sidebar) sidebar.classList.remove('sidebar-open');
            if (backdrop) backdrop.classList.remove('visible');
        });
    });

    // Slicer change handlers
    ['dash-slicer-airline', 'dash-slicer-date', 'dash-slicer-channel'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', function() {
                const key = id.replace('dash-slicer-', '');
                DASHBOARD_STATE[key] = this.value;
                renderCharts(document.querySelector('.dash-nav-item.dash-nav-active').getAttribute('data-page'));
                updateKPIs(computeKPIs(), document.querySelector('.dash-nav-item.dash-nav-active').getAttribute('data-page'));
            });
        }
    });

    // Reset filters
    const resetBtn = document.getElementById('dash-btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            DASHBOARD_STATE.airline = 'all';
            DASHBOARD_STATE.dateRange = 'all';
            DASHBOARD_STATE.channel = 'all';
            document.getElementById('dash-slicer-airline').value = 'all';
            document.getElementById('dash-slicer-date').value = 'all';
            document.getElementById('dash-slicer-channel').value = 'all';
            renderCharts(document.querySelector('.dash-nav-item.dash-nav-active').getAttribute('data-page'));
            updateKPIs(computeKPIs(), document.querySelector('.dash-nav-item.dash-nav-active').getAttribute('data-page'));
        });
    }

    // Fullscreen
    const fsBtn = document.getElementById('dash-btn-fullscreen');
    const fsOverlay = document.createElement('div');
    fsOverlay.className = 'dash-fullscreen-overlay';
    fsOverlay.innerHTML = `
        <div class="dash-fs-header">
            <h1 class="dash-fs-title" id="dash-fs-title">AEROVISION 360 Dashboard</h1>
            <button class="dash-fs-close" id="dash-fs-close">✕</button>
        </div>
        <div class="dash-fs-content" id="dash-fs-content"></div>
    `;
    document.body.appendChild(fsOverlay);

    const fsClose = document.getElementById('dash-fs-close');
    fsBtn.addEventListener('click', () => {
        const activePage = document.querySelector('.dash-page.dash-page-active');
        const pageId = activePage ? activePage.id : 'page01';
        document.getElementById('dash-fs-title').textContent = document.getElementById('dash-page-title').textContent;
        fsOverlay.classList.add('dash-fullscreen-active');
        DASHBOARD_STATE.fullscreenActive = true;
        // Lock body scroll while fullscreen is open
        document.body.style.overflow = 'hidden';

        // Clone page content into fullscreen
        const fsContent = document.getElementById('dash-fs-content');
        fsContent.innerHTML = '';
        const clone = activePage.cloneNode(true);
        fsContent.appendChild(clone);

        // Re-render charts in fullscreen (clone keeps original canvas IDs)
        renderChartsForElement(clone, pageId);
    });

    fsClose.addEventListener('click', () => {
        fsOverlay.classList.remove('dash-fullscreen-active');
        DASHBOARD_STATE.fullscreenActive = false;
        // Unlock body scroll
        document.body.style.overflow = '';
        // Destroy fullscreen charts
        Object.keys(DASHBOARD_CONFIG.chartInstances).forEach(k => {
            if (k.startsWith('fs-')) {
                DASHBOARD_CONFIG.chartInstances[k].destroy();
                DASHBOARD_CONFIG.chartInstances[k] = null;
            }
        });
        // Re-render the original page charts
        const activePage = document.querySelector('.dash-page.dash-page-active');
        if (activePage) {
            renderCharts(activePage.id);
        }
    });

    // Click outside to close fullscreen
    fsOverlay.addEventListener('click', (e) => {
        if (e.target === fsOverlay) {
            fsClose.click();
        }
    });
}

/**
 * Render charts into a specific DOM element (for fullscreen)
 */
function renderChartsForElement(element, pageId) {
    // Clone keeps original canvas IDs; _currentRenderRoot directs createChart to the clone
    renderCharts(pageId, element);
}

/**
 * Main render function
 */
function renderDashboard() {
    const kpis = computeKPIs();
    updateKPIs(kpis, 'all');
    renderCharts('page01');
}

/**
 * Initialize dashboard
 */
function initDashboard() {
    // Only initialize if dashboard elements exist
    if (!document.getElementById('powerbi-dashboard')) return;

    loadDashboardData();

    // Window resize handler for charts
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            Object.values(DASHBOARD_CONFIG.chartInstances).forEach(chart => {
                if (chart && typeof chart.resize === 'function') {
                    chart.resize();
                }
            });
        }, 200);
    });
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initMobileMenu,
        initScrollAnimations,
        initSmoothScroll,
        initTypeWriter,
        initAccordions,
        initDashboardZoom,
        initNavbarScroll,
        initPowerBI,
        embedReport,
        initDashboard,
        POWERBI_CONFIG,
        POWERBI_PAGE_MAP
    };
}
