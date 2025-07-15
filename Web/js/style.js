const explicationBox = document.getElementById('explication');

function changeTextWithFade(newText) {
    // Étape 1 : on fade-out
    explicationBox.classList.add('fade-out');

    // Étape 2 : après le fade-out (400ms), on change le texte, puis fade-in
    setTimeout(() => {
        explicationBox.textContent = newText;

        // Force reflow pour que le fade-in soit bien déclenché
        void explicationBox.offsetWidth;

        explicationBox.classList.remove('fade-out');
    }, 0);
}

document.querySelectorAll('.mot-cle').forEach((mot) => {
    mot.addEventListener('mouseenter', () => {
        const texte = mot.getAttribute('data-explication');
        changeTextWithFade(texte);
    });

    mot.addEventListener('mouseleave', () => {
        changeTextWithFade("Survolez un mot-clé pour voir l'explication ici.");
    });
});
