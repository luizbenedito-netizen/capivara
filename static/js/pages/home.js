document.addEventListener("DOMContentLoaded", function() {
    
    window.resetDropdown = (dropdownContainer) => {
        if (!dropdownContainer) return;
        const toggleText = dropdownContainer.querySelector('[data-dropdown-value]');
        const toggleBtn = dropdownContainer.querySelector('.dropdown-toggle');
        if (toggleText && toggleBtn) {
            if (toggleText.dataset.initialHtml !== undefined) {
                toggleText.innerHTML = toggleText.dataset.initialHtml;
            }
            const initialVal = toggleBtn.dataset.initialValue;
            if (initialVal) {
                toggleBtn.dataset.value = initialVal;
            } else {
                toggleBtn.removeAttribute('data-value');
            }
        }
        dropdownContainer.querySelectorAll('.dropdown-option').forEach(opt => {
            opt.classList.remove('active');
        });
    };

    const initDropdowns = () => {
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            const toggleText = dropdown.querySelector('[data-dropdown-value]');
            const toggleBtn = dropdown.querySelector('.dropdown-toggle');
            
            if (toggleText && toggleBtn && !toggleText.dataset.initialHtml) {
                toggleText.dataset.initialHtml = toggleText.innerHTML;
                toggleBtn.dataset.initialValue = toggleBtn.dataset.value || '';
            }
        });
        document.addEventListener('click', function(e) {
            const item = e.target.closest('.dropdown-item');
            if (!item) return;
            const dropdown = item.closest('.dropdown');
            if (!dropdown) return;
            if (item.tagName === 'A') e.preventDefault();
            const toggleText = dropdown.querySelector('[data-dropdown-value]');
            const toggleBtn = dropdown.querySelector('.dropdown-toggle');
            if (toggleText && toggleBtn) {
                toggleText.innerHTML = item.innerHTML; // Altera o conteúdo
                toggleBtn.dataset.value = item.getAttribute('data-value');
            }
            dropdown.querySelectorAll('.dropdown-option')
                .forEach(opt => opt.classList.remove('active'));
            item.closest('.dropdown-option')?.classList.add('active');
        });
    };

    const initYearControls = () => {
        const monthDropdown = document.querySelector('.month-dropdown');
        if (!monthDropdown) return;

        const yearElement = monthDropdown.querySelector(".year-value");
        const btnPrev = monthDropdown.querySelector(".year-btn:first-child");
        const btnNext = monthDropdown.querySelector(".year-btn:last-child");

        const updateYear = (increment) => {
            let currentYear = parseInt(yearElement.textContent);
            yearElement.textContent = currentYear + increment;
        };

        btnPrev.onclick = (e) => {
            e.stopPropagation();
            updateYear(-1);
        };
        btnNext.onclick = (e) => {
            e.stopPropagation();
            updateYear(1);
        };
    };

    const initMonthCache = () => {
        const dropdownMonth = document.querySelector('.month-dropdown');
        if (!dropdownMonth) return;
        let lastMonth = dropdownMonth.querySelector(".month-selector")?.dataset.value;
        let lastYear = dropdownMonth.querySelector(".year-value")?.textContent.trim();
        dropdownMonth.addEventListener('hidden.bs.dropdown', function(event) {
            setTimeout(async () => {
                const selectedToggle = dropdownMonth.querySelector(".month-selector");
                const selectedYear = dropdownMonth.querySelector(".year-value");
                if (!selectedToggle || !selectedYear) return;
                const currentMonth = selectedToggle.dataset.value;
                const currentYear = selectedYear.textContent.trim();
                if (currentMonth === lastMonth && currentYear === lastYear) return;
                lastMonth = currentMonth;
                lastYear = currentYear;
                try {
                    await fetch('/api/context/date/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: new URLSearchParams({
                            month: currentMonth,
                            year: currentYear
                        })
                    });
                } catch (error) {
                    console.error("Erro ao atualizar o cache de sessão:", error);
                }
            }, 0);
        });
    };

    initDropdowns();
    initYearControls();
    initMonthCache();

    const fabContainer = document.getElementById('fabContainer');
    const fabToggle = document.getElementById('toggle');

    if (!fabContainer || !fabToggle) return;

    document.addEventListener('click', function (event) {
        if (!fabContainer.contains(event.target)) {
            fabToggle.checked = false;
        }
    });   
});

const toggleTheme = async () => {
    const btn = document.getElementById('toggleTheme');
    btn.addEventListener('click', async () => {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        await fetch('/api/context/theme/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',

                'X-CSRFToken': getCookie('csrftoken')
            },
            body: new URLSearchParams({
                theme: newTheme
            })
        });
    });
};

toggleTheme();