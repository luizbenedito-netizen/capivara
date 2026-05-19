let modal = {}

const ModalDefaultSettings = {
    title: 'Modal',
    position: 'top',
    showCloseButton: true,
    showConfirmButton: false,
    html: "",
    footer: "",
    customClass: {
        popup: 'home-modal'
    }
}

const initModal = ({name}) => {
    if (!modal[name]) {
        const modalElem = document.getElementById(name);
        if (!modalElem) return;
        modal[name] = {
            title: modalElem.querySelector('.modal-title') || '',
            body: modalElem.querySelector('.modal-body-custom') || '',
            footer: modalElem.querySelector('.modal-footer-custom') || '',
            beforeDefault: () => null,
            afterDefault: () => null
        };
    }
}

window.propsModal = (name) => {
    if (!modal[name]) initModal({name});
    return modal[name] || {};
}

const closeDropdown = (context) => {
    const dropdown = context.querySelector('.dropdown');
    if (!dropdown) return;
    const toggle = dropdown.querySelector('.dropdown-toggle');
    toggle.classList.remove('show');
    toggle.setAttribute('aria-expanded', 'false');
    const menu = dropdown.querySelector('.dropdown-menu');
    if (menu) menu.classList.remove('show');
}

window.showModal = async ({name = null, before = (args) => null, after = (args) => null}) => {

    initModal({name});

    if (!modal[name]) return;
    const cache = modal[name];

    const checkbox = document.getElementById("toggle");
    checkbox.checked = false;

    Swal.fire({
        ...ModalDefaultSettings,
        title: cache.title,
        html: cache.body,
        footer: cache.footer,
        willOpen: () => {
            before(modal[name]);
            modal[name].beforeDefault();
            closeDropdown(modal[name].body);
        },
        didOpen: () => {
            after(modal[name]);
            modal[name].afterDefault();
        },
        willClose: () => null,
        didClose: () => null
    });
};

document.addEventListener('shown.bs.dropdown', function(event) {
    const dropdown = event.target;
    const menu = dropdown.nextElementSibling;
    const swalPopup = dropdown.closest('.swal2-popup');
    if (swalPopup && menu) {
        const buttonRect = dropdown.getBoundingClientRect();
        const swalRect = swalPopup.getBoundingClientRect();
        const availableHeight = swalRect.bottom - buttonRect.bottom - 15;
        menu.style.maxHeight = `${availableHeight}px`;
        menu.style.overflowY = 'auto';
    }
});