document.documentElement.classList.add("js-enabled");

const menuButton = document.querySelector("[data-menu-toggle]");
const menu = document.getElementById("primary-navigation");

if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
        const isOpen = menu.classList.toggle("is-open");
        menuButton.setAttribute("aria-expanded", String(isOpen));
    });

    menu.addEventListener("click", (event) => {
        if (event.target.closest("a")) {
            menu.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && menu.classList.contains("is-open")) {
            menu.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.focus();
        }
    });
}
