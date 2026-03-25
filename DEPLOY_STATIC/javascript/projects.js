const projects = [
    {
        title: "Ikoyi Residence",
        img: "{% static 'images/befor-and-after-images.jpeg' %}",
        description: "Premium residential construction in Ikoyi."
    },
    {
        title: "Lekki Office Complex",
        img: "{% static 'images/Futurepro.webp' %}",
        description: "High-end commercial development in Lekki."
    },
    {
        title: "Victoria Island Renovation",
        img: "{% static 'images/premium_photo-1748283940309-8e68a0ef23d2.avif' %}",
        description: "Complete renovation and cladding project."
    }
];

const container = document.getElementById("projects-container");

projects.forEach(project => {
    const card = document.createElement("div");
    card.className = "bg-[#1f1f1f] rounded-xl overflow-hidden shadow-lg hover:shadow-2xl transition transform hover:scale-105";

    card.innerHTML = `
    <img src="${project.img}" alt="${project.title}" class="w-full h-56 object-cover">
    <div class="p-4">
      <h3 class="text-lg font-bold text-[#46B4B1] mb-2">${project.title}</h3>
      <p class="text-gray-300 text-sm">${project.description}</p>
    </div>
  `;

    container.appendChild(card);
});