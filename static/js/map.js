// Ініціалізація карти
const map = L.map('map').setView([49.245, 30.110], 11); // Жашків

// Базові шари
const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
});

const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: '© Esri'
}).addTo(map);

const openTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: '© OpenTopoMap'
});

// Завантаження zhashkivTGLayer із локального файлу
function loadZhashkivTGLayer() {
    console.log("Запуск loadZhashkivTGLayer");
    fetch('/static/geo/Zhash_TG.geojson') // Зміни шлях до файлу, якщо потрібно
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
              if (!data || !data.type || data.type !== "FeatureCollection" || !data.features || data.features.length === 0) {
                showMessage("Дані для шару 'Zhashkiv-TG' не знайдено");
                zhashkivTGLayer.clearLayers();
                return;
            }
            zhashkivTGLayer.clearLayers();
            const newLayer = createLayer(data, function () {
                return {
                    color: '#7FFF00',
                    fillColor: '#ff7800',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0
                };
            }, function (feature, layer) {
                const props = feature.properties;
                let info = `${feature.properties.locality || 'Невідомо'}<br>`;
                if (props.name) info += `<b>Назва:</b> ${props.name}<br>`;
                layer.bindPopup(info);
            });
            zhashkivTGLayer.addLayer(newLayer);
            console.log("Додано новий шар до zhashkivTGLayer:", zhashkivTGLayer);
        })
        .catch(err => {
            console.error("Помилка завантаження zhashkivTGLayer:", err);
            showMessage(`Помилка завантаження шару 'Zhashkiv-TG': ${err.message}`);
            zhashkivTGLayer.clearLayers();
        });
}

// Завантаження zhashkivNPLayer із локального файлу
function loadZhashkivNPLayer() {
    console.log("Запуск loadZhashkivNPLayer");

    // Ініціалізація layerGroup для підписів
    if (!window.labelLayerGroup) {
        window.labelLayerGroup = L.layerGroup().addTo(map);
    }
    const labelLayerGroup = window.labelLayerGroup;

    // Очищаємо шар підписів перед завантаженням
    labelLayerGroup.clearLayers();

    fetch('/static/geo/Zhashkiv_NP.geojson')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
            if (!data || !data.type || data.type !== "FeatureCollection" || !data.features || data.features.length === 0) {
                showMessage("Дані для шару 'Zhashkiv-NP' не знайдено");
                zhashkivNPLayer.clearLayers();
                labelLayerGroup.clearLayers();
                return;
            }

            zhashkivNPLayer.clearLayers();

            const newLayer = createLayer(data, function () {
                return {
                    color: '#EEDC82',
                    fillColor: '#ff7800',
                    weight: 3,
                    opacity: 1,
                    fillOpacity: 0
                };
            }, function (feature, layer) {
                const props = feature.properties;
                let info = `${props.locality || 'Невідомо'}<br>`;
                if (props.name) info += `<b>Назва:</b> ${props.name}<br>`;
                layer.bindPopup(info);

                // Додаємо підпис для кожного контуру
                if (props.locality) {
                    let centroid;
                    if (typeof turf !== 'undefined') {
                        // Використовуємо turf.js, якщо доступно
                        centroid = turf.centroid(feature).geometry.coordinates;
                        centroid = [centroid[1], centroid[0]]; // [lat, lng]
                    } else {
                        // Альтернатива: використовуємо центр меж контуру
                        centroid = layer.getBounds().getCenter();
                        centroid = [centroid.lat, centroid.lng];
                    }

                    const label = L.marker(centroid, {
                        icon: L.divIcon({
                            className: 'custom-label',
                            html: `<div>${props.locality}</div>`,
                            iconSize: [100, 20],
                            iconAnchor: [50, 10]
                        }),
                        interactive: false
                    });
                    labelLayerGroup.addLayer(label);
                }
            });

            zhashkivNPLayer.addLayer(newLayer);
            console.log("Додано новий шар до zhashkivNPLayer:", zhashkivNPLayer);

            // Функція для керування видимістю підписів залежно від масштабу
            function updateLabels() {
                const zoom = map.getZoom();
                if (zoom <= 13) {
                    map.addLayer(labelLayerGroup);
                } else {
                    map.removeLayer(labelLayerGroup);
                }
            }

            // Викликаємо при завантаженні шару
            updateLabels();

            // Оновлюємо підписи при зміні масштабу, уникаючи дублювання обробників
            map.off('zoomend', updateLabels); // Видаляємо попередній обробник
            map.on('zoomend', updateLabels);
        })
        .catch(err => {
            console.error("Помилка завантаження zhashkivNPLayer:", err);
            showMessage(`Помилка завантаження шару 'Zhashkiv-NP': ${err.message}`);
            zhashkivNPLayer.clearLayers();
            if (labelLayerGroup) {
                labelLayerGroup.clearLayers();
            }
        });
}

// Накладні шари
let geoLayer = L.markerClusterGroup().addTo(map); // Ділянки активні за замовчуванням
let statusLayer = L.layerGroup();
let categoryLayer = L.layerGroup();
let zhashkivTGLayer = L.layerGroup().addTo(map); // Zhashkiv-TG активний за замовчуванням
let zhashkivNPLayer = L.layerGroup().addTo(map); // Zhashkiv-NP активний за замовчуванням
let searchLayer = L.geoJSON(null, {
    style: { color: 'red', fillColor: 'red', weight: 4, fillOpacity: 0.7 }
}).addTo(map); // searchLayer завжди активний

// Колір для статусів
const statusColors = {
    '1': '#ff0000', // Вільна червоний
    '2': '#FBEC5D', // Оренда жовтий
    '3': '#00CED1', // Постійне користування голубий
    '4': '#7FFF00', // Власність світло-зелений
    '5': '#C71585'  // Аукціон
};

// Колір для категорій
const categoryColors = {
    'A': '#FBEC5D', // 100 Землі сільськогосподарського призначення жовтий
    'B': '#00FFFF', // 200 Землі житлової та громадської забудови голубий
    'C': '#8B008B', // 300 Землі природно-заповідного призначення фіолетовий
    'D': '#C41E3A', // 400 Землі оздоровчого призначення червоний
    'E': '#7FFF00', // 500 Землі рекреаційного призначення світло-зелений
    'F': '#FF55A3', // 600 Землі історико-культурного призначення розовий
    'G': '#228b22', // 700 Землі лісогосподарського призначення зелений
    'H': '#1e90ff', // 800 Землі водного фонду синій
    'I': '#FF8C00'  // 900 Землі промисловості та іншого призначення оранжевий
};

const statusLabels = {
    '1': 'Вільна',
    '2': 'Оренда',
    '3': 'Постійне користування',
    '4': 'Власність',
    '5': 'Аукціон'
};

const categoryLabels = {
    'A': 'Землі с/г призначення',
    'B': 'Землі житлової та громадської забудови',
    'C': 'Землі природно-заповідного призначення',
    'D': 'Землі оздоровчого призначення',
    'E': 'Землі рекреаційного призначення',
    'F': 'Землі історико-культурного призначення',
    'G': 'Землі лісогосподарського призначення',
    'H': 'Землі водного фонду',
    'I': 'Землі промисловості'
};


// Функція для створення шару
function createLayer(data, style, onEachFeature) {
    const validGeoJSON = {
        type: "FeatureCollection",
        features: data.features || []
    };
    console.log("createLayer GeoJSON:", validGeoJSON);
    try {
        const layer = L.geoJSON(validGeoJSON, {
            style,
            onEachFeature
        });
        console.log("createLayer створив шар:", layer);
        return layer;
    } catch (e) {
        console.error("Помилка створення шару:", e);
        return L.layerGroup();
    }
}

// Дебаунсинг
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Легенда
const legendControl = L.control({ position: 'bottomright' });
legendControl.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'info legend');
    div.style.backgroundColor = 'white';
    div.style.padding = '10px';
    div.style.border = '1px solid #ccc';
    div.innerHTML = '<h4>Легенда</h4>';
    return div;
};
legendControl.addTo(map);

function updateLegend() {
    const legendDiv = document.querySelector('.legend');
    let content = '<h4>Легенда</h4>';
    if (map.hasLayer(statusLayer)) {
        content += '<h5>Вид використання</h5>';
        Object.keys(statusColors).forEach(key => {
            content += `<i style="background:${statusColors[key]};width:18px;height:18px;display:inline-block;margin-right:5px;"></i> ${
                key === '1' ? 'Вільна' :
                key === '2' ? 'Оренда' :
                key === '3' ? 'Постійне користування' :
                key === '4' ? 'Власність' :
                'Аукціон'
            }<br>`;
        });
    }
    if (map.hasLayer(categoryLayer)) {
        content += '<h5>Категорія</h5>';
        Object.keys(categoryColors).forEach(key => {
            content += `<i style="background:${categoryColors[key]};width:18px;height:18px;display:inline-block;margin-right:5px;"></i> ${
                key === 'A' ? 'Землі с/г призначення' :
                key === 'B' ? 'Землі житлової забудови' :
                key === 'C' ? 'Землі природо-заповідного фонду' :
                key === 'D' ? 'Землі оздоровчого призначення' :
                key === 'E' ? 'Землі рекреаційного призначення' :
                key === 'F' ? 'Землі історико-культурного призначення' :
                key === 'G' ? 'Землі лісогосподарського призначення' :
                key === 'H' ? 'Землі водного фонду' :
                'Землі промисловості'
            }<br>`;
        });
    }
    if (!map.hasLayer(statusLayer) && !map.hasLayer(categoryLayer)) {
        content = '<h4>Легенда</h4><p>Виберіть шар для відображення легенди</p>';
    }
    legendDiv.innerHTML = content;
}

const loadParcelsWithClusters = debounce(function () {
    if (map.getZoom() < 14 || !map.hasLayer(geoLayer)) return;
    const bounds = map.getBounds();
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;
    const areaMin = parseFloat(document.getElementById('areaMin').value) || 0;
    const areaMax = parseFloat(document.getElementById('areaMax').value) || Infinity;
    const status = document.getElementById('statusFilter').value || '';
    const category = document.getElementById('categoryFilter').value || '';


    // Формуємо URL: якщо є status або category, ігноруємо bbox
    let url = '/landplots/geojson/';
    const params = [];
    if (status) params.push(`status=${encodeURIComponent(status)}`);
    if (category) params.push(`category=${encodeURIComponent(category)}`);
    if (params.length > 0) {
        url += `?${params.join('&')}`;
    } else {
        const bbox = map.getBounds().toBBoxString();
        url += `?bbox=${bbox}`;
    }

    console.log("URL запиту:", url); // Дебагінг

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log("Отримані дані:", data); // Дебагінг
            if (!data || !data.type || data.type !== "FeatureCollection" || !data.features || data.features.length === 0) {
                showMessage("Ділянки не знайдено");
                return;
            }
            geoLayer.clearLayers();
            const filteredData = {
                type: "FeatureCollection",
                features: data.features.filter(feature => {
                    const area = feature.properties.area || 0;
                    return area >= areaMin && area <= areaMax;
                })
            };
            console.log("Відфільтровані дані:", filteredData); // Дебагінг
            const geoJsonLayer = L.geoJSON(filteredData, {
                style: function (feature) {
                    return {
                        fillColor:'#1E90FF',
                        fillOpacity: 0.3,
                        color: '#1E90FF',
                        weight: 2
                    };
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(`
                        <b>Кадастровий номер:</b> ${feature.properties.cadastr_number || 'Невідомо'}<br>
                        <b>Площа:</b> ${feature.properties.area != null ? feature.properties.area + ' га' : 'Невідомо'}<br>
                        <b>Адреса:</b> ${feature.properties.location || 'Невідомо'}<br>
                        <b>Категорія:</b> ${categoryLabels[feature.properties.category] || 'Невідомо'}<br>
                        <b>Цільове призначення:</b> ${feature.properties.destination || 'Невідомо'}<br>
                        <b>Користувач:</b> ${feature.properties.owner_name || 'Невідомо'}<br>
                        <b>Користування:</b> ${statusLabels[feature.properties.status] || 'Невідомо'}<br>
                    `);
                }
            });
            geoLayer.addLayer(geoJsonLayer);
            if (filteredData.features.length === 0) {
                showMessage("Ділянок у вказаному діапазоні площі не знайдено");
            } else {
                showMessage("Ділянки успішно завантажено", "success");
            }
        })
        .catch(err => {
            console.error("Помилка завантаження geoLayer:", err);
            showMessage(`Помилка завантаження ділянок: ${err.message}`, "error");
        });
}, 500);

document.getElementById('categoryFilterBtn').addEventListener('click', () => {
    const areaMin = parseFloat(document.getElementById('areaMin').value) || 0;
    const areaMax = parseFloat(document.getElementById('areaMax').value) || Infinity;
    if (areaMax < areaMin) {
        showMessage("Максимальна площа не може бути меншою за мінімальну", "error");
        return;
    }
    loadParcelsWithClusters();
    const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
    if (modal) modal.hide();
});

document.getElementById('statusFilterBtn').addEventListener('click', () => {
    const areaMin = parseFloat(document.getElementById('areaMin').value) || 0;
    const areaMax = parseFloat(document.getElementById('areaMax').value) || Infinity;
    if (areaMax < areaMin) {
        showMessage("Максимальна площа не може бути меншою за мінімальну", "error");
        return;
    }
    loadParcelsWithClusters();
    const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
    if (modal) modal.hide();
});

document.getElementById('filterAreaBtn').addEventListener('click', () => {
    const areaMin = parseFloat(document.getElementById('areaMin').value) || 0;
    const areaMax = parseFloat(document.getElementById('areaMax').value) || Infinity;
    if (areaMax < areaMin) {
        showMessage("Максимальна площа не може бути меншою за мінімальну", "error");
        return;
    }
    loadParcelsWithClusters();
    const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
    if (modal) modal.hide();
});

document.getElementById('resetBtn').addEventListener('click', () => {
    searchLayer.clearLayers();
    document.getElementById('areaMin').value = '';
    document.getElementById('areaMax').value = '';
    document.getElementById('searchInput').value = '';
    document.getElementById('searchUserInput').value = '';
    document.getElementById('statusFilter').value = '';
    document.getElementById('categoryFilter').value = '';
    loadParcelsWithClusters();
    showMessage("Фільтр скинуто", "success");
});


// Завантаження statusLayer
const loadStatusLayer = debounce(function () {
    console.log("Запуск loadStatusLayer, statusLayer:", statusLayer);
    if (map.getZoom() < 14 || !statusLayer || !map.hasLayer(statusLayer)) {
        console.log("statusLayer не активний, зум < 14 або statusLayer null");
        return;
    }
    const bounds = map.getBounds();
    const status = document.getElementById('statusFilter').value || '';
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;
    console.log("Завантаження statusLayer з bbox:", bbox);
    fetch(`/api/status_layer/?bbox=${bbox}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
            console.log("statusLayer response:", data);
            if (!data || !data.type || data.type !== "FeatureCollection" || !data.features || data.features.length === 0) {
                showMessage("Дані для шару 'Вид використання' не знайдено");
                statusLayer.clearLayers();
                updateLegend();
                return;
            }
            statusLayer.clearLayers();
            const newLayer = createLayer(data, function (feature) {
                return {
                    color: '#00008B',
                    fillColor: statusColors[feature.properties.status] || '#cccccc',
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.6
                };
            }, function (feature, layer) {
                const props = feature.properties;
                let info = `<b>Кадастровий номер:</b> ${props.cadastr_number || 'Невідомо'}<br>`;
                if (props.status_display) info += `<b>Статус:</b> ${props.status_display}<br>`;
                if (props.area != null) info += `<b>Площа:</b> ${props.area} га<br>`;
                if (props.location) info += `<b>Адреса:</b> ${props.location}<br>`;
                if (props.destination) info += `<b>Цільове призначення:</b> ${props.destination}<br>`;
                if (props.owner_name) info += `<b>Користувач:</b> ${props.owner_name}<br>`;
                if (props.category_display) info += `<b>Категорія:</b> ${props.category_display}<br>`;
                layer.bindPopup(info);
            });
            statusLayer.addLayer(newLayer);
            console.log("Додано новий шар до statusLayer:", statusLayer);
            updateLegend();
        })
        .catch(err => {
            console.error("Помилка завантаження statusLayer:", err);
            showMessage(`Помилка завантаження шару 'Вид використання': ${err.message}`);
            statusLayer.clearLayers();
            updateLegend();
        });
}, 500);

// Завантаження categoryLayer
const loadCategoryLayer = debounce(function () {
    document.getElementById('spinner').style.display = 'block';
    console.log("Запуск loadCategoryLayer, categoryLayer:", categoryLayer);
    if (map.getZoom() < 14 || !categoryLayer || !map.hasLayer(categoryLayer)) {
        console.log("categoryLayer не активний, зум < 14 або categoryLayer null");
        return;
    }
    const bounds = map.getBounds();
    const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;
    console.log("Завантаження categoryLayer з bbox:", bbox);
    fetch(`/api/category_layer/?bbox=${bbox}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
            document.getElementById('spinner').style.display = 'none'; // Сховати спінер
            console.log("categoryLayer response:", data);
            if (!data || !data.type || data.type !== "FeatureCollection" || !data.features || data.features.length === 0) {
                showMessage("Дані для шару 'Категорія' не знайдено");
                categoryLayer.clearLayers();
                updateLegend();
                return;
            }
            categoryLayer.clearLayers();
            const newLayer = createLayer(data, function (feature) {
                return {
                    color: '#00008B',
                    fillColor: categoryColors[feature.properties.category] || '#cccccc',
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.6 // Зменшено прозорість для categoryLayer
                };
            }, function (feature, layer) {
                const props = feature.properties;
                let info = `<b>Кадастровий номер:</b> ${props.cadastr_number || 'Невідомо'}<br>`;
                if (props.category_display) info += `<b>Категорія:</b> ${props.category_display}<br>`;
                if (props.area != null) info += `<b>Площа:</b> ${props.area} га<br>`;
                if (props.location) info += `<b>Адреса:</b> ${props.location}<br>`;
                if (props.destination) info += `<b>Цільове призначення:</b> ${props.destination}<br>`;
                if (props.owner_name) info += `<b>Користувач:</b> ${props.owner_name}<br>`;
                if (props.status_display) info += `<b>Статус:</b> ${props.status_display}<br>`;
                layer.bindPopup(info);
            });
            categoryLayer.addLayer(newLayer);
            console.log("Додано новий шар до categoryLayer:", categoryLayer);
            updateLegend();
        })
        .catch(err => {
            document.getElementById('spinner').style.display = 'none'; // Сховати спінер
            console.error("Помилка завантаження categoryLayer:", err);
            showMessage(`Помилка завантаження шару 'Категорія': ${err.message}`);
            categoryLayer.clearLayers();
            updateLegend();
        });
}, 500);



// Події карти
map.on('moveend zoomend', function () {
    loadParcelsWithClusters();
    loadStatusLayer();
    loadCategoryLayer();
    loadZhashkivTGLayer();
    loadZhashkivNPLayer();
});
map.on('overlayadd', function (e) {
    console.log("Додано шар:", e.name);
    if (e.name === 'Ділянки') loadParcelsWithClusters();
    if (e.name === 'Вид використання') loadStatusLayer();
    if (e.name === 'Категорія') loadCategoryLayer();
    updateLegend();
});
map.on('overlayremove', function (e) {
    console.log("Видалено шар:", e.name);
    if (e.name === 'Ділянки') {
        geoLayer.clearLayers();
    }
    if (e.name === 'Вид використання') {
        statusLayer.clearLayers();
        console.log("statusLayer очищено");
    }
    if (e.name === 'Категорія') {
        categoryLayer.clearLayers();
        console.log("categoryLayer очищено");
    }
    updateLegend();
});

// Контроль шарів із радіокнопками
const baseMaps = {
    "OpenStreetMap": osmLayer,
    "Esri Satellite": esriSatellite,
    "OpenTopoMap": openTopoMap
};
const overlayMaps = {
    "Ділянки": geoLayer,
    "Вид використання": statusLayer,
    "Категорія": categoryLayer,
    // searchLayer не додаємо, бо він завжди активний
};
L.control.layers(baseMaps, overlayMaps, { collapsed: false }).addTo(map);
// Робимо накладні шари радіокнопками
const layerControl = document.querySelector('.leaflet-control-layers');
layerControl.querySelectorAll('.leaflet-control-layers-overlays input[type=checkbox]').forEach(input => {
    input.type = 'radio';
    input.name = 'overlay';
});

// Початкове завантаження
loadParcelsWithClusters();

// Пошук за кадастровим номером
document.getElementById('searchBtn').addEventListener('click', () => {
    const val = document.getElementById('searchInput').value.trim();
    if (!val) return showMessage("Введіть кадастровий номер");
    if (!/^[0-9]{10}:[0-9]{2}:[0-9]{3}:[0-9]{4}$/.test(val)) {
        return showMessage("Некоректний кадастровий номер. Формат: 0000000000:00:000:0000");
    }
    searchLayer.clearLayers();
    fetch(`/api/search_landplot/?cadastr=${encodeURIComponent(val)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP error ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("API response:", data);
            if (data.error || !data.geometry || !data.properties) {
                showMessage(data.error || "Ділянка за цим кадастровим номером не знайдена");
                return;
            }
            const feature = {
                type: "Feature",
                properties: data.properties,
                geometry: data.geometry
            };
            const foundLayer = L.geoJSON(feature, {
                style: { color: 'red', fillColor: 'red', weight: 4, fillOpacity: 0.7 }
            }).addTo(searchLayer);
            map.fitBounds(foundLayer.getBounds());
            foundLayer.bindPopup(`
                <b>Кадастровий номер:</b> ${data.properties.cadastr_number || 'Невідомо'}<br>
                <b>Площа:</b> ${data.properties.area != null ? data.properties.area + ' га' : 'Невідомо'}<br>
                <b>Адреса:</b> ${data.properties.location || 'Невідомо'}<br>
                <b>Цільове призначення:</b> ${data.properties.destination || 'Невідомо'}<br>
                <b>Користувач:</b> ${data.properties.owner_name || 'Невідомо'}<br>
                <b>Статус:</b> ${data.properties.status_display || 'Невідомо'}<br>
                <b>Категорія:</b> ${data.properties.category_display || 'Невідомо'}
            `).openPopup();
            const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
            if (modal) modal.hide();
        })
        .catch(err => {
            console.error("Помилка пошуку ділянки:", err);
            showMessage(`Помилка пошуку ділянки: ${err.message}`);
        });
});

// Пошук за користувачем
document.getElementById('searchUserBtn').addEventListener('click', () => {
    const userVal = document.getElementById('searchUserInput').value.trim();
    if (!userVal) return showMessage("Введіть ім'я або прізвище користувача");
    if (!/^[a-zA-Zа-яґєіїїА-ЯҐЄІЇ\s\-]+$/.test(userVal)) {
        return showMessage("Некоректне ім'я. Дозволені літери, пробіли і дефіс.");
    }
    searchLayer.clearLayers();
    fetch(`/api/search_landplot/?user=${encodeURIComponent(userVal)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP error ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.error || !data.features || data.features.length === 0) {
                showMessage(data.error || "Ділянки за цим користувачем не знайдені");
                return;
            }
            const boundsArray = [];
            data.features.forEach(feature => {
                const parcel = {
                    type: "Feature",
                    geometry: feature.geometry,
                    properties: feature.properties
                };
                const layer = L.geoJSON(parcel, {
                    style: { color: '#66FF00', fillColor: '#66FF00', weight: 3, fillOpacity: 0.7 }
                }).addTo(searchLayer);
                layer.bindPopup(`
                    <b>Кадастровий номер:</b> ${feature.properties.cadastr_number || 'Невідомо'}<br>
                    <b>Площа:</b> ${feature.properties.area != null ? feature.properties.area + ' га' : 'Невідомо'}<br>
                    <b>Адреса:</b> ${feature.properties.location || 'Невідомо'}<br>
                    <b>Цільове призначення:</b> ${feature.properties.destination || 'Невідомо'}<br>
                    <b>Користувач:</b> ${feature.properties.owner_name || 'Невідомо'}<br>
                    <b>Статус:</b> ${feature.properties.status_display || 'Невідомо'}<br>
                    <b>Категорія:</b> ${feature.properties.category_display || 'Невідомо'}
                `);
                 const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
                if (modal) modal.hide();
                try {
                    boundsArray.push(layer.getBounds());
                } catch (e) {
                    console.warn("Не вдалося визначити межі шару:", e);
                }
            });
            if (boundsArray.length > 0) {
                const allBounds = boundsArray.reduce((acc, b) => acc.extend(b), boundsArray[0]);
                map.fitBounds(allBounds);
            }

        })
        .catch(err => {
            console.error("Помилка пошуку ділянок за користувачем:", err);
            showMessage(`Помилка пошуку ділянок: ${err.message}`);
        });
});

function showMessage(message, type = 'info') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `map-message ${type}`;
    msgDiv.textContent = message;
    document.getElementById('map').appendChild(msgDiv);
    setTimeout(() => msgDiv.remove(), 3000);
}

document.getElementById('filterAreaBtn').addEventListener('click', () => {
    const areaMin = parseFloat(document.getElementById('areaMin').value) || 0;
    const areaMax = parseFloat(document.getElementById('areaMax').value) || Infinity;
    if (areaMax < areaMin) {
        showMessage("Максимальна площа не може бути меншою за мінімальну");
        return;
    }
    loadParcelsWithClusters();
    const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal'));
    if (modal) modal.hide();
});

// Кастомний контрол для кнопки "Фільтри"
L.Control.FilterButton = L.Control.extend({
    options: {
        position: 'topleft' // Розташування кнопки (можна змінити на 'topright', 'bottomleft', 'bottomright')
    },
    onAdd: function (map) {
        const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        const button = L.DomUtil.create('button', 'btn btn-primary filter-btn', container);
        button.innerHTML = '<i class="bi bi-funnel"></i>'; // Іконка воронки
        button.setAttribute('type', 'button');
        button.setAttribute('data-bs-toggle', 'modal');
        button.setAttribute('data-bs-target', '#filterModal');
        button.title = 'Відкрити фільтри';
        L.DomEvent.on(button, 'click', () => {
            const modal = bootstrap.Modal.getInstance(document.getElementById('filterModal')) || new bootstrap.Modal(document.getElementById('filterModal'));
            modal.show();
        });
        return container;
    }
});

// Додаємо контрол на карту
new L.Control.FilterButton().addTo(map);