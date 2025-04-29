
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    form && form.addEventListener("submit", (e) => {
        const inputs = document.querySelectorAll("input[required]");
        inputs.forEach(input => {
            if (!input.value.trim()) {
                alert(`${input.name} is required.`);
                e.preventDefault();
            }
        });
    });
});
