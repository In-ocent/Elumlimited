document.addEventListener("DOMContentLoaded", () => {
    const startYear = 2004;
    const currentYear = new Date().getFullYear();
    const years = currentYear - startYear;
    document.getElementById("experience-years-section").textContent = years;
});