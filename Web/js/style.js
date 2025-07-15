const explicationBox = document.getElementById('explication');

document.querySelectorAll('.mot-cle').forEach((mot) => {
    mot.addEventListener('mouseenter', () => {
        const texte = mot.getAttribute('data-explication');
        explicationBox.textContent = texte;
        explicationBox.classList.add('visible');
    });

    mot.addEventListener('mouseleave', () => {
        explicationBox.textContent = "Survolez un mot-clé pour voir l'explication ici.";
        explicationBox.classList.remove('visible');
    });
});
