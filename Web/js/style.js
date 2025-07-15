document.querySelectorAll('.mot-cle').forEach((mot) => {
    mot.addEventListener('mouseenter', () => {
        const texte = mot.getAttribute('data-explication');
        document.getElementById('explication').textContent = texte;
    });

    mot.addEventListener('mouseleave', () => {
        document.getElementById('explication').textContent = "Survolez un mot-clé pour voir l'explication ici.";
    });
});
