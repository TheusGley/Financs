const toggleButton = document.getElementById('toggleButton');
const sidebar = document.getElementById('sidebar');
const content = document.querySelector('.content');

toggleButton.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

content.addEventListener('click', () => {
    sidebar.classList.remove('active');
});

document.addEventListener('click', (event) => {
    if (!sidebar.contains(event.target) && !toggleButton.contains(event.target)) {
        sidebar.classList.remove('active');
    }
});
