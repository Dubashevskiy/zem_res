console.log("jQuery версія:", typeof $ !== "undefined" ? $.fn.jquery : "не знайдено");

// Автозаповнення місцерозташування
$(function() {
  if ($("#id_location").length) {
    $("#id_location").autocomplete({
      source: function(request, response) {
        $.ajax({
          url: "/location_autocomplete/",  // або {% url 'location_autocomplete' %} якщо в шаблоні
          data: {
            term: request.term
          },
          success: function(data) {
            response([...new Set(data)]);
          }
        });
      },
      minLength: 2
    });
  }
});

//Автозаповнення кадастрового номера

$(function() {
  $("#id_cadastr_number").autocomplete({
    source: function(request, response) {
      $.ajax({
        url: "/cadastr_autocomplete/",
        data: {
          term: request.term
        },
        success: function(data) {
          // Фільтруємо дублікати за допомогою Set
          var uniqueData = [...new Set(data)];
          response(uniqueData);
        }
      });
    },
    minLength: 2
  });
});

$(function() {
  $("#id_owner_name").autocomplete({
    source: function(request, response) {
      $.ajax({
        url: "/owner_autocomplete/",
        data: {
          term: request.term
        },
        success: function(data) {
          var uniqueData = [...new Set(data)];
          response(uniqueData);  // Відправляємо дані без додаткової фільтрації
        }
      });
    },
    minLength: 2
  });
});

// додаткова форма додавання інформації про користувача та паспорт водного обєкта
document.addEventListener("DOMContentLoaded", function () {
  const statusField = document.getElementById("id_status");
  const hasPassportField = document.getElementById("id_has_passport");
  const subOrendaField = document.getElementById("id_suborendar");
  const userInfo = document.getElementById("user_info");
  const subOrenda = document.getElementById("suborendar");
  const waterPassport = document.getElementById("water_passport");
  const hydroStructure = document.getElementById("hydro_structure");

  function toggleBlocks() {
    if (!userInfo || !waterPassport || !subOrenda || !hydroStructure) return; // Захист

    userInfo.style.display = "none";
    waterPassport.style.display = "none";
    hydroStructure.style.display = "none";
    subOrenda.style.display = "none";

    if (statusField && ["2", "3", "4", "6"].includes(statusField.value)) {
      userInfo.style.display = "block";
    }

// Показуємо suborenda для suborendar = "1"
    if (subOrendaField && ["1"].includes(subOrendaField.value)) {
      subOrenda.style.display = "block";
    }


    if (hasPassportField && hasPassportField.checked) {
      waterPassport.style.display = "block";
      hydroStructure.style.display = "block";
    }
  }
  toggleBlocks();

  if (statusField) statusField.addEventListener("change", toggleBlocks);
  if (hasPassportField) hasPassportField.addEventListener("change", toggleBlocks);
  if (subOrendaField) subOrendaField.addEventListener("change", toggleBlocks);
});

// Функція сортування
/*
function sortTable(n) {
    var table = document.getElementById("searchTable");  // Тепер правильний ID
    var rows = table.rows;
    var switching = true;
    var dir = "asc"; // Початковий напрямок сортування

    while (switching) {
        switching = false;
        var shouldSwitch = false;
        for (var i = 1; i < (rows.length - 1); i++) {
            var x = rows[i].getElementsByTagName("TD")[n];
            var y = rows[i + 1].getElementsByTagName("TD")[n];

            // Отримуємо значення для порівняння
            var xContent = x.innerHTML.trim();
            var yContent = y.innerHTML.trim();

            // Перевірка на числа або дати
            var xIsNumber = !isNaN(xContent) && xContent !== "";
            var yIsNumber = !isNaN(yContent) && yContent !== "";

            var xIsDate = Date.parse(xContent);
            var yIsDate = Date.parse(yContent);

            if (xIsDate && yIsDate) {
                // Якщо обидва значення є датами
                xContent = Date.parse(xContent);
                yContent = Date.parse(yContent);
            } else if (xIsNumber && yIsNumber) {
                // Якщо обидва значення є числами
                xContent = parseFloat(xContent);
                yContent = parseFloat(yContent);
            }

            // Сортуємо за текстом, числом чи датою
            if (dir === "asc" && xContent > yContent) {
                shouldSwitch = true;
                break;
            } else if (dir === "desc" && xContent < yContent) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            dir = (dir === "asc") ? "desc" : "asc";
        }
    }
}
*/

// Функція пошуку
function searchTable() {
    var input = document.getElementById("searchInput");
    var filter = input.value.toUpperCase();
    var table = document.getElementById("searchTable");
    var tr = table.getElementsByTagName("tr");

    for (var i = 0; i < tr.length; i++) {
      var td = tr[i].getElementsByTagName("td")[1];  // пошук по другій колонці (Кадастровий номер)
      if (td) {
        var txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }


// Автоматичне приховування повідомлень
/*
setTimeout(() => {
  const messages = document.querySelectorAll('.alert');
  messages.forEach((msg) => {
    msg.style.transition = "opacity 0.5s ease-out";
    msg.style.opacity = 0;
    setTimeout(() => msg.remove(), 500);
  });
}, 4000); // 4 секунди
*/

//Приховування колонок паспорту водних обєктів
function showDetails(number, name, area, volume, depth, approval, developer, row) {
    document.getElementById('passNumber').textContent = number;
    document.getElementById('passName').textContent = name;
    document.getElementById('passArea').textContent = area;
    document.getElementById('passVolume').textContent = volume;
    document.getElementById('passDepth').textContent = depth;
    document.getElementById('passApproval').textContent = approval;
    document.getElementById('passDeveloper').textContent = developer;
    document.getElementById('sidePanel').style.display = 'block';

    // Підсвічування вибраного рядка
    document.querySelectorAll('tr').forEach(tr => tr.classList.remove('highlight-row'));
    row.classList.add('highlight-row');
 }

 //Приховування колонок суборенди
 function subshowDetails(suborendar, subrentstart, subrentend,  row) {
    document.getElementById('subOwner').textContent = suborendar;
    document.getElementById('subRentStart').textContent = subrentstart;
    document.getElementById('subRentEnd').textContent = subrentend;
    document.getElementById('subsidePanel').style.display = 'block';
        // Підсвічування вибраного рядка
    document.querySelectorAll('tr').forEach(tr => tr.classList.remove('highlight-row'));
    row.classList.add('highlight-row');
 }
 //Приховування колонок примітка
 function notesshowDetails(notes, row) {
    document.getElementById('notes').textContent = notes;
    document.getElementById('notessidePanel').style.display = 'block';
        // Підсвічування вибраного рядка
    document.querySelectorAll('tr').forEach(tr => tr.classList.remove('highlight-row'));
    row.classList.add('highlight-row');
 }

function hidePanel() {
    document.getElementById('subsidePanel').style.display = 'none';
    document.getElementById('sidePanel').style.display = 'none';
    document.getElementById('notessidePanel').style.display = 'none';
    document.querySelectorAll('tr').forEach(tr => tr.classList.remove('highlight-row'));
}
// фільтрація Ajax
    function updateResultsWater(url) {
        $.ajax({
            url: url || "{% url 'zem_lease_result' %}",
            data: $("#filter-form").serialize(),
            success: function(data) {
                $("#results").html(data);
            }
        });
    }

    $("#filter-form").on("change", "input, select", function() {
        updateResults();
    });

    // підтримка пагінації
    $("#results").on("click", ".pagination a", function(e) {
        e.preventDefault();
        updateResults($(this).attr("href"));
    });



// перехід на сторінку редагування за подвійним кліком
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".clickable-table tr[data-id]").forEach(function (row) {
        row.addEventListener("dblclick", function () {
            const id = this.dataset.id;
            const prefix = this.dataset.urlPrefix || this.closest("table").dataset.urlPrefix;
            const params = window.location.search.slice(1); // без '?'

            if (id && prefix) {
                window.location.href = `/${prefix}/edit/${id}/${params ? '?' + params : ''}`;
            } else {
                console.warn("Не вказано id або prefix");
            }
        });
    });
});

const filterForm = document.getElementById('filter-form');
if (filterForm) {
  filterForm.addEventListener('submit', function(event) {
    const areaFrom = document.getElementById('id_area_from');
    const areaTo = document.getElementById('id_area_to');
    const errorDiv = document.getElementById('filter-error');

    let hasError = false;
    let errorMessage = "";

    if (areaFrom && areaFrom.value && isNaN(areaFrom.value)) {
        hasError = true;
        errorMessage += "Поле 'Площа від' має бути числом. ";
    }
    if (areaTo && areaTo.value && isNaN(areaTo.value)) {
        hasError = true;
        errorMessage += "Поле 'Площа до' має бути числом. ";
    }

    if (hasError) {
        event.preventDefault();
        if (errorDiv) {
          errorDiv.classList.remove('d-none');
          errorDiv.innerText = errorMessage;
        } else {
          alert(errorMessage);
        }
    }
  });
}

const myFilterForm = document.getElementById('filter-form');
if (myFilterForm) {
  myFilterForm.addEventListener('submit', function(event) {
        const areaFrom = document.getElementById('id_area_from');
        const areaTo = document.getElementById('id_area_to');
        const errorDiv = document.getElementById('filter-error');

        let hasError = false;
        let errorMessage = "";

        if (areaFrom && areaFrom.value && isNaN(areaFrom.value)) {
            hasError = true;
            errorMessage += "Поле 'Площа від' має бути числом. ";
        }
        if (areaTo && areaTo.value && isNaN(areaTo.value)) {
            hasError = true;
            errorMessage += "Поле 'Площа до' має бути числом. ";
        }

        if (hasError) {
            event.preventDefault();
            if (errorDiv) {
              errorDiv.classList.remove('d-none');
              errorDiv.innerText = errorMessage;
            } else {
              alert(errorMessage);
            }
        }
    });
}
// Покращена фільтрація
;

window.updateResults = function(url) {
    $.ajax({
        url: url || filterResultUrl,  // використовуємо передану з шаблону змінну
        data: $("#filter-form").serialize(),
        success: function(data) {
            $("#results").html(data);
        }
    });
};

$(document).ready(function() {
    $("#filter-form").on("change", "input, select", function() {
        updateResults();
    });

    // підтримка пагінації
    $("#results").on("click", ".pagination a", function(e) {
        e.preventDefault();
        updateResults($(this).attr("href"));
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".clickable-table tr[data-id]").forEach(function (row) {
        row.addEventListener("dblclick", function () {
            const id = this.dataset.id;
            const prefix = this.dataset.urlPrefix || this.closest("table").dataset.urlPrefix;
            const params = new URLSearchParams(window.location.search); // без '?'
            const next = encodeURIComponent(window.location.href);
            params.set('next', window.location.pathname + window.location.search);

            if (id && prefix) {
                let url = `/${prefix}/edit/${id}/`;
                const fullParams = [];

                if (params) fullParams.push(params);
                fullParams.push(`next=${next}`);

                url += `?${fullParams.join('&')}`;

                window.location.href = `/${prefix}/edit/${id}/?${params.toString()}`;;
            } else {
                console.warn("Не вказано id або prefix");
            }
        });
    });
});